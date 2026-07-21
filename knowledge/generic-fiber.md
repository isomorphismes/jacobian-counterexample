---
title: Binary cubics and the complete fiber description
tags: [binary-cubic, generic-degree, inverse, image]
---

# Binary cubics and the complete fiber description

The map has an explicit three-valued algebraic inverse.  This chapter makes the
projective-root interpretation precise.

Throughout this chapter the base field is $\mathbb C$ (the same arguments
work over any algebraically closed field of characteristic zero).

## Finite roots

For a target $(a,b,c)$, dehomogenize its binary cubic at $V=1$:

$$
p_{a,b,c}(w)=cw^3-2w^2+bw-2a.
$$

Every preimage with $x\ne0$ has

$$
w=y+\frac1x,\qquad p_{a,b,c}(w)=0,\qquad
p'_{a,b,c}(w)=\frac2x.
$$

Conversely, let $w$ be any simple root and put

$$
h=\frac{p'_{a,b,c}(w)}2.
$$

Then $h\ne0$, and the unique corresponding preimage is

$$
\boxed{
x=\frac1h,\qquad
y=w-h,\qquad
z=5h^2-3wh-ch^3.}
$$

Substitution into the rational identities of the previous chapter returns
$(A,B,C)=(a,b,c)$.

## The root at infinity

The projective point $[U:V]=[1:0]$ is a root precisely when $c=0$.
It is always simple because $Q_V(1,0)=-2$.  Its corresponding source point
is

$$
\boxed{(x,y,z)=(0,b,a-4b^2).}
$$

Indeed, $F(0,y,z)=(z+4y^2,y,0)$.

## Why every simple projective root gives one point

At any simple root $[u_0:v_0]$, Euler's identity for the homogeneous cubic
implies that its gradient is a nonzero scalar multiple of
$(v_0,-u_0)$.  There is a unique rescaling $(U,V)=s(u_0,v_0)$ for which

$$
Q_U(U,V)=2V,\qquad Q_V(U,V)=-2U.
$$

When $V\ne0$, the preceding affine formula reconstructs $(x,y,z)$.
When $V=0$, the explicit infinity formula does.  This is inverse to the
marked-root construction from the source.

More precisely, let

$$
I^{\mathrm{sm}}=
\{(a,b,c,[U:V]):Q_{a,b,c}(U,V)=0, [U:V]\text{ is simple}\}.
$$

Then

$$
\mathbb A^3\longrightarrow I^{\mathrm{sm}},\qquad
(x,y,z)\longmapsto(F(x,y,z),[1+xy:x])
$$

is an isomorphism, not merely a bijection on complex points.  The finite-root
formula gives its regular inverse on $V\ne0$.  On $U\ne0$, put

$$
s=V/U,\qquad k=1-bs+3as^2.
$$

Simplicity is exactly $k\ne0$, and a regular inverse on this chart is

$$
\boxed{
x=\frac{s}{k},\qquad
y=b-3as,\qquad
z=ak^3-y^2k(k+3).}
$$

At $s=0$ this reduces to the root-at-infinity formula.

## Fiber cardinalities and image

A nonzero binary cubic over $\mathbb C$ has one of three root patterns:

- three simple projective roots;
- one double root and one simple root;
- one triple root.

Only simple roots produce source points.  Therefore the corresponding fiber
cardinalities are exactly $3$, $1$, and $0$.

The triple-root cubics are parametrized by

$$
\boxed{
(a,b,c)=\left(\frac{\rho^2}{3}, 2\rho, \frac{2}{3\rho}\right),
\qquad \rho\ne0.}
$$

Consequently the set-theoretic image on complex points is

$$
F(\mathbb A^3(\mathbb C))
=\mathbb A^3\setminus
\left\{\left(\frac{\rho^2}{3},2\rho,\frac{2}{3\rho}\right):
\rho\in\mathbb C^*\right\}.
$$

Because $F$ is dominant, its scheme-theoretic image—and the Zariski closure
of its point-set image—is still all of $\mathbb A^3$.  The omitted curve is
also the reduced singular locus of the discriminant hypersurface.

For example $(1/3,2,2/3)$ is omitted because

$$
p(w)=\frac23(w-1)^3.
$$

Independently, a Gröbner basis gives

$$
(F_1-1/3,F_2-2,F_3-2/3)=(1).
$$

## Generic degree and monodromy

The generic cubic has three distinct roots, so the map has geometric and
function-field degree $3$:

$$
[\mathbb C(x,y,z):\mathbb C(F_1,F_2,F_3)]=3.
$$

There is also a direct function-field proof.  Over
$k=\mathbb C(b,c)$, solve the root equation for the remaining coefficient:

$$
a=h(w)=\frac{cw^3-2w^2+bw}{2}.
$$

The rational map $h:\mathbb P^1\to\mathbb P^1$ has degree three, so

$$
[k(w):k(h(w))]=3.
$$

The inverse formulas show that $w$ generates the full source function field
over $\mathbb C(a,b,c)$; hence its cubic is the minimal polynomial and the
map has geometric degree three.

The discriminant factor $\Delta$ is not a square.  Viewed as a quadratic in
$a$, its own discriminant is

$$
-4(3bc-4)^3,
$$

which is nonsquare in $\mathbb C(b,c)$.  Thus $\Delta$ is irreducible and
has odd valuation along its divisor.  The degree-three extension is generically
nonnormal (and has trivial automorphism group), while its degree-six normal
closure—and the geometric monodromy—has group $S_3$.

“Generically three-to-one” is the correct phrase.  The exact fiber sizes vary
on the discriminant and omitted loci.
