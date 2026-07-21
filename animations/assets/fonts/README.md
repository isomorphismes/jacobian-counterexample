# Bundled animation typeface

`Inter-VariableFont_opsz-wght.ttf` is the unmodified Inter 4.001 variable font
from Google Fonts commit
[`e1d6480`](https://github.com/google/fonts/tree/e1d6480102fed30739fead0faee463101f892c8f/ofl/inter).
The film uses two repository-unique static Modified Versions, so an unrelated
Inter installation cannot win Pango's family-name lookup.

```text
upstream   Inter-VariableFont_opsz-wght.ttf
size       876576 bytes
SHA-256    29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031
family     Inter
version    4.001; git-66647c0bb

regular    JacobianCounterexampleFilmText-Regular.ttf
size       341712 bytes
SHA-256    2282daa5748d02c1ac3703811c778a5e4775d13f4563fc9957db7ab8402d664d

bold       JacobianCounterexampleFilmText-Bold.ttf
size       343388 bytes
SHA-256    11ca1dd863323d2ab533be2e4094266b838f56040d18f9fbaa633b360585cb28

family     Jacobian Counterexample Film Text
version    4.001-jcfilm.2; git-66647c0bb
instances  opsz=14, wght=400 and opsz=14, wght=700
```

Run `python animations/build_font_asset.py` in the pinned animation environment
to reproduce both faces. The script uses FontTools 4.51.0 with timestamp
recalculation disabled. It makes direct static instances, assigns unique name
records 1, 2, 3, 4, 5, 6, 16, 17, and 25, and verifies that every compiled
design table matches the corresponding unrenamed instance. Typographic family
and subfamily records 16 and 17 are required for reliable Pango weight
selection on macOS. The scene also compares actual Regular and Bold glyph
outlines with a deliberately missing family's fallback before rendering.

Manim's text SVG cache does not hash font files. If either derived face changes,
also change the public family name and the probe hash prefixes (or clear the
text SVG cache) before rendering, or old outlines may be reused.

The bundled `OFL.txt` notice says copyright 2020 The Inter Project Authors; the
font files retain the upstream embedded copyright-2016 name record. All three
font files remain under SIL Open Font License Version 1.1. The static, renamed
files are Modified Versions under that license. The original embedded
copyright, trademark, and attribution metadata is preserved; the Inter Project
Authors and Google do not endorse this project.
