---
title: Direct exact certificate
tags: [verification, exact-arithmetic]
---

# Direct exact certificate

The most literal certificate differentiates the three displayed polynomials
and expands a $3\times3$ determinant in $\mathbb Q[x,y,z]$.  SymPy,
SageMath, and Magma all reduce the result to $-2$.

The complete executable versions are:

- [`artifacts/sympy/verify.py`](../artifacts/sympy/verify.py),
- [`artifacts/sage/verify.sage`](../artifacts/sage/verify.sage),
- [`artifacts/magma/01_direct_verification.m`](../artifacts/magma/01_direct_verification.m).

A minimal SymPy fragment is:

```python
import sympy as s

x, y, z = s.symbols("x y z")
F = s.Matrix([
    (1+x*y)**3*z + y**2*(1+x*y)*(4+3*x*y),
    y + 3*x*(1+x*y)**2*z + 3*x*y**2*(4+3*x*y),
    2*x - 3*x**2*y - x**3*z,
])

assert s.expand(F.jacobian((x, y, z)).det()) == -2
```

## Exact substitutions

At $P_0=(0,0,-1/4)$, one immediately gets

$$
F(P_0)=(-1/4,0,0).
$$

At $P_+=(1,-3/2,13/2)$, the useful value is
$1+xy=-1/2$.  Then

$$
\begin{aligned}
F_1(P_+)&=(-1/2)^3(13/2)+(9/4)(-1/2)(-1/2)=-1/4,\\
F_2(P_+)&=-3/2+3(1)(1/4)(13/2)+3(1)(9/4)(-1/2)=0,\\
F_3(P_+)&=2+9/2-13/2=0.
\end{aligned}
$$

The involution

$$
(x,y,z)\longmapsto(-x,-y,z)
$$

leaves $F_1$ fixed and changes the signs of $F_2,F_3$.  Since the latter
two values are zero at $P_+$, it sends the calculation to
$P_-=(-1,3/2,13/2)$ automatically.

## Why this is not the preferred proof

A full determinant expansion is decisive but opaque: it confirms cancellation
without explaining it.  The next chapter compresses the determinant to a
two-by-two calculation and exposes the hidden cubic geometry.
