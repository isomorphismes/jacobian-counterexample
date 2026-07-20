"""Offline Piper speech service for reproducible draft narration.

The service intentionally lives outside :mod:`jacobian_story` so its cache
contract can be tested with small stand-ins for Manim Voiceover and Piper.
Piper is imported lazily: importing the animation source does not load ONNX
Runtime or a voice model.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
import tempfile
from typing import Any
import wave

from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService


PIPER_VERSION = "1.4.2"
RECOMMENDED_PIPER_VOICE = "en_US-libritts-high"
PIPER_MODEL_ENV = "JACOBIAN_PIPER_MODEL"
PIPER_CONFIG_ENV = "JACOBIAN_PIPER_CONFIG"
PIPER_SPEAKER_ENV = "JACOBIAN_PIPER_SPEAKER_ID"


def _sha256_file(path: Path) -> str:
    """Return a streaming SHA-256 digest without loading a model into RAM."""

    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _optional_speaker_id(value: int | str | None) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("Piper speaker id must be a non-negative integer")
    try:
        speaker_id = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            "Piper speaker id must be a non-negative integer"
        ) from error
    if speaker_id < 0 or str(value).strip() != str(speaker_id):
        raise ValueError("Piper speaker id must be a non-negative integer")
    return speaker_id


class PiperSpeechService(SpeechService):
    """Synthesize deterministic, cached draft narration with Piper 1.4.2.

    ``model_path`` is read from ``JACOBIAN_PIPER_MODEL`` when omitted. The
    companion config defaults to ``<model_path>.json`` and can be overridden
    with ``JACOBIAN_PIPER_CONFIG``. ``JACOBIAN_PIPER_SPEAKER_ID`` is optional;
    Piper selects speaker zero for a multi-speaker model when it is absent.

    Cache keys include hashes of both local voice files. Replacing a model at
    the same path therefore cannot silently reuse stale audio. The returned
    ``input_text`` is always the original text (including bookmarks), which
    preserves Manim Voiceover's caption and timing behavior.
    """

    def __init__(
        self,
        model_path: str | os.PathLike[str] | None = None,
        config_path: str | os.PathLike[str] | None = None,
        speaker_id: int | str | None = None,
        *,
        length_scale: float | None = None,
        noise_scale: float | None = None,
        noise_w_scale: float | None = None,
        normalize_audio: bool = True,
        volume: float = 1.0,
        use_cuda: bool = False,
        **kwargs: object,
    ) -> None:
        raw_model_path = model_path or os.getenv(PIPER_MODEL_ENV)
        if not raw_model_path:
            raise ValueError(
                f"Set {PIPER_MODEL_ENV} to a Piper .onnx voice model path"
            )

        self.model_path = Path(raw_model_path).expanduser().resolve()
        raw_config_path = config_path or os.getenv(PIPER_CONFIG_ENV)
        self.config_path = (
            Path(raw_config_path).expanduser().resolve()
            if raw_config_path
            else Path(f"{self.model_path}.json")
        )
        if not self.model_path.is_file():
            raise FileNotFoundError(
                f"Piper model file does not exist: {self.model_path}"
            )
        if not self.config_path.is_file():
            raise FileNotFoundError(
                f"Piper config file does not exist: {self.config_path}"
            )

        raw_speaker_id = (
            speaker_id
            if speaker_id is not None
            else os.getenv(PIPER_SPEAKER_ENV)
        )
        self.speaker_id = _optional_speaker_id(raw_speaker_id)
        self.length_scale = length_scale
        self.noise_scale = noise_scale
        self.noise_w_scale = noise_w_scale
        self.normalize_audio = bool(normalize_audio)
        self.volume = float(volume)
        self.use_cuda = bool(use_cuda)
        self.model_sha256 = _sha256_file(self.model_path)
        self.config_sha256 = _sha256_file(self.config_path)
        self._voice: Any | None = None
        super().__init__(transcription_model=None, **kwargs)

    def _cache_input(self, clean_text: str) -> dict[str, object]:
        return {
            "input_text": clean_text,
            "service": "piper-tts",
            "service_version": PIPER_VERSION,
            "model_name": self.model_path.name,
            "model_sha256": self.model_sha256,
            "config_name": self.config_path.name,
            "config_sha256": self.config_sha256,
            "speaker_id": self.speaker_id,
            "length_scale": self.length_scale,
            "noise_scale": self.noise_scale,
            "noise_w_scale": self.noise_w_scale,
            "normalize_audio": self.normalize_audio,
            "volume": self.volume,
            "use_cuda": self.use_cuda,
        }

    def _load_voice(self) -> Any:
        if self._voice is None:
            from piper import PiperVoice

            self._voice = PiperVoice.load(
                self.model_path,
                config_path=self.config_path,
                use_cuda=self.use_cuda,
            )
        return self._voice

    def generate_from_text(
        self,
        text: str,
        cache_dir: str | os.PathLike[str] | None = None,
        path: str | os.PathLike[str] | None = None,
        **kwargs: object,
    ) -> dict[str, object]:
        """Generate one WAV clip, or return its content-addressed cache hit."""

        if kwargs:
            unknown = ", ".join(sorted(kwargs))
            raise TypeError(f"Unsupported Piper synthesis options: {unknown}")

        clean_text = remove_bookmarks(text)
        input_data = self._cache_input(clean_text)
        output_dir = Path(self.cache_dir if cache_dir is None else cache_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        cached = self.get_cached_result(input_data, output_dir)
        if cached is not None:
            cached_audio = output_dir / str(cached["original_audio"])
            if cached_audio.is_file():
                # Audio is keyed by bookmark-free text, but trackers must keep
                # the exact current text for captions and bookmark positions.
                cached["input_text"] = text
                return cached

        filename = (
            Path(path).name
            if path is not None
            else f"{self.get_audio_basename(input_data)}.wav"
        )
        audio_path = output_dir / filename

        from piper import SynthesisConfig

        synthesis_config = SynthesisConfig(
            speaker_id=self.speaker_id,
            length_scale=self.length_scale,
            noise_scale=self.noise_scale,
            noise_w_scale=self.noise_w_scale,
            normalize_audio=self.normalize_audio,
            volume=self.volume,
        )

        temporary_path: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                prefix=f".{audio_path.stem}-",
                suffix=".wav",
                dir=output_dir,
                delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)

            with wave.open(str(temporary_path), "wb") as wav_file:
                self._load_voice().synthesize_wav(
                    clean_text,
                    wav_file,
                    syn_config=synthesis_config,
                )

            with wave.open(str(temporary_path), "rb") as wav_file:
                if wav_file.getnframes() == 0:
                    raise RuntimeError("Piper produced an empty WAV clip")
            temporary_path.replace(audio_path)
            temporary_path = None
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": filename,
        }
