---
title: The exact three-point fiber
tags: [groebner-basis, fiber, scheme]
---

# The exact three-point fiber

Substitution proves that at least three points lie over
$q=(-1/4,0,0)$.  A Gröbner basis proves that there are no others and that no
hidden multiplicities occur.

In $\mathbb Q[x,y,z]$, exact ideal reduction gives

$$
\boxed{
\left(F_1+\frac14,F_2,F_3\right)
=\left(z-\frac{27}{4}x^2+\frac14,
        y+\frac32x,
        x^3-x\right).}
$$

The quotient has $\mathbb Q$-basis $1,x,x^2$, so the fiber scheme has
length three.  Since

$$
x^3-x=x(x-1)(x+1)
$$

has distinct roots in characteristic zero, the quotient is reduced.  Solving
the triangular basis gives exactly

$$
(0,0,-1/4),\quad(1,-3/2,13/2),\quad(-1,3/2,13/2).
$$

## A direct proof without Gröbner bases

Put $u=1+xy$ and

$$
r=2-3xy-x^2z,
$$

so $F_3=xr$.  If $F_3=0$, there are two cases.

If $x=0$, then $F_2=y$ and $F_1=z+4y^2$.  The target forces
$y=0,z=-1/4$.

If $x\ne0$, then $r=0$.  In the weighted form one has

$$
F_2=\frac{4u+2}{x},\qquad
F_1=\frac{u(u+1)}{x^2}.
$$

The target forces $u=-1/2$, followed by $x^2=1$.  Then
$y=(u-1)/x$ and $z=(2-3xy)/x^2$, producing precisely the two remaining
points.

The Magma file
[`03_fiber_certificate.m`](../artifacts/magma/03_fiber_certificate.m) verifies
ideal equality, zero-dimensionality, and radicality directly.
