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

The elementary browser curves and the Manim film's curve sequences share
the deterministic data in
[`shared/curve-fixtures.json`](../shared/curve-fixtures.json).  Regenerate it
from the exact Python formulas with:

```sh
python3 -m animations.math_core shared/curve-fixtures.json --samples 61
```

The richer browser-only presets add an eleven-line pencil and a sampled
$25\times31$ mesh of the plane $y=0$, together with their direct polynomial
images. Three highlighted rulings make the mesh deformation readable. The
browser evaluates these drawing samples with floating-point arithmetic; the
exact algebraic certificates remain the separate SymPy, Sage, and Magma
artifacts. Tests check every displayed source/image pair against the polynomial
map, verify the explicit image formula for the plane mesh, and enforce geometry
budgets.

Three.js is split into a deferred viewer chunk and loaded only as the section
approaches the viewport. Rendering is event-driven, pixel density is capped,
and repeated animation ticks on the same discretized sample do not rebuild the
coordinate table or redraw the canvases.

## Video handoff

The release page embeds these publication files:

- `site/public/media/marked-root-explainer.mp4`
- `site/public/media/marked-root-explainer.en.vtt`

The 4:38 MP4 is a 1080p H.264/AAC Manim render with reproducibly configured offline draft
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
viewer explicitly identifies its curves and sampled meshes as a real
three-dimensional slice of the six-real-dimensional space underlying
$\mathbb C^3$.

Code is MIT licensed. Site prose, original visual assets, the transcript,
captions, and released narration are CC BY 4.0; see the repository-level
license and third-party notices. The Piper runtime, voice model, training
corpus, and linked sources retain their respective terms.
