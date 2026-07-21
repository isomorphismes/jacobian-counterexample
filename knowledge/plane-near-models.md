---
title: Two exact plane near-models
tags: [dimension-two, quotient, cusp, degree-six, near-counterexample]
---

# Two exact plane near-models

The failed descents are highly structured.  They produce explicit
noninjective plane maps whose Jacobians are powers of a single linear form.
These are useful construction seeds because they isolate the divisor that must
be moved to infinity without introducing poles.

## The equivariant quotient of the threefold map

The canonical map is equivariant for

$$
(x,y,z)\longmapsto(\lambda x,\lambda^{-1}y,\lambda^{-2}z)
$$

and target weights $(-2,-1,1)$.  The invariant rings are polynomial:

$$
\mathbb C[x,y,z]^{\mathbb C^*}=\mathbb C[u,v],
\quad u=xy,\quad v=x^2z,
$$

$$
\mathbb C[A,B,C]^{\mathbb C^*}=\mathbb C[p,q],
\quad p=AC^2,\quad q=BC.
$$

Put

$$
\begin{aligned}
a&=(1+u)^3v+u^2(1+u)(4+3u),\\
b&=u+3(1+u)^2v+3u^2(4+3u),\\
c&=2-3u-v.
\end{aligned}
$$

The descended map is

$$
H(u,v)=(ac^2,bc),
\qquad \boxed{JH=-2c^2}.
$$

It is noninjective:

$$
H(0,0)=H\left(-\frac32,\frac{13}{2}\right)=(0,0).
$$

The square defect is forced by the orbit multiplier $C/x=c$.  It is the
precise trace left by the third coordinate after quotienting.

There is a further factorization.  Set

$$
X=c,\qquad Y=c(u+1).
$$

Then

$$
G(X,Y)=\left(XY+Y^2-Y^3,\ 2X+4Y-3Y^2\right),
$$

$$
\boxed{JG=-2X},\qquad G(0,0)=G(2,2)=(0,0).
$$

So the threefold étale cover becomes an ordinary ramified cubic after two
quotient/blow-down steps.

There is also a sharp valuation obstruction to the most obvious repair.  If a
rational source chart sends the divisor $X=0$ to infinity while both outputs
remain regular, take a boundary valuation with $\nu(X)=-k<0$.  Regularity of

$$
2X+4Y-3Y^2
$$

forces $\nu(Y)=-k/2$ and leading relation $2X=3Y^2$.  Regularity of

$$
XY+Y^2-Y^3
$$

forces instead $X=Y^2$.  The two required cancellations are incompatible.
This explains algebraically why dividing away the factor $X$ reintroduces a
pole.

## The octahedral degree-six cusp model

The first allowed geometric degree admits an equally explicit near-model.  The
polynomials

$$
\begin{aligned}
P(t)&=64t^3-96t^2+30t+1,\\
Q(t)&=16t^2-16t+1
\end{aligned}
$$

satisfy the exact octahedral identity

$$
P(t)^2-Q(t)^3=108t(1-t),
\qquad 2QP'-3Q'P=108.
$$

The associated Belyi passport is

$$
(2^3),\qquad(3^2),\qquad(4,1,1),
$$

with the degree-six octahedral $S_4$-action.  In affine normalization
coordinates $x=s$, $y=st$, define

$$
\begin{aligned}
U&=x^2-16xy+16y^2,\\
V&=x^3+30x^2y-96xy^2+64y^3.
\end{aligned}
$$

Then

$$
\boxed{J(U,V)=108x^3},
$$

and

$$
V^2-U^3=108x^4y(x-y).
$$

The leading forms have no common projective zero, so this map is finite.  Its
generic degree is six: the ratio $t=y/x$ obeys the degree-six equation coming
from $V^2/U^3=P(t)^2/Q(t)^3$.  The line $x=0$ carries the index-four
ramification, while $y=0$ and $y=x$ are the two unramified cusp sheets.

This model matches three independent requirements for a first counterexample:
degree six, non-Galois octahedral monodromy, and $2:3$ cusp geometry.  It fails
only because its ramification divisor is affine.  Borisov's framework explains
why such Belyi and boundary data are natural necessary inputs, not by
themselves constructions of Keller maps {cite}`borisov2020`.

## Why the whole sextic extension is excluded

The finite normalization of $\mathbb C[U,V]$ in its degree-six function field
is

$$
B=\mathbb C[s,st]\cong\mathbb C[x,y].
$$

Suppose some rational parametrization of this same extension produced a plane
Keller pair on another $\mathbb A^2$.  Integral elements $s,st$ would lie in
its integrally closed coordinate ring.  Zariski Main Theorem would factor the
quasi-finite Keller map through an open immersion

$$
\mathbb A^2\hookrightarrow\operatorname{Spec}B\cong\mathbb A^2.
$$

By Ax--Grothendieck that open immersion is surjective.  Hence $(s,st)$ is a
polynomial automorphism.  But

$$
J(s,st)=sJ(s,t)=\text{constant}
$$

would give

$$
J(U,V)=108s^4J(s,t)=\text{constant}\cdot s^3,
$$

not a nonzero constant.  Therefore **no reparametrization of this exact
function-field extension can be a plane Keller counterexample**.

The lesson is constructive: a successful degree-six cover needs a finite
normalization $Y\ne\mathbb A^2$ that contains $\mathbb A^2$ as a proper
open subset.  Its omitted ramification divisor must have a nontrivial class in
$\mathrm{Cl}(Y)$; otherwise deleting it creates a forbidden nonconstant unit
on the source.
