# Shared visualization fixtures

`curve-fixtures.json` is the canonical sampled bridge between the Manim film
and the interactive landing page. It is generated, not hand-authored:

```bash
python3 -m animations.math_core shared/curve-fixtures.json --samples 61
```

Schema version 1 contains:

- the displayed polynomial map and source/target coordinate order;
- three elementary source curves and their exact images;
- the common target family
  `2*T*(T-s)*(T-(1-s))` and its three marked-root inverse branches;
- the announced three-point fiber; and
- a required warning that the plotted points lie in `R^3`, a real slice of
  the map on `C^3`.

Every sample record has the form
`{"parameter": number, "point": [number, number, number]}`. Tests regenerate
all 61 samples from the exact formulas and require byte-independent JSON
equality after parsing.
