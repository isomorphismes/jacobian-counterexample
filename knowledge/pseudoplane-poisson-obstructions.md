---
title: Exact Poisson obstructions on the exceptional pseudo-plane
tags: [dimension-two, poisson, pseudo-plane, darboux, no-go]
---

# Exact Poisson obstructions on the exceptional pseudo-plane

Consider

$$
T=\operatorname{Spec}R,
\qquad
R=\mathbb C[a,b,c]/(b^2-a-a^2c)
$$

with the Poisson bracket induced by the scaffold
$a=x^2$, $b=x(1+x^2y)$, $c=2y+x^2y^2$:

$$
\{a,b\}=2a^2,
\qquad \{a,c\}=4b,
\qquad \{b,c\}=2+4ac.
$$

A pair $U,V\in R$ satisfying $\{U,V\}=1$ would pull back to a
noninjective plane Keller map.  No such pair is produced here.  This note
proves several exact no-go theorems which sharply constrain where one could
occur.  Every finite polynomial calculation is independently checked by
[`certify_pseudoplane_poisson.py`](../research/n2/certify_pseudoplane_poisson.py).

## 1. Global symplectic form and two Darboux charts

Put $F=b^2-a-a^2c$.  The bracket is the hypersurface Jacobian bracket

$$
\{f,g\}=-2\det\frac{\partial(F,f,g)}{\partial(a,b,c)},
$$

and its nowhere-vanishing two-form is

$$
\omega=-\frac12\operatorname{Res}_T
 \frac{da\wedge db\wedge dc}{F}.
$$

There are two particularly simple rational Darboux charts.  On $D(a)$ set

$$
p=-\frac1{2a},\qquad q=b.
$$

Then $\{p,q\}=1$ and

$$
c=2p+4p^2q^2.
$$

On $D(1+ac)$ set

$$
P=\frac b2,
\qquad Q=\frac{c}{1+ac}.
$$

Again $\{P,Q\}=1$, and

$$
a=\frac{4P^2}{1+4P^2Q},\qquad
b=2P,\qquad
c=Q(1+4P^2Q).
$$

The two opens cover $T$.  Their overlap has $q\ne0$ and transition

$$
\boxed{P=\frac q2,\qquad Q=-2p-q^{-2}.}
$$

This transition is symplectic.  The term $q^{-2}$ is the global obstruction
seen by all of the elementary Darboux attempts below: local coordinates are
easy, but a local mate regular on one component of $b=0$ develops a pole on
the other.

## 2. The two components of $b=0$

Let

$$
D_0=\{a=b=0\},
\qquad
D_\infty=\{b=0,\ 1+ac=0\}.
$$

Then

$$
\operatorname{div}(a)=2D_0,
\quad
\operatorname{div}(b)=D_0+D_\infty,
\quad
\operatorname{div}(1+ac)=2D_\infty.
$$

Near $D_0$, $(b,c)$ are regular coordinates and

$$
a=b^2-cb^4+2c^2b^6-5c^3b^8+\cdots,
\qquad
1+2ac=\sqrt{1+4b^2c}.
$$

Consequently

$$
\{f,g\}=2(1+2ac)(f_b g_c-f_c g_b).
$$

Writing $U=U_0(c)+bU_1(c)+O(b^2)$ and similarly for $V$, a necessary
first-jet condition is

$$
\boxed{2\bigl(U_1V_0'-U_0'V_1\bigr)=1.}
$$

Thus the divisor itself causes no local obstruction.  The obstruction is the
incompatibility of regularity at both $D_0$ and $D_\infty$.

## 3. None of the generators has a polynomial mate

On $D(a)$ the ring is $\mathbb C[a^{\pm1},b]$ and

$$
\{a,-\}=2a^2\partial_b,
\qquad
\{b,-\}=-2a^2\partial_a.
$$

If $\{a,V\}=1$, integration in the function field gives

$$
V=\frac{b}{2a^2}+h(a).
$$

