# Third-party notices

This file records third-party software and source material used by the public
explainer. Versions should match the lock files and reproducible environments.

## Mathematical and historical sources

The repository cites, links to, and discusses works by Levent Alpöge, Fable,
Andy Jiang, GPT, Aaron Lou (@aaron_lou), O.-H. Keller,
Bass--Connell--Wright, Arno van den Essen, Zbigniew Jelonek, and other
authors. Those source works are not
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

## Animation typeface

The film bundles Inter 4.001 from the pinned
[Google Fonts commit](https://github.com/google/fonts/tree/e1d6480102fed30739fead0faee463101f892c8f/ofl/inter),
under the SIL Open Font License Version 1.1. The bundled OFL notice says
copyright 2020 The Inter Project Authors; the font's preserved embedded name
record says copyright 2016 The Inter Project Authors. The unmodified input and
its license are stored at
`animations/assets/fonts/Inter-VariableFont_opsz-wght.ttf` and
`animations/assets/fonts/OFL.txt`.

```text
upstream  Inter-VariableFont_opsz-wght.ttf
SHA-256  29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031

regular   JacobianCounterexampleFilmText-Regular.ttf
SHA-256  2282daa5748d02c1ac3703811c778a5e4775d13f4563fc9957db7ab8402d664d

bold      JacobianCounterexampleFilmText-Bold.ttf
SHA-256  11ca1dd863323d2ab533be2e4094266b838f56040d18f9fbaa633b360585cb28
```

`Jacobian Counterexample Film Text` Regular and Bold are static Modified
Versions of Inter 4.001, produced reproducibly by
`animations/build_font_asset.py` with FontTools 4.51.0. They instantiate the
pinned source at `opsz=14, wght=400` and `opsz=14, wght=700`, then assign the
repository-unique OpenType name records 1, 2, 3, 4, 5, 6, 16, 17, and 25. The
build verifies that each face's compiled design tables exactly match its
direct, unrenamed static instance. The explicit typographic family/subfamily
records prevent Pango from listing the family but silently substituting its
Bold fallback; the scene additionally compares actual glyph outlines against
a deliberately missing family before every render. The original embedded
copyright, trademark, attribution, and license metadata is preserved. "Inter"
identifies the upstream work only; the Inter Project Authors and Google do not
endorse this project.

Manim's text SVG cache does not include font-file bytes in its key. A future
font modification must therefore change the unique family name and probe hash
prefixes, or be accompanied by an explicit text-cache clear before rendering.

All three font files remain under SIL OFL 1.1. Rendered film frames and other
documents made with them are not Font Software and retain the project's stated
content license.

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

The landing page's published 4:37 draft is identified there as synthesized
with Piper TTS `1.4.2`, `en_US-libritts-high`, speaker `0`. Its spoken script is
the repository's CC BY 4.0 canonical narration; the Piper runtime, voice model,
and LibriTTS source data retain the distinct terms recorded above. The page
does not present this draft as a human voice.

## Generated artwork

`site/public/assets/hero-marked-roots.png` was generated for this repository
with OpenAI's image-generation tooling under the direction of Bartosz
Naskrecki. The resulting project asset is released under CC BY 4.0 as stated in
`LICENSE-CONTENT`.
