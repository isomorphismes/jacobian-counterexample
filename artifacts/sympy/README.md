# SymPy certificate

Run from the repository root:

```sh
python3 artifacts/sympy/verify.py
```

The program checks the full determinant, the three points, the rational
coordinate proof, equality of fiber ideals, the determinant-one normalization,
a secondary inverse-`x` resultant, both binary-cubic inverse charts, and the
nonproper escape family.  All coefficients
are exact `sympy.Rational` values.  It also certifies the commuting polynomial
vector fields that define the induced non-automorphic rank-three Weyl-algebra
endomorphism.
