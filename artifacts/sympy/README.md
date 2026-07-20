# SymPy certificate

Run from the repository root:

```sh
python3 artifacts/sympy/verify.py
python3 artifacts/sympy/verify_plane_attack.py
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
