# Third-party notices

This file records third-party software and source material used by the public
explainer. Versions should match the lock files and reproducible environments.

## Mathematical and historical sources

The repository cites, links to, and discusses works by Levent Alpöge, Fable,
Andy Jiang, GPT, Aaron Lou, O.-H. Keller, Bass--Connell--Wright, Arno van den
Essen, Zbigniew Jelonek, and other authors. Those source works are not
relicensed by this repository. Short descriptions and mathematical facts are
provided with source links in the paper and literature audit.

## Website and animation software

- [Three.js](https://threejs.org/) is distributed under the MIT License.
- [Vite](https://vite.dev/) is distributed under the MIT License.
- [Manim Community](https://www.manim.community/) is distributed under the MIT
  License.
- [Manim Voiceover](https://voiceover.manim.community/) is distributed under
  the MIT License.
- [Piper TTS 1.4.2](https://github.com/OHF-Voice/piper1-gpl/tree/v1.4.2),
  used only as an external offline draft-narration runtime, is distributed
  under the GNU General Public License, version 3 or later. It is installed by
  `environment-animation.yml`; its source is not copied into this repository.

Transitive JavaScript and Python dependencies retain their respective license
terms. Their exact versions are recorded in the package lock and animation
environment files.

## Piper draft voice and training corpus

The recommended draft voice is
[`en_US-libritts-high`](https://huggingface.co/rhasspy/piper-voices/blob/main/en/en_US/libritts/high/MODEL_CARD).
Its per-voice model card specifies **CC BY 4.0**, 904 speakers, 22,050 Hz
output, and training from scratch on the LibriTTS `train-clean-360` split.
This project follows that voice-specific license and attribution record even
though broader collection pages can display different repository-level
metadata.

[LibriTTS (OpenSLR 60)](https://www.openslr.org/60/) is also distributed under
CC BY 4.0. It is derived from LibriVox audiobooks and Project Gutenberg text;
the `train-clean-360` archive is the split identified by the voice model card.
For transparent provenance, any published project draft made with this voice
should carry attribution to the model and dataset, including links to the
model card, OpenSLR record, and
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Cite the
[LibriTTS paper](https://arxiv.org/abs/1904.02882) in scholarly uses.

Neither Piper voice weights nor LibriTTS data are distributed in this
repository. The documented downloader stores the `.onnx` and `.onnx.json`
files outside the checkout. Human final narration recorded with
`RecorderService` is independent of this model and should carry the human
contributor's explicit CC BY 4.0 or CC0 grant.

The landing page's published 4:35 draft is identified there as synthesized
with Piper TTS `1.4.2`, `en_US-libritts-high`, speaker `0`. Its spoken script is
the repository's CC BY 4.0 canonical narration; the Piper runtime, voice model,
and LibriTTS source data retain the distinct terms recorded above. The page
does not present this draft as a human voice.

## Generated artwork

`site/public/assets/hero-marked-roots.png` was generated for this repository
with OpenAI's image-generation tooling under the direction of Bartosz
Naskrecki. The resulting project asset is released under CC BY 4.0 as stated in
`LICENSE-CONTENT`.
