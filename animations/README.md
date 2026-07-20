# Narrated explainer

`JacobianStory` is the attribution-first Manim explainer for the explicit
three-dimensional map. The published offline Piper draft runs 4 minutes 35
seconds; the conservative human-narration planning estimate is about 5 minutes
45 seconds.
The scene uses three descriptions of one morphism:

1. [Levent Alpöge's formula post](https://x.com/__alpoge__/status/2079028340955197566)
   gives the explicit formula and credits Akhil and Fable in the post.
2. [Andy Jiang's post](https://x.com/davikrehalt/status/2079175065695035442)
   gives the projective marked-root description and explicitly presents it as
   GPT output.
3. [Aaron Lou's note](https://aaronlou.com/jacobian_counterexample_derivation.pdf)
   gives the factorization-resultant derivation and a global affine chart.

The repository contributors claim only compilation, checking, exposition,
animation, and web presentation.

## Files

- `jacobian_story.py`: `JacobianStory`, voice-service selection, and scene code.
- `piper_service.py`: offline Piper synthesis and content-addressed caching.
- `story_data.py`: canonical narration, provenance, and JSON export.
- `transcript.md`: text-first transcript generated from the canonical records.
- `math_core.py`: exact map, exact curve families, and sampled JSON export.
- `srt_to_vtt.py`: strict conversion of Manim SRT captions to browser WebVTT.
- `../shared/curve-fixtures.json`: deterministic samples shared with the site.
- `../environment-animation.yml`: pinned animation environment.

The formulas and metadata modules use only the Python standard library. They
can be tested on a machine without Manim.

## Environment

Current pins are Manim Community `0.20.1`, Manim Voiceover `0.4.0`, and
Piper TTS `1.4.2`.

```bash
conda env create -f environment-animation.yml
conda run -n jacobian-animation manim checkhealth
```

The scene deliberately uses Pango `Text`, not `Tex` or `MathTex`; rendering
does not require `dvisvgm`. FFmpeg, Cairo, Pango, and the Voiceover plugin are
still required.

## Voice modes

There are three explicit modes: silent CI timing, offline Piper draft speech,
and a human recording for the final publication. The final, preferred voice is
still `RecorderService`; Piper is a reproducible aid for reviewing a genuinely
narrated draft before the human track exists.

### Silent CI mode

The default is deterministic silence:

```bash
JACOBIAN_VOICE_SERVICE=silent \
  conda run -n jacobian-animation manim \
  --renderer=cairo --disable_caching --seed 20260720 -ql \
  --save_sections animations/jacobian_story.py JacobianStory
```

This mode creates silent WAV files from the canonical word count. It exercises
voice timing and caption generation without a microphone, network, API key, or
Whisper model.

### Reproducible offline Piper draft

The recommended draft model is **`en_US-libritts-high`**, not Lessac. It is a
22,050 Hz, 904-speaker model trained from scratch on LibriTTS
`train-clean-360`. Choose a speaker id from `0` through `903`; if the variable
is omitted, Piper uses speaker `0` for this multi-speaker model.

Piper requires both the `.onnx` model and its `.onnx.json` configuration. Keep
these large third-party files outside the repository. After creating the
environment, download them from Piper's official voice collection:

```bash
mkdir -p /absolute/path/outside-this-repo/piper-voices
conda run -n jacobian-animation python -m piper.download_voices \
  --download-dir /absolute/path/outside-this-repo/piper-voices \
  en_US-libritts-high
```

Then render the voiced draft entirely offline:

```bash
JACOBIAN_VOICE_SERVICE=piper \
JACOBIAN_PIPER_MODEL=/absolute/path/outside-this-repo/piper-voices/en_US-libritts-high.onnx \
JACOBIAN_PIPER_SPEAKER_ID=0 \
  conda run -n jacobian-animation manim \
  --renderer=cairo --disable_caching --seed 20260720 -ql \
  --save_sections animations/jacobian_story.py JacobianStory
```

`JACOBIAN_PIPER_CONFIG` is optional; it defaults to the model path plus
`.json`. `JACOBIAN_PIPER_SPEAKER_ID` is also optional. Each narration segment
is cached under a key containing the text, Piper version, model and config
SHA-256 hashes, speaker, and synthesis settings. Thus an unchanged setup
reuses its clips, while replacing either voice file invalidates them even at
the same path. Captions continue to come from the canonical narration, not
speech recognition.

The download command needs network access once; synthesis and later cache hits
do not. Model weights and raw Voiceover cache clips are intentionally not
committed; only the selected web MP4 and its captions are publication assets.
See the exact Piper, model, and LibriTTS attribution in
[`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md).

### Preferred human final

The publication mode records a contributor's human voice:

```bash
JACOBIAN_VOICE_SERVICE=recorder \
  conda run -n jacobian-animation manim \
  --renderer=cairo --disable_caching --seed 20260720 \
  -r 1920,1080 --fps 30 --format=mp4 --save_sections \
  -o jacobian-story animations/jacobian_story.py JacobianStory
```

`RecorderService(transcription_model=None)` is intentional. Caption text is
split deterministically from the canonical narration, so Whisper is not needed. Keep
the accepted recordings in the Voiceover cache if later renders must be
bit-for-bit reproducible. A contributor who records the final track should
license that recording explicitly under CC BY 4.0 or CC0.

Manim Voiceover's official stable documentation currently recommends
`--disable_caching`; all commands retain it.

## Captions and web assets

Manim writes an SRT file next to the rendered movie. Convert and validate it:

```bash
python3 animations/srt_to_vtt.py \
  path/to/jacobian-story.srt path/to/jacobian-story.en.vtt
```

The landing page includes the WebVTT file as its default captions track and
exposes every narration segment as ordinary HTML, with a direct link to
`transcript.md`. Visual identity never depends on color alone; narration and
labels identify each root branch.

Generate exact shared data for another renderer with:

```bash
python3 -m animations.math_core shared/curve-fixtures.json --samples 61
python3 -m animations.story_data shared/story-metadata.json
```

The visualization is explicitly labeled as the real slice `R^3` inside the
complex map on `C^3`.

## Verification

The Manim-free checks cover formula parity, the three inverse branches,
deterministic JSON export, transcript synchronization, credit URLs, caption
conversion, source policy, dependency pins, and mocked Piper synthesis and
cache invalidation:

```bash
pytest -q tests/test_animation_assets.py tests/test_piper_service.py
```

The current release passed a low-quality full-render review and a 1080p visual
inspection. `ffprobe` confirms video, audio, frame rate, and duration; the
published hashes and inspection values are recorded in
[`site/public/media/README.md`](../site/public/media/README.md). Any replacement
render must repeat those gates. No render is claimed merely because the
source-level tests pass.

## License

Original animation source is MIT-licensed under `LICENSE-CODE`; repository
text, captions, and released narration are CC BY 4.0 under `LICENSE-CONTENT`.
Manim, Manim Voiceover, linked posts, linked papers, fonts, models, corpora,
and voice services retain their own licenses and terms.

Official implementation references:

- [Manim installation](https://docs.manim.community/en/stable/installation.html)
- [Manim render configuration](https://docs.manim.community/en/stable/guides/configuration.html)
- [Manim Voiceover releases](https://github.com/ManimCommunity/manim-voiceover/releases)
- [Manim Voiceover quickstart](https://voiceover.manim.community/en/stable/quickstart.html)
- [Manim Voiceover API](https://voiceover.manim.community/en/stable/api.html)
- [Piper 1.4.2 source](https://github.com/OHF-Voice/piper1-gpl/tree/v1.4.2)
- [`en_US-libritts-high` model card](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/libritts/high/MODEL_CARD)
- [LibriTTS corpus record (OpenSLR 60)](https://www.openslr.org/60/)
