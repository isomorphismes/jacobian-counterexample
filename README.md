# A three-dimensional Keller map with a three-point fiber

This repository is an exact, reproducible audit of the polynomial map announced
on 2026-07-20 as a counterexample to the Jacobian conjecture.  The finite
algebra needed for the conclusion checks out:

Private canonical remote: [nasqret/jacobian-counterexample](https://github.com/nasqret/jacobian-counterexample).

\[
\begin{aligned}
F_1&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
F_2&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
F_3&=2x-3x^2y-x^3z
\end{aligned}
\]

satisfies

\[
\det JF=-2
\]

as a polynomial identity over `Z`, while the scheme-theoretic fiber over
\((-1/4,0,0)\) is

\[
\left(F_1+\frac14,F_2,F_3\right)
=\left(z-\frac{27}{4}x^2+\frac14,
        y+\frac32x,
        x^3-x\right).
\]

Consequently that fiber consists of exactly the three reduced points

\[
(0,0,-1/4),\qquad(1,-3/2,13/2),\qquad(-1,3/2,13/2).
\]

Thus, for the standard characteristic-zero statement, this map is a
counterexample in dimension `3`.  Taking its product with the identity gives a
counterexample in every dimension `n >= 3`.  This is a mathematical conclusion
from the displayed identities; attribution, priority, and peer-review status are
tracked separately in the [literature audit](knowledge/literature-audit.md).

## Determinant-one integral normalization

The linearly normalized map below has integer coefficients, determinant `1`,
and identity linear part.  Put `U = 1 + 2XY` and define

\[
\begin{aligned}
H_1&=X-3X^2Y-2X^3Z,\\
H_2&=Y+6XU^2Z+6XY^2(4+6XY),\\
H_3&=U^3Z+Y^2U(4+6XY).
\end{aligned}
\]

Then `det JH = 1`, but

\[
H(0,0,-1/4)=H(1/2,-3/2,13/2)=H(-1/2,3/2,13/2)=(0,0,-1/4).
\]

This normalization removes any ambiguity about whether “nonzero constant” or
“equal to one” is intended in the conjecture.

## Hidden cubic: why the example works

For a target `(a,b,c)`, form the binary cubic

\[
Q_{a,b,c}(U,V)=cU^3-2U^2V+bUV^2-2aV^3.
\]

With `(A,B,C)=F(x,y,z)`, `U=1+xy`, and `V=x`, there are global polynomial
identities

\[
Q_{A,B,C}(U,V)=0,\qquad Q_U=2V,\qquad Q_V=-2U.
\]

Thus a source point is exactly a target cubic together with a marked simple
projective root; `F` forgets the root.  A generic cubic has three such roots,
so `F` has geometric degree `3`.  Cubics with a triple root have no preimage,
and the cubic discriminant is exactly the nonproperness hypersurface.  The full
inverse formulas and proofs are in [the binary-cubic chapter](knowledge/generic-fiber.md).

## Reproduce

All calculations use exact rational arithmetic.

```sh
python3 artifacts/sympy/verify.py
DOT_SAGE=/tmp/jacobian-sage sage artifacts/sage/verify.sage
(cd artifacts/magma && MAGMA_STARTUP_FILE=/dev/null /Applications/Magma/magma run_all.m)
pytest -q
jupyter-book build knowledge
```

`make verify` runs the locally available algebra systems and tests; `make book`
builds the HTML book at `knowledge/_build/html/index.html`.

## Repository guide

- [memory.md](memory.md) is the curated, durable research memory.
- [journal.md](journal.md) is the chronological audit trail.
- [plan.md](plan.md) records gates, completed work, and next research questions.
- [knowledge/](knowledge/index.md) is both an Obsidian vault and a Jupyter Book.
- [artifacts/magma/](artifacts/magma/README.md) contains compilable Magma certificates.
- [artifacts/sympy/verify.py](artifacts/sympy/verify.py) and
  [artifacts/sage/verify.sage](artifacts/sage/verify.sage) provide independent
  open-source verification.

## Scope and date

The web-status audit is frozen at **2026-07-20 (Europe/Warsaw)**.  The
counterexample announcement was only hours old when this repository was made;
the exact proof is self-contained, but claims about reception and priority must
be updated as the literature develops.
