# SymPy certificate

Run from the repository root:

```sh
python3 artifacts/sympy/verify.py
python3 artifacts/sympy/verify_plane_attack.py
python3 artifacts/sympy/verify_resultant_route.py
python3 research/n2/certify_pseudoplane_poisson.py
```

The program checks the full determinant, the three points, the rational
coordinate proof, equality of fiber ideals, the determinant-one normalization,
a secondary inverse-`x` resultant, both binary-cubic inverse charts, and the
nonproper escape family.  All coefficients
are exact `sympy.Rational` values.  It also certifies the commuting polynomial
vector fields that define the induced non-automorphic rank-three Weyl-algebra
endomorphism.

The second script checks the dimension-two research identities: the
equivariant noninjective quotient, its cubic factor, the linear-slice and
marked-plane differential identities, the arbitrary-target tangent obstruction
on the collision graph, the equivariant nonlinear-slice invariants, and the
octahedral degree-six cusp near-model and passport.  Passing it does not assert
a solution of the plane conjecture.

The third script verifies the exact left--right linear equivalence of Aaron
Lou's factor derivation, representative cases of the general
coefficient--resultant determinant law,
the collapse of the literal degree-two analogue, two quadratic--cubic slice
obstructions, and the noninjective quadratic-factor $\mathbb A^2$ scaffold.
It also certifies the universal-cover quotient, the rational
constant-Jacobian pseudo-plane chart, its genuine denominator, and degrees
two through six of the Chebyshev boundary obstruction.  It formulates, but
does not solve, the remaining nonlinear Poisson problem.

The fourth script works directly in the exceptional pseudo-plane Poisson
algebra.  It verifies the two rational Darboux charts and their symplectic
transition, the all-weight homogeneous bracket formulas, the natural locally
nilpotent flow, and the conformally Poisson etale self-map.  Most importantly,
it computes over the rationals that the coefficient ideal for a single
bracket-one pair of ambient total degree at most two has Groebner basis
`[1]`.  The accompanying valuation and residue proofs are in
[`pseudoplane-poisson-obstructions.md`](../../knowledge/pseudoplane-poisson-obstructions.md).
