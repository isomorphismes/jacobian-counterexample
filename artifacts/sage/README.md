# SageMath certificate

Sage may try to initialize a cache in the user's home directory.  The following
keeps the cache in a disposable location and runs every exact assertion:

```sh
DOT_SAGE=/tmp/jacobian-sage sage artifacts/sage/verify.sage
DOT_SAGE=/tmp/jacobian-sage sage research/n2/low_degree_collision.sage
```

The research script computes an exact Gröbner basis for the normalized
degree-at-most-three collision ansatz and asserts that the ideal is `(1)`.