Along $D_0$, the first term has valuation $1-4=-3$, while every term in
$h(a)$ has even valuation.  It cannot be regular.

If $\{b,V\}=1$, then

$$
V=\frac1{2a}+h(b).
$$

Regularity at $D_\infty$, where $a$ is a unit and $b=0$, forbids a pole of
$h$ at $b=0$.  In the second Darboux chart the same expression is

$$
V=\frac Q2+\frac1{8P^2}+h(2P),
$$

which cannot then be regular at $D_0$, where $P=0$.  This proves the all-degree
no-go for $b$ without a bounded ansatz.

For $c$, work over $K=\mathbb C(c)$ and put

$$
s=1+2ac,\qquad z=s+2\sqrt c\,b.
$$

The relation gives $s^2-4cb^2=1$, so
$K(\sqrt c)(T)=K(\sqrt c)(z)$, while

$$
\{c,z\}=-4\sqrt c\,z.
$$

The equation $\{c,V\}=1$ would therefore require a rational antiderivative
of $dz/z$.  This is impossible: $dz/z$ has nonzero residues, whereas an exact
rational differential has zero residues.  Hence $c$ has no rational mate,
and a fortiori no polynomial mate.

## 4. No homogeneous Darboux pair

The hyperbolic $\mathbb C^*$-action has weights

$$
\operatorname{wt}(a,b,c)=(2,1,-2),
$$

and the Poisson bracket has degree $+1$.  Put $t=ac$.  Since
$R=\mathbb C[a,c]\oplus b\mathbb C[a,c]$, its homogeneous pieces are explicit:

$$
R_{2k}=
\begin{cases}
a^k\mathbb C[t],&k\ge0,\\
c^{-k}\mathbb C[t],&k<0,
\end{cases}
\qquad
R_{2k+1}=bR_{2k}.
$$

If homogeneous $U,V$ have constant bracket, their weights sum to $-1$; one
is even and the other odd.  Up to swapping the pair, for $k\ge0$ write

$$
U=a^kP(t),\qquad V=bc^{k+1}Q(t).
$$

Direct differentiation gives

$$
\begin{aligned}
\{U,V\}=2t^k\bigl(&k(2(k+1)+(2k+3)t)PQ\\
 &+(2k+1)t(1+t)P'Q+2kt(1+t)PQ'\bigr).
\end{aligned}
$$

For $k\ge1$ this is divisible by $t$.  For $k=0$ it is
$2t(1+t)P'Q$.  Neither can be a nonzero constant.

For the negative weights put $k=-h$, $h\ge1$, and write

$$
U=c^hP(t),\qquad V=ba^{h-1}Q(t).
$$

Then

$$
\begin{aligned}
\{U,V\}=-2t^{h-1}\bigl(&h((2h-1)+2ht)PQ\\
 &+(2h-1)t(1+t)P'Q+2ht(1+t)PQ'\bigr).
\end{aligned}
$$

The factor $t^{h-1}$ excludes $h\ge2$.  At $h=1$ this becomes

$$
\{U,V\}=-\frac2Q\frac d{dt}\bigl(t(1+t)PQ^2\bigr).
$$

If it were $1$, then

$$
\frac d{dt}\bigl(t(1+t)PQ^2\bigr)=-\frac12Q.
$$

For nonzero polynomials $P,Q$, the two sides have degrees
$\deg P+2\deg Q+1$ and $\deg Q$, respectively, a contradiction.  Therefore

$$
\boxed{\begin{gathered}
\text{There is no }\mathbb C^*\text{-homogeneous pair }U,V\text{ with}\\
\{U,V\}=1.
\end{gathered}}
$$

## 5. No pair of ambient total degree at most two

This stronger bounded theorem allows both coordinates to be nonhomogeneous.
Modulo $b^2=a+a^2c$, the images of ambient polynomials of total degree at most
two have nonconstant basis

$$
a,b,c,a^2,ab,ac,bc,c^2,a^2c.
$$

