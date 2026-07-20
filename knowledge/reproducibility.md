---
title: Reproducibility
tags: [reproducibility, code, magma, sage, sympy]
---

# Reproducibility

All decisive calculations use exact rational arithmetic.  No numerical
tolerance, random point sample, or remote service is required.

## One-command checks

From the repository root:

```sh
make verify
make book
```

Or run each layer separately:

```sh
python3 artifacts/sympy/verify.py
python3 artifacts/sympy/verify_plane_attack.py
python3 artifacts/sympy/verify_resultant_route.py
python3 research/n2/certify_pseudoplane_poisson.py
python3 research/n2/search_resultant_poisson.py --poisson-degree 3
DOT_SAGE=/tmp/jacobian-sage sage artifacts/sage/verify.sage
DOT_SAGE=/tmp/jacobian-sage sage research/n2/low_degree_collision.sage
cd artifacts/magma
MAGMA_STARTUP_FILE=/dev/null /Applications/Magma/magma run_all.m
```

The `DOT_SAGE` and `MAGMA_STARTUP_FILE` settings only isolate user-specific
cache/startup behavior.  They do not change the coefficient field or algorithms.

## What each implementation checks

| Artifact | Threefold map | Plane descent | Near-models | Resultant route |
|---|---:|---:|---:|---:|
| SymPy scripts | full | identities | yes | full identities/search |
| Sage scripts | full | degree-3 collision ideal | no | no |
| Magma suite | full | structural identities | yes | core identities |
| Jupyter notebook | full core | documentation | documentation | documentation |

## Jupyter Book

Build the book with

```sh
jupyter-book build knowledge
```

and open `knowledge/_build/html/index.html`.  The notebook is stored with exact
outputs but book builds do not re-execute it by default, so documentation builds
remain deterministic.  Re-execute explicitly with:

```sh
jupyter nbconvert --to notebook --execute --inplace \
  knowledge/notebooks/sympy-verification.ipynb
```

## Obsidian

Open the `knowledge/` directory as an Obsidian vault.  It already contains a
minimal `.obsidian/` configuration.  Ordinary relative Markdown links are used
so the same source works in Obsidian, GitHub, and Jupyter Book.

## Expected outputs

The command-line certificates terminate on any failed assertion.  Successful
runs end with messages of the form:

```text
PASS: all SymPy certificates verified exactly over Q.
PASS: all exact plane-attack certificates verified over Q.
PASS: all exact factorization/resultant route certificates verified over Q.
PASS: pseudo-plane Poisson identities and quadratic no-go certified over Q.
PASS: all SageMath certificates verified exactly over Q.
PASS: all Magma certificates completed.
```
