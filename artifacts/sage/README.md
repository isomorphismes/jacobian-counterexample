# SageMath certificate

Sage may try to initialize a cache in the user's home directory.  The following
keeps the cache in a disposable location and runs every exact assertion:

```sh
DOT_SAGE=/tmp/jacobian-sage sage artifacts/sage/verify.sage
```