The constant coefficient of $\{U,V\}=1$ says that the determinant of the
linear $(b,c)$-coefficient matrix is $1/2$.  An $\mathrm{SL}_2$ change of
target coordinates therefore reduces the general pair to

$$
\begin{aligned}
U={}&\frac b2+Aa+Da^2+Eab+Fac+Gbc+Hc^2+Ia^2c,\\
V={}&c+A'a+D'a^2+E'ab+F'ac+G'bc+H'c^2+I'a^2c.
\end{aligned}
$$

For coefficient-pairs $X=(X,X')$, put
$\Delta(X,Y)=XY'-X'Y$.  Comparing coefficients in $\{U,V\}-1$ gives,
among others,

$$
8\Delta(E,H)+\Delta(F,G)=0,
\qquad
6\Delta(E,H)+\Delta(F,G)+1=0.
$$

Hence $\Delta(E,H)=1/2$, so $E,H$ are independent.  The equations

$$
\Delta(E,I)=\Delta(H,I)=0
$$

force $I=0$.  Next

$$
10\Delta(E,G)-4\Delta(F,I)=0,
\qquad \Delta(G,H)=0
$$

force $G=0$.  The remaining equations successively give

$$
H'=0,\quad A=0,\quad E=F'=0,\quad -E'H=\frac12,\quad D=0,
$$

then

$$
F=2A'H,\qquad A'F=0,\qquad A'=F=0,\qquad E'=0,
$$

contradicting $-E'H=1/2$.  Thus

$$
\boxed{\text{No two ambient quadratics have Poisson bracket }1\text{ in }R.}
$$

The exact coefficient ideal has 23 generators in 14 unknowns after the
normalization above; SymPy computes its reduced Groebner basis as $[1]$.
This is notably stronger than the earlier linear no-go.  It is also sharp in
a different direction: the identity

$$
1=\frac12\{b,c\}+\frac12\{ab,c^2\}-4\{ac,bc\}
$$

expresses $1$ as a **sum** of three brackets of quadratics, but this section
proves that it cannot be compressed into one quadratic bracket.

## 6. Locally nilpotent and self-similar directions

The Hamiltonian derivation

$$
\delta=\frac12\{a,-\}
=a^2\partial_b+2b\partial_c
$$

is locally nilpotent, with flow

$$
(a,b,c)\longmapsto
(a,b+\lambda a^2,c+2\lambda b+\lambda^2a^2).
$$

Its image lies in the proper ideal $(a^2,b)$, so it has no slice.  More
generally, the classification for generalized Danielewski surfaces applies
with $f(a)=a^2$ and $\varphi(a,b)=b^2-a$ {cite}`bianchiveloso2017`; it says

$$
\operatorname{ML}(R)=\mathbb C[a],
\qquad
\operatorname{LND}(R)=\{f(a)\delta:f\in\mathbb C[a]\}.
$$

**External-input flag.**  The displayed classification of *all* locally
nilpotent derivations is Corollary 8 of the cited paper, not a result proved by
the finite certificate script.  The formula for $\delta$, its local
nilpotence, and its lack of a slice are proved directly here and checked
exactly.  None of the generator, homogeneous, or quadratic no-go theorems
depends on the external classification.

Finally, the known nonproper etale self-map is, in $(a,b,c)$ order,

$$
\eta(a,b,c)=\bigl(b^2,b(1+2ac),4c\bigr).
$$

It is conformally Poisson with factor four:

$$
\{\eta^*f,\eta^*g\}=4\eta^*\{f,g\}.
$$

For $t=ac$ and $s=1+2t$ it induces the Chebyshev dynamics

$$
t\longmapsto4t(1+t),
\qquad
s\longmapsto2s^2-1=T_2(s).
$$

The homogeneous theorem rules out every equivariant Darboux pair.  A viable
construction must therefore be mixed-weight, nontriangular, and globally
compatible with the $q^{-2}$ Darboux transition.  The non-equivariant
deformations of $\eta$ are the most structured remaining source of such
mixed-weight ansatzes.
