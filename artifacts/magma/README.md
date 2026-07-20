# Magma certificates

These self-contained Magma programs verify the proposed polynomial map using
exact rational arithmetic.

- `01_direct_verification.m` computes the full (3\times3) Jacobian,
  verifies its determinant is (-2), and checks the three stated preimages.
- `02_structural_certificate.m` verifies a smaller, independently readable
  weighted-coordinate determinant identity.
- `03_fiber_certificate.m` proves equality with the triangular fiber ideal
  \((4z-27x^2+1,\ 2y+3x,\ x(x-1)(x+1))\), and verifies that it is
  zero-dimensional and radical.
- `04_normalization_certificate.m` verifies the preferred integral linear
  conjugate `H`: its Jacobian determinant is `1`, its linear part is the
  identity, and its displayed three-point fiber is exact.
- `05_binary_cubic_certificate.m` verifies the structural identities
  `Q=0`, `Q_U=2V`, and `Q_V=-2U` for the associated binary cubic, then proves
  that the fiber over `(1/3,2,2/3)` is the unit ideal.
- `run_all.m` runs every certificate and exits nonzero if an assertion fails.

On this Mac, Magma is installed outside `PATH`. Run from this directory:

```sh
cd artifacts/magma
MAGMA_STARTUP_FILE=/dev/null /Applications/Magma/magma run_all.m
```

Setting `MAGMA_STARTUP_FILE` avoids the host's optional personal startup file;
it does not alter the Magma system libraries or any calculation.

No floating-point arithmetic or probabilistic check is used.
