---
title: The map and the claim
tags: [definition, keller-map]
---

# The map and the claim

Let $k$ be a field of characteristic different from $2$.  For the
classical conjecture take $k=\mathbb C$.  Define
$F=(F_1,F_2,F_3):\mathbb A_k^3\to\mathbb A_k^3$ by

$$
\begin{aligned}
F_1&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
F_2&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
F_3&=2x-3x^2y-x^3z.
\end{aligned}
$$

We use

$$
A=F_1,\qquad B=F_2,\qquad C=F_3
$$

when the outputs themselves are being manipulated.  Lower-case
$(a,b,c)$ denotes a fixed target point.

The coordinate degrees are

$$
(\deg F_1,\deg F_2,\deg F_3)=(7,6,4).
$$

## Main theorem

:::{admonition} Theorem — Keller counterexample in dimension three
:class: important
The map $F$ satisfies

$$
\det\left(\frac{\partial(F_1,F_2,F_3)}
                 {\partial(x,y,z)}\right)=-2.
$$

Moreover,

$$
\begin{aligned}
F(0,0,-1/4)
&=F(1,-3/2,13/2)\\
&=F(-1,3/2,13/2)=(-1/4,0,0).
\end{aligned}
$$
:::

The determinant is a nonzero constant, so $F$ is a Keller map and an étale
morphism.  The three inputs are distinct, so $F$ is not injective and cannot
be a polynomial automorphism.  This is exactly a counterexample to the usual
Jacobian conjecture.

No theorem equating injectivity and polynomial invertibility is needed for the
negative conclusion: a map with an inverse of any kind is necessarily
injective.

## Coefficient field

The determinant identity lies in $\mathbb Z[x,y,z]$, and the collision lies
in $\mathbb Z[1/2]$.  The same example therefore works over every field of
odd characteristic.  Characteristic zero is the historically meaningful case;
positive-characteristic analogues were already known to fail for simpler
reasons.
