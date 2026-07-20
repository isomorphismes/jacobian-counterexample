# Landing page

This directory contains the static GitHub Pages presentation for **One Map,
Three Descriptions**.  It uses semantic HTML, TypeScript, Vite, and Three.js;
there is no framework, CDN, analytics script, or remote font request.

## Develop and verify

```sh
cd site
npm ci
npm run typecheck
npm test
npm run build
npm run preview
```

The production build is written to the ignored `site/dist/` directory.  The
assembly step copies the canonical paper and, when available, the built
Jupyter Book into that directory.

The browser and Manim visualizations share the deterministic data in
[`shared/curve-fixtures.json`](../shared/curve-fixtures.json).  Regenerate it
from the exact Python formulas with:

```sh
python3 -m animations.math_core shared/curve-fixtures.json --samples 61
```

The browser performs all final coordinate evaluation locally and the tests
check every displayed source/image pair against the polynomial map.

## Video handoff

The release page embeds these publication files:

- `site/public/media/marked-root-explainer.mp4`
- `site/public/media/marked-root-explainer.en.vtt`

The 4:35 MP4 is a 1080p H.264/AAC Manim render with reproducibly configured offline draft
narration from Piper TTS `1.4.2`, `en_US-libritts-high`, speaker `0`. The human
recording described in [`animations/README.md`](../animations/README.md)
remains the preferred final voice. The page identifies this distinction beside
the player instead of presenting synthesized audio as a human recording.

The exact canonical narration is also ordinary HTML inside the page. During
assembly, [`animations/transcript.md`](../animations/transcript.md) is copied
to `dist/media/marked-root-explainer-transcript.md` as a downloadable text-first
alternative. The WebVTT captions and HTML transcript must agree with that
canonical record; the website content tests enforce the 14 scene identifiers,
and the Python animation tests enforce the full spoken text.

## Accessibility and scope

The page includes a skip link, visible keyboard focus, semantic reading order,
caption/transcript support, reduced-motion behavior, keyboard plot controls,
and an accessible coordinate table that remains useful without WebGL.  The
viewer explicitly identifies its curves as a real three-dimensional slice of
the six-real-dimensional space underlying `C^3`.

Code is MIT licensed. Site prose, original visual assets, the transcript,
captions, and released narration are CC BY 4.0; see the repository-level
license and third-party notices. The Piper runtime, voice model, training
corpus, and linked sources retain their respective terms.
