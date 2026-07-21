---
title: Determinant-one integral normalization
tags: [normalization, integer-coefficients]
---

# Determinant-one integral normalization

Some formulations normalize the constant Jacobian to $1$ and the linear
part to the identity.  Both conditions can be imposed without losing integer
coefficients.

The linear part of $F$ is

$$
L(x,y,z)=(z,y,2x).
$$

Let $D=\operatorname{diag}(2,1,1)$, and define

$$
H=D^{-1}\circ L^{-1}\circ F\circ D.
$$

Writing $T=1+2XY$, this becomes

$$
\boxed{
\begin{aligned}
H_1&=X-3X^2Y-2X^3Z,\\
H_2&=Y+6XT^2Z+6XY^2(4+6XY),\\
H_3&=T^3Z+Y^2T(4+6XY).
\end{aligned}}
$$

It follows either by conjugation or exact differentiation that

$$
H(0)=0,\qquad dH_0=I_3,\qquad \det JH=1.
$$

Nevertheless,

$$
\begin{aligned}
H(0,0,-1/4)
&=H(1/2,-3/2,13/2)\\
&=H(-1/2,3/2,13/2)=(0,0,-1/4).
\end{aligned}
$$

Thus the counterexample survives the strongest elementary affine
normalization.  Its coordinate degrees, in the displayed output order, are
$(4,6,7)$.

## Why conjugation preserves the conclusion

Both $L$ and $D$ are invertible linear maps.  Pre- and postcomposition by
such maps preserves injectivity and polynomial invertibility.  The determinant
changes by the product of the constant linear determinants; here the choice of
$L^{-1}$ changes $-2$ to $1$, while conjugation by $D$ changes nothing.
