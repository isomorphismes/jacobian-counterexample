---
title: Structural determinant certificate
tags: [proof, birational-coordinates, binary-cubic]
---

# Structural determinant certificate

This proof is short enough to check by hand.

## Rational coordinate form

Work first on the dense open set $x\ne0$, and put

$$
w=y+\frac1x.
$$

With $A=F_1$, $B=F_2$, and $C=F_3$, direct collection of terms gives

$$
\boxed{
B=4w+\frac2x-3Cw^2,
\qquad
A=w^2+\frac wx-Cw^3.}
$$

The first coordinate change has Jacobian

$$
\det\frac{\partial(x,w,C)}{\partial(x,y,z)}=-x^3,
$$

because $\partial w/\partial y=1$ and
$\partial C/\partial z=-x^3$.  Treating $(x,w,C)$ as independent, the
second change has determinant

$$
\begin{aligned}
\det\frac{\partial(A,B,C)}{\partial(x,w,C)}
&=
\begin{vmatrix}
-w/x^2 & 2w+1/x-3Cw^2\\
-2/x^2&4-6Cw
\end{vmatrix}\\
&=\frac2{x^3}.
\end{aligned}
$$

The chain rule now yields

$$
\det JF=(-x^3)\frac2{x^3}=-2
$$

on $x\ne0$.  Since $\det JF+2$ is a polynomial vanishing on a Zariski
dense open set, it is the zero polynomial.  Thus the identity holds everywhere,
including $x=0$.

## The denominator-free identity

The rational calculation is the affine chart of a global polynomial identity.
For target variables $(a,b,c)$, introduce the binary cubic

$$
Q_{a,b,c}(U,V)
=cU^3-2U^2V+bUV^2-2aV^3.
$$

For the source point set

$$
U=1+xy,\qquad V=x.
$$

Exact expansion in $\mathbb Z[x,y,z]$ gives

$$
\boxed{
Q_{A,B,C}(U,V)=0,\qquad
(Q_{A,B,C})_U(U,V)=2V,\qquad
(Q_{A,B,C})_V(U,V)=-2U.}
$$

Because $U-yV=1$, the pair $(U,V)$ never vanishes.  The last two
identities show that $[U:V]$ is a simple projective root of the cubic.  This
is the reason for the otherwise surprising coefficient cancellations: the map
forgets a marked simple root of a binary cubic.

The three identities are independently asserted in the SymPy notebook and in
the SageMath and Magma artifacts.
