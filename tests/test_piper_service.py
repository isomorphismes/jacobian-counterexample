"""Manim-free contract tests for the local Piper voice service."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys
import types

import pytest


ROOT = Path(__file__).parents[1]


@pytest.fixture
def mocked_piper_service(monkeypatch, tmp_path):
    """Load the production module against tiny Voiceover/Piper stand-ins."""

    default_cache = tmp_path / "default-cache"

    class FakeSpeechService:
        def __init__(
            self,
            transcription_model=None,
            cache_dir=None,
            **kwargs,
        ):
            assert transcription_model is None
            assert not kwargs
            self.cache_dir = Path(cache_dir or default_cache)
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self._cache = {}

        @staticmethod
        def _key(input_data):
            return json.dumps(input_data, sort_keys=True)

        def get_audio_basename(self, input_data):
            digest = hashlib.sha256(
                self._key(input_data).encode("utf-8")
            ).hexdigest()
            return f"piper-test-{digest[:12]}"

        def get_cached_result(self, input_data, cache_dir):
            del cache_dir
            result = self._cache.get(self._key(input_data))
            return None if result is None else deepcopy(result)

        def _wrap_generate_from_text(self, text, **kwargs):
            result = self.generate_from_text(text, **kwargs)
            result["final_audio"] = result["original_audio"]
            self._cache[self._key(result["input_data"])] = deepcopy(result)
            return result

    helper_module = types.ModuleType("manim_voiceover.helper")
    helper_module.remove_bookmarks = lambda text: re.sub(
        r"<bookmark\s+mark=['\"]\w+['\"]\s*/>", "", text
    )
    base_module = types.ModuleType("manim_voiceover.services.base")
    base_module.SpeechService = FakeSpeechService
    services_module = types.ModuleType("manim_voiceover.services")
    voiceover_module = types.ModuleType("manim_voiceover")
    monkeypatch.setitem(sys.modules, "manim_voiceover", voiceover_module)
    monkeypatch.setitem(sys.modules, "manim_voiceover.helper", helper_module)
    monkeypatch.setitem(sys.modules, "manim_voiceover.services", services_module)
    monkeypatch.setitem(
        sys.modules, "manim_voiceover.services.base", base_module
    )

    class FakeSynthesisConfig:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    class FakeVoice:
        def __init__(self):
            self.calls = []

        def synthesize_wav(self, text, wav_file, syn_config):
            self.calls.append((text, syn_config))
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(22_050)
            wav_file.writeframes(b"\x00\x00" * 64)

    class FakePiperVoice:
        loads = []

        @classmethod
        def load(cls, model_path, config_path=None, use_cuda=False):
            voice = FakeVoice()
            cls.loads.append((model_path, config_path, use_cuda, voice))
            return voice

    piper_module = types.ModuleType("piper")
    piper_module.PiperVoice = FakePiperVoice
    piper_module.SynthesisConfig = FakeSynthesisConfig
    monkeypatch.setitem(sys.modules, "piper", piper_module)

    module_name = "jacobian_piper_service_under_test"
    source_path = ROOT / "animations" / "piper_service.py"
    spec = importlib.util.spec_from_file_location(module_name, source_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    monkeypatch.setitem(sys.modules, module_name, module)
    spec.loader.exec_module(module)
    return module, FakePiperVoice


def _voice_files(tmp_path):
    model = tmp_path / "en_US-libritts-high.onnx"
    config = tmp_path / "en_US-libritts-high.onnx.json"
    model.write_bytes(b"small fake ONNX model")
    config.write_text('{"audio":{"sample_rate":22050}}', encoding="utf-8")
    return model, config


def test_piper_synthesizes_once_then_reuses_content_addressed_cache(
    mocked_piper_service, monkeypatch, tmp_path
):
    module, fake_piper_voice = mocked_piper_service
    model, config = _voice_files(tmp_path)
    monkeypatch.setenv(module.PIPER_MODEL_ENV, str(model))
    monkeypatch.delenv(module.PIPER_CONFIG_ENV, raising=False)
    monkeypatch.setenv(module.PIPER_SPEAKER_ENV, "17")

    cache_dir = tmp_path / "voice-cache"
    service = module.PiperSpeechService(cache_dir=cache_dir)
    narration = "Mark <bookmark mark='root'/> one root, then forget it."
    first = service._wrap_generate_from_text(narration)
    second = service._wrap_generate_from_text(narration)

    assert first["input_text"] == second["input_text"] == narration
    assert first["original_audio"] == second["original_audio"]
    assert (cache_dir / first["original_audio"]).is_file()
    assert len(fake_piper_voice.loads) == 1
    loaded_model, loaded_config, use_cuda, voice = fake_piper_voice.loads[0]
    assert loaded_model == model.resolve()
    assert loaded_config == config.resolve()
    assert use_cuda is False
    assert len(voice.calls) == 1
    clean_text, synthesis_config = voice.calls[0]
    assert clean_text == "Mark  one root, then forget it."
    assert synthesis_config.speaker_id == 17

    cache_input = first["input_data"]
    assert cache_input["service"] == "piper-tts"
    assert cache_input["service_version"] == "1.4.2"
    assert cache_input["model_name"] == model.name
    assert cache_input["config_name"] == config.name
    assert len(cache_input["model_sha256"]) == 64
    assert len(cache_input["config_sha256"]) == 64
    assert cache_input["speaker_id"] == 17
    assert str(tmp_path) not in json.dumps(cache_input, sort_keys=True)


def test_piper_cache_identity_changes_when_model_contents_change(
    mocked_piper_service, tmp_path
):
    module, _ = mocked_piper_service
    model, config = _voice_files(tmp_path)
    first = module.PiperSpeechService(
        model_path=model,
        config_path=config,
        cache_dir=tmp_path / "cache-a",
    )
    first_identity = first._cache_input("same words")

    model.write_bytes(b"different fake ONNX model")
    second = module.PiperSpeechService(
        model_path=model,
        config_path=config,
        cache_dir=tmp_path / "cache-b",
    )
    second_identity = second._cache_input("same words")

    assert first_identity["model_name"] == second_identity["model_name"]
    assert first_identity["model_sha256"] != second_identity["model_sha256"]
    assert first.get_audio_basename(first_identity) != second.get_audio_basename(
        second_identity
    )


def test_piper_reports_missing_model_and_invalid_speaker_clearly(
    mocked_piper_service, monkeypatch, tmp_path
):
    module, _ = mocked_piper_service
    monkeypatch.delenv(module.PIPER_MODEL_ENV, raising=False)
    monkeypatch.delenv(module.PIPER_CONFIG_ENV, raising=False)
    monkeypatch.delenv(module.PIPER_SPEAKER_ENV, raising=False)
    with pytest.raises(ValueError, match=module.PIPER_MODEL_ENV):
        module.PiperSpeechService()

    model, config = _voice_files(tmp_path)
    with pytest.raises(ValueError, match="non-negative integer"):
        module.PiperSpeechService(
            model_path=model,
            config_path=config,
            speaker_id="1.5",
        )


def test_piper_source_is_lazy_and_declares_recommended_voice():
    source = (ROOT / "animations" / "piper_service.py").read_text(
        encoding="utf-8"
    )
    before_class = source.split("class PiperSpeechService", maxsplit=1)[0]
    assert "from piper import" not in before_class
    assert 'RECOMMENDED_PIPER_VOICE = "en_US-libritts-high"' in source
