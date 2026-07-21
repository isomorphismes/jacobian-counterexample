---
title: The factorization--resultant route to the plane problem
tags: [dimension-two, resultant, factorization, poisson, search]
---

# The factorization--resultant route to the plane problem

:::{admonition} Verdict
:class: warning
Aaron Lou's 20 July 2026
[derivation](https://aaronlou.com/jacobian_counterexample_derivation.pdf)
reconstructs exactly the same three-dimensional map already audited in this
repository, after one source sign change and reversal of the outputs.  It does
not solve the plane case.  Its factorization viewpoint nevertheless yields two
precise plane programs, one of which contains an explicit noninjective
$\mathbb A^2$ scaffold with the correct infinitary deck behavior.

For provenance, the explicit formula first appeared in Levent Alpöge's
[announcement](https://x.com/__alpoge__/status/2079028340955197566).  Andy
Jiang (@davikrehalt) then posted the
[projective marked-root model](https://x.com/davikrehalt/status/2079175065695035442).
Lou's factor coordinates and this chapter give affine gauges for that same
projective incidence; the exact comparison is recorded in the
[literature audit](literature-audit.md).
:::

Every algebraic identity below is checked independently in
[`verify_resultant_route.py`](../artifacts/sympy/verify_resultant_route.py) and
[`07_resultant_route.m`](../artifacts/magma/07_resultant_route.m).  Topological
and monodromy arguments are stated separately from the computer algebra.
The detailed valuation, homogeneous-weight, and quadratic Poisson no-go proofs
are collected in [Exact Poisson obstructions on the exceptional
pseudo-plane](pseudoplane-poisson-obstructions.md).

## 1. What the PDF actually constructs

Write the canonical map in this repository as $F=(A,B,C)$.  Define

$$
S(x,y,z)=(x,y,-z),\qquad R(A,B,C)=(C,B,A).
$$

If $G$ denotes the map in Lou's equation (13), exact expansion gives

$$
\boxed{G=R\circ F\circ S.}
$$

Thus the maps are exactly left--right linearly equivalent: this is an
isomorphism of source--target arrows, not strict conjugacy.  The note is a
conceptually valuable derivation of the same example, not a second family.  Its cubic

$$
\frac{G_1}{2}t^3+t^2+\frac{G_2}{2}t+G_3
$$

is $-\tfrac12$ times the marked binary cubic of $F\circ S$ after $t\mapsto-t$.
The collision $(0,2,0)$ in the PDF is a different fiber of the same map.

The construction starts with

$$
L(t)=xt+\beta,\qquad Q(t)=\gamma t^2+\delta t+\epsilon
$$

and records the four coefficients of $LQ$ together with

$$
\rho=\operatorname{Res}(L,Q)
     =x^2\epsilon-x\beta\delta+\beta^2\gamma.
$$

The decisive identity is

$$
\det\frac{\partial(c_3,c_2,c_1,c_0,\rho)}
{\partial(x,\beta,\gamma,\delta,\epsilon)}=-\rho^2.
$$

On the slice $c_2=\rho=1$, Lou gives the polynomial chart

$$
\begin{aligned}
\beta&=1+xy,\\
\gamma&=\frac{2-3xy+x^2z}{2},\\
\delta&=-\frac{xz-y+x^2yz-3xy^2}{2},\\
\epsilon&=-z(1+xy)^2+4y^2+3xy^3,
\end{aligned}
$$

with polynomial inverse

$$
y=2\beta\delta-x\epsilon,
\qquad
z=4y\delta+2\gamma y^2-\epsilon.
$$

This is the exceptional step: a normalized factor space becomes affine
three-space without deleting a principal divisor.

## 2. The general coefficient--resultant identity

Let $P,Q$ have degrees $r,s$, with every coefficient variable retained.  Let
$c_{r+s},\ldots,c_0$ be the coefficients of $PQ$, and let
$\rho=\operatorname{Res}(P,Q)$.  Up to the sign fixed by coefficient ordering,

$$
\boxed{
\det\frac{\partial(c_{r+s},\ldots,c_0,\rho)}
{\partial(\operatorname{coeff}P,\operatorname{coeff}Q)}
=\pm(s-r)\rho^2.}
$$

Here is a proof on the dense simple-root locus.  Put

$$
P=a\prod_{i=1}^{r}(t-\alpha_i),\qquad
Q=b\prod_{j=1}^{s}(t-\beta_j),
$$

and let $D=\prod_{i,j}(\alpha_i-\beta_j)$.  Then
$\rho=a^s b^rD$.  The coefficient/root Jacobians are Vandermonde
determinants:

$$
J_P=\pm a^rV(\alpha),\quad
J_Q=\pm b^sV(\beta),\quad
J_{PQ}=\pm(ab)^{r+s}V(\alpha,\beta).
$$

Holding all roots fixed, the determinant of
$(a,b)\mapsto(ab,\rho)$ is $(r-s)\rho$.  Finally,

$$
V(\alpha,\beta)=\pm V(\alpha)V(\beta)D.
$$

Dividing the output root-coordinate Jacobian by $J_PJ_Q$ leaves
$\pm(s-r)\rho^2$.  Both sides are polynomials, so the identity extends across
the complement of the simple-root locus.

Two immediate consequences organize the search.

1. The determinant vanishes identically for equal factor degrees.
2. Under $(P,Q)\mapsto(\lambda P,\lambda^{-1}Q)$, the resultant has weight
   $s-r$.  On $\rho=1$, a generic product has

   $$
   |s-r|\binom{r+s}{r}
   $$

   normalized ordered factorizations.

The low-degree cases are therefore:

| split | resultant weight | generic normalized degree | interpretation |
|---|---:|---:|---|
| $1+1$ | $0$ | degenerate | literal plane analogue fails |
| $1+2$ | $1$ | $3$ | Lou's threefold construction |
| $1+3$ | $2$ | $8$ | residual $\mu_2$ gauge |
| $2+2$ | $0$ | degenerate globally | useful restricted scaffold below |
| $2+3$ | $1$ | $10$ | cleanest direct plane blueprint |
| $1+5$ | $4$ | $24$ | residual $\mu_4$ gauge |
| $2+4$ | $2$ | $30$ | residual $\mu_2$ gauge |
| $3+3$ | $0$ | degenerate | residual $\mathbb G_m$ gauge |

The residual finite gauges are not cosmetic.  A connected invariant slice
isomorphic to $\mathbb A^2$ cannot carry a free $\mu_k$ action: compactly
supported Euler characteristic would give $1=k\chi_c(X/\mu_k)$.  Equivalently,
a $\mu_k$-torsor over $\mathbb A^2$ splits.  This is why the consecutive split
$2+3$, whose weight is one, is substantially cleaner than a sextic split.

## 3. Why the literal two-dimensional copy collapses

Take two linear factors in monic form,

$$
P=t+\beta,\qquad Q=\gamma t+\delta,
\qquad \rho=\delta-\beta\gamma=1.
$$

Then $\delta=1+\beta\gamma$, and the product coefficients are

$$
c_2=\gamma,\qquad
c_1=1+2\beta\gamma,\qquad
c_0=\beta+\beta^2\gamma.
$$

They satisfy

$$
c_1^2-4c_2c_0=1.
$$

The map $(\beta,\gamma)\mapsto(c_2,c_1,c_0)$ identifies $\mathbb A^2$ with
the open subset of this smooth quadric obtained by deleting

$$
\{c_2=0,c_1=-1\}.
$$

Indeed

$$
\beta=\frac{c_1-1}{2c_2}\quad(c_2\ne0),
\qquad
\beta=\frac{2c_0}{c_1+1}\quad(c_1\ne-1).
$$

There is only one factor sheet in this affine chart.  Equal factor degrees also
make the augmented determinant zero, exactly as the general identity predicts.

## 4. The clean $2+3$ blueprint and its first failures

For a quadratic and a cubic, the resultant-one hypersurface maps étale to the
six-dimensional quintic coefficient space.  Fixing four product coefficients
leaves a surface; the other two coefficients automatically form an étale map
to $\mathbb A^2$.  If a connected inverse surface were $\mathbb A^2$ and
contained two factor choices of one product, it would be a degree-ten plane
counterexample.  Degree ten is compatible with the established geometric
degree lower bound six, although any actual coordinate degrees must also pass
the much stronger known restrictions in [the plane status audit](plane-status.md).

### 4.1 The Bring--Jerrard plane is not affine two-space

Fix the top four coefficients so that

$$
PQ=t^5+at+b.
$$

Let $Y$ be the resultant-one factor surface and
$\pi:Y\to\mathbb A^2_{a,b}$.  Its discriminant is the irreducible unibranch
cusp

$$
D:\quad256a^5+3125b^4=0,
$$

normalized by $(a,b)=(-5s^4,4s^5)$.  Hence
$\chi_c(D)=1$, $\chi_c(D\setminus\{0\})=0$, and
$\chi_c(\mathbb A^2\setminus D)=0$.

The factor counts are exact:

- off $D$, choosing two of five simple roots gives $10$ points;
- on $D\setminus\{0\}$, the double-root block lies wholly in one factor,
  giving $1+\binom32=4$ points;
- above $(0,0)$, every $2+3$ split of $t^5$ has a common root, so the
  resultant-one fiber is empty.

Therefore

$$
\boxed{\chi_c(Y)=10\cdot0+4\cdot0+0=0.}
$$

This is not cancellation between components.  The root cover is connected;
its local monodromies are transpositions and act transitively, hence generate
$S_5$.  The induced action on two-element subsets is transitive.  Since $\pi$
is étale and open, $Y$ is connected and smooth.  Thus the sole component is
not $\mathbb A^2$.

### 4.2 A unit obstruction for the top-coefficient family

Use Euclidean coordinates

$$
A_0=t^2+pt+q,\qquad
B_0=(mt+n)A_0+(rt+s).
$$

Then

$$
N=\operatorname{Res}(A_0,B_0)=s^2-prs+qr^2.
$$

Because the resultant weight is one, the unique normalization is
$A=N^{-1}A_0$, $B=NB_0$.  Fix

$$
(c_5,c_4,c_3,c_2)=(M,A,B,C).
$$

Successive coefficient elimination gives

$$
\begin{aligned}
n&=A-2Mp,\\
r&=B-2Ap+3Mp^2-2Mq,\\
s&=C+Ap^2-2Aq-Bp-Mp^3+4Mpq.
\end{aligned}
$$

If the resulting normalized surface were $\mathbb A^2$ in this monic chart,
$N$ would be a nonzero constant because $N^{-1}$ is a regular unit.  But its
successive coefficients give

$$
[q^3]N=4M^2,\qquad
[q^2]N|_{M=0}=4A^2,\qquad
[p^2]N|_{M=A=0}=2B^2.
$$

Thus $M=A=B=0$ and $N=C^2$; the product has degree at most two.  No genuine
quintic survives.  A similar exact calculation for the middle four
coefficients also forces every fixed coefficient and the putative constant
resultant to vanish.

This identifies an important design rule: a successful $2+3$ surface must
cross the divisor where the marked quadratic loses its leading term.  Lou's
threefold chart succeeds for precisely the analogous reason—it cancels the
apparent denominator at $x=0$ rather than remaining in a monic localization.

### 4.3 Cusp near-misses

Two sparse coefficient surfaces get very close to the desired geometry:

$$
Pt^5+Qt^4+1,\qquad \operatorname{Disc}=3125P^4+256Q^5,
$$

and

$$
t(Pt^4+Qt^3+1),\qquad \operatorname{Disc}=256P^3-27Q^4.
$$

Their normalized factor surfaces retain an unavoidable nonconstant unit—the
constant coefficient of the quadratic factor—so no component is
$\mathbb A^2$.  The second family is especially suggestive: it has the desired
one-place $(3,4)$ cusp and six marked-factor sheets.  The repair would have to
force that leading coefficient to a constant through a nonlinear coefficient
surface while letting the complementary factor escape across a boundary.

## 5. An explicit noninjective $\mathbb A^2$ scaffold

There is a different construction in which the source problem is solved and
the target-coordinate problem remains.

Take two ordered quadratics

$$
P=t^2+bt+c,\qquad Q=t^2-bt+f,
\qquad u=c-f,\quad v=c+f.
$$

Their resultant is

$$
\operatorname{Res}(P,Q)=u^2+2b^2v.
$$

On the smooth Danielewski surface

$$
S:\quad u^2+2b^2v=1,
$$

delete the line $L_-={b=0,u=-1}$.  The complement is exactly
$\mathbb A^2_{x,y}$ via

$$
b=x,\qquad
u=1+x^2y,\qquad
v=-y-\frac{x^2y^2}{2}.
$$

The inverse is polynomial on the two standard pieces:

$$
y=\frac{u-1}{b^2}\quad(b\ne0),
\qquad
y=-\frac{2v}{u+1}\quad(u+1\ne0).
$$

There is a simpler intermediate target than the product coefficients.  Put

$$
a=x^2,\qquad
\mathcal B=x(1+x^2y),\qquad
\mathcal C=2y+x^2y^2.
$$

These polynomial functions satisfy

$$
T:\quad \mathcal B^2=a+a^2\mathcal C.
$$

### 5.1 The scaffold is the exceptional affine pseudo-plane

The geometry above has a classical name.  On the resultant-one factor surface
make the change of coordinates

$$
X=b,\qquad Y=-2v,\qquad Z=u.
$$

Its equation becomes the Danielewski surface

$$
\widetilde T:\quad X^2Y=Z^2-1.
$$

The displayed affine-plane chart is precisely the open embedding

$$
\kappa:\mathbb A^2\hookrightarrow\widetilde T,\qquad
(x,y)\longmapsto
(X,Y,Z)=\left(x,\,2y+x^2y^2,\,1+x^2y\right),
$$

whose complement is the line

$$
L_-=\{X=0,Z=-1\}.
$$

The two inverse formulas are

$$
y=\frac{Z-1}{X^2}\quad(X\ne0),
\qquad
y=\frac{Y}{Z+1}\quad(Z\ne-1).
$$

The factor-swap involution is

$$
\sigma(X,Y,Z)=(-X,Y,-Z),
$$

and its invariant quotient is exactly

$$
\pi:\widetilde T\longrightarrow T,\qquad
(X,Y,Z)\longmapsto(a,\mathcal B,\mathcal C)=(X^2,XZ,Y).
$$

Thus the noninjective map found above is not an accidental parameterization:

$$
\boxed{\Phi=(a,\mathcal B,\mathcal C)=\pi\circ\kappa.}
$$

It is surjective, with two points over $a\ne0$ and one point over the line
$a=\mathcal B=0$.  The second sheet escapes through $L_-$ as $a\to0$.
The rational involution $\tau$ below is simply
$\kappa^{-1}\sigma\kappa$ wherever both sides are defined.

After renaming $(u,v,w)=(a,\mathcal C,\mathcal B)$, the target equation is

$$
u(1+uv)=w^2.
$$

This is the affine pseudo-plane $S(2,2,1)$ studied in the affine
pseudo-covering program {cite}`miyanishi2005,miyanishi2015lectures`.
It is $\mathbb Q$-acyclic, has fundamental group $\mathbb Z/2$, and
$\Phi:\mathbb A^2\to T$ is its standard degree-two Galois affine
pseudo-covering.  In fact, Miyanishi introduced this framework by asking how a
hypothetical plane Keller map could split as

$$
\mathbb A^2\xrightarrow{\ \Phi\ }T
\xrightarrow{\ h\ }\mathbb A^2.
$$

The identification is still useful because it lands in the exceptional case.
For a pseudo-plane of type $(d,n,r)$, the canonical class is
$(r-2)F_0$ in $\operatorname{Pic}(T)\cong\mathbb Z/d$.  An etale map to
$\mathbb A^2$ forces this class to vanish.  Our surface has $d=r=2$, so the
canonical obstruction vanishes identically.  The current
Borisov--Gabber--Vasiu manuscript explicitly records $r=2$ as the remaining
characteristic-zero case and notes that the plane Jacobian conjecture would
exclude such a map {cite}`borisovgabbervasiu2026`.  Thus this recognition
validates the bottleneck; it does not bypass it.

Dubouloz and Palka proved that $S(2,2,1)$ has large families of nonproper
etale **endomorphisms** {cite}`duboulozpalka2018`.  Their simplest one is

$$
\eta(a,\mathcal B,\mathcal C)
=\bigl(\mathcal B^2,\,
        \mathcal B(1+2a\mathcal C),\,4\mathcal C\bigr).
$$

This is not the missing map $T\to\mathbb A^2$.  Their factorization uses the
open embedding

$$
j:T\hookrightarrow\widetilde T,\qquad
j(a,\mathcal B,\mathcal C)
=\bigl(\mathcal B,4\mathcal C,1+2a\mathcal C\bigr),
\qquad \eta=\pi\circ j.
$$

Trying to land $j(T)$ in our affine-plane chart gives the exact rational
Darboux pair

$$
U=\mathcal B,\qquad
V=\frac{2\mathcal C}{1+a\mathcal C},\qquad
\{U,V\}=4.
$$

On the original plane this is

$$
U=x(1+x^2y),\qquad
V=\frac{2y(2+x^2y)}{(1+x^2y)^2}.
$$

The Jacobian is already the nonzero constant $4$, but $V$ has a genuine pole
on $1+x^2y=0$.  The standard automorphisms $\Theta^P$ of $\widetilde T$
only replace $V$ by

$$
V+P(U)=\frac{2\mathcal C}{1+a\mathcal C}+P(\mathcal B);
$$

the polar divisor survives.  Equivalently, the lifted endomorphism

$$
(X,Y,Z)\longmapsto(XZ,4Y,2Z^2-1)
$$

sends the interior curve $Z=0$ into the omitted line $L_-$.  This isolates a
very sharp new search criterion: find a noninvertible etale endomorphism $E$
of $\widetilde T$ satisfying

$$
E^{-1}(L_-)\subseteq L_-.
$$

Then $\kappa^{-1}E\kappa$ would be a polynomial plane Keller map.  The known
Belyi--Shabat and deformation families fail this boundary-preservation test in
their simplest form.

There is an exact all-degree obstruction behind this pole.  In

$$
A=\mathbb C[a,\mathcal C,\mathcal B]/
(\mathcal B^2-a-a^2\mathcal C)
$$

let $D=\{\mathcal B,-\}$.  After inverting $a$,

$$
A_a=\mathbb C[a^{\pm1},\mathcal B],
\qquad D=-2a^2\frac{\partial}{\partial a}.
$$

If a regular $G\in A$ satisfied $D(G)=c\ne0$, then in the function field

$$
G=\frac{c}{2a}+f(\mathcal B),\qquad f\in\mathbb C(\mathcal B).
$$

Along $D_0=\{a=\mathcal B=0\}$ one has
$\operatorname{ord}_{D_0}(a)=2$ and
$\operatorname{ord}_{D_0}(\mathcal B)=1$, so regularity forces the principal
part $f(\mathcal B)=-c/(2\mathcal B^2)+\cdots$.  Along the other component

$$
D_\infty=\{\mathcal B=0,\ 1+a\mathcal C=0\},
$$

$a$ is a unit, so regularity forces $f$ to have no pole at $\mathcal B=0$.
This is impossible.  Therefore

$$
\boxed{\{\mathcal B,G\}\ne\text{nonzero constant}
       \quad\text{for every }G\in A.}
$$

The rational mate $2\mathcal C/(1+a\mathcal C)$ realizes exactly the forced
tradeoff: it cancels the pole on $D_0$ and acquires it on $D_\infty$.  In
Čech form, the two local mates differ by $2/\mathcal B^2$.  This kills the
entire triangularly sheared Dubouloz--Palka family, not merely a bounded
ansatz.  Similarly, the locally nilpotent Hamiltonian derivation $\{a,-\}$
vanishes on $D_0$, so $a$ cannot have a constant Poisson mate.  Any solution
of the boxed problem below must therefore use a genuinely mixed first
coordinate.

The equivariant family can be excluded just as explicitly.  On
$\widetilde T$, its degree-$d$ members are governed by Chebyshev polynomials:

$$
E_{d,\lambda}(X,Y,Z)=
\left(\lambda^{-1}XU_{d-1}(Z),\lambda^2Y,T_d(Z)\right),
$$

where

$$
T_d(Z)^2-1=(Z^2-1)U_{d-1}(Z)^2,\qquad
T_d'(Z)=dU_{d-1}(Z).
$$

Conjugation by $\kappa$ gives a rational plane map whose second coordinate is

$$
\lambda^2y\,\frac{Z+1}{T_d(Z)+1},
\qquad Z=1+x^2y.
$$

For every $d>1$, $T_d(Z)+1$ has a zero other than the boundary value $Z=-1$,
so a genuine pole remains; $d=1$ is the sole polynomial member.  More
generally, every even-degree equivariant factor
$j_\eta:T\to\widetilde T$ classified by Dubouloz--Palka meets $L_-$, and
their deformation automorphisms preserve $L_-$ setwise.  Hence the full
published equivariant family and its standard high-dimensional deformations
fail the boundary-avoidance condition, not only the degree-two example.

### 5.2 The exact Poisson-coordinate bottleneck

The surface $T$ is smooth, and the source map $\mathbb A^2\to T$ is
everywhere unramified because

$$
\{a,\mathcal B\}=2a^2,\qquad
\{a,\mathcal C\}=4\mathcal B,\qquad
\{\mathcal B,\mathcal C\}=2+4a\mathcal C
$$

have no common zero.  It already has the exact collision

$$
(1,0),\ (-1,-2)\longmapsto(a,\mathcal B,\mathcal C)=(1,1,0).
$$

Consequently the broadest live equation on this scaffold is

$$
\boxed{
\text{Find }U,V\in
\mathbb C[a,\mathcal B,\mathcal C]/
(\mathcal B^2-a-a^2\mathcal C)
\text{ with }\{U,V\}_{x,y}=1.}
$$

Any such pair, pulled back to $\mathbb C[x,y]$, would immediately be a plane
Keller counterexample with the displayed collision.  No linear pair works.
There is, however, a useful exact degree-two identity

$$
1=\frac12\{\mathcal B,\mathcal C\}
 +\frac12\{a\mathcal B,\mathcal C^2\}
 -4\{a\mathcal C,\mathcal B\mathcal C\}.
$$

This is a sum of three brackets, not one bracket; it does not solve the
problem.  It shows that the symplectic form is already exact at low algebraic
complexity, so a de Rham-cohomology obstruction alone cannot finish the route.

The intrinsic form of the bracket is particularly simple.  If

$$
\mathscr F=\mathcal B^2-a-a^2\mathcal C,
$$

then, for ambient representatives,

$$
\{f,g\}=-2\det
\frac{\partial(\mathscr F,f,g)}
     {\partial(a,\mathcal B,\mathcal C)}.
$$

Two algebraic Darboux charts cover $T$.  On $D(a)$ put

$$
p=-\frac1{2a},\qquad q=\mathcal B;
$$

then $\{p,q\}=1$ and
$\mathcal C=2p+4p^2q^2$.  On $D(1+a\mathcal C)$ put

$$
P=\frac{\mathcal B}{2},\qquad
Q=\frac{\mathcal C}{1+a\mathcal C};
$$

then $\{P,Q\}=1$.  On their overlap,

$$
P=\frac q2,\qquad Q=-2p-\frac1{q^2}.
$$

Thus the obstruction is global gluing, represented concretely by the
$q^{-2}$ transition term, rather than a failure of local Darboux coordinates.

Three further exact no-go results substantially narrow the search.

1. **No generator has a mate.**  None of $a,\mathcal B,\mathcal C$ can be one
   member of a regular pair with nonzero constant bracket.  For $a$, integration
   on $D(a)$ forces
   $V=\mathcal B/(2a^2)+h(a)$; the first term has odd valuation $-3$ along
   $D_0$, while every $h(a)$ has even valuation.  The two-divisor argument for
   $\mathcal B$ was given above.  For $\mathcal C$, over
   $\mathbb C(\sqrt{\mathcal C})$ set

   $$
   s=1+2a\mathcal C,\qquad
   z=s+2\sqrt{\mathcal C}\,\mathcal B.
   $$

   Then $s^2-4\mathcal C\mathcal B^2=1$ and
   $\{\mathcal C,z\}=-4\sqrt{\mathcal C}\,z$.  A constant mate would require
   a rational function whose derivative has a nonzero $dz/z$ residue, which
   is impossible.
2. **No homogeneous pair works.**  Give
   $(a,\mathcal B,\mathcal C)$ weights $(2,1,-2)$; the bracket has weight
   $+1$.  A homogeneous candidate pair must have weights summing to $-1$.
   Writing $t=a\mathcal C$, every such pair reduces, up to exchange, to

   $$
   a^kR(t),\quad \mathcal B\mathcal C^{k+1}S(t)
   \quad(k\ge0)
   $$

   or

   $$
   \mathcal C^hR(t),\quad \mathcal B a^{h-1}S(t)
   \quad(h\ge1).
   $$

   Direct expansion is divisible by $t$ except in the last boundary case
   $h=1$, where the equation becomes

   $$
   -\frac2{S(t)}
   \frac d{dt}\bigl[t(1+t)R(t)S(t)^2\bigr]=1.
   $$

   Polynomial degrees make this identity impossible.  Hence every solution
   must break the natural $\mathbb C^*$ symmetry.
3. **Quadratic ambient complexity is impossible.**  Reduce all ambient
   polynomials of total degree at most two modulo
   $\mathscr F$ and impose $\{U,V\}=1$.  Exact coefficient comparison gives
   the unit ideal; an independent Gröbner certificate is included with the
   search artifacts.  Thus a surviving pair must have ambient degree at least
   three.  This does not contradict the three-bracket identity: a sum of
   decomposable bivectors need not itself be decomposable.

The product is the depressed quartic

$$
PQ=t^4+pt^2+qt+r,
$$

where

$$
p=v-b^2,\qquad q=-bu,\qquad r=\frac{v^2-u^2}{4}.
$$

Equivalently,

$$
p=-a-\frac{\mathcal C}{2},\qquad
q=-\mathcal B,\qquad
r=\frac{\mathcal C^2}{16}-\frac{a\mathcal C}{4}-\frac14.
$$

On the affine-plane chart,

$$
\begin{aligned}
p&=-x^2-y-\frac{x^2y^2}{2},\\
q&=-x-x^3y,\\
r&=\frac{(-y-x^2y^2/2)^2-(1+x^2y)^2}{4}.
\end{aligned}
$$

It has the exact collision

$$
\boxed{(1,0),\ (-1,-2)\longmapsto(-1,-1,-1/4).}
$$

The complementary-factor involution becomes

$$
\tau(x,y)=\left(-x,-y-\frac2{x^2}\right),
\qquad \det D\tau=1.
$$

It fixes $p,q,r$ but is not a polynomial automorphism of the chosen plane: it
exchanges the two boundary charts.  This is exactly the desired local picture
for a nonproper plane Keller cover.  The two collision points also have the
same tangent bivector

$$
(J(p,q),J(p,r),J(q,r))=(1,1,1/2),
$$

so the earlier multi-point tangent obstruction does not apply.

The coefficient image is the hypersurface $H=0$, where

$$
\begin{aligned}
H={}&-16p^4r+4p^3q^2+128p^2r^2+p^2-144pq^2r\\
   &+27q^4-256r^3+12r-1.
\end{aligned}
$$

Its singular locus is the elliptic curve

$$
2p^2+24r-3=0,
\qquad
27q^2=-p(8p^2-9).
$$

The smooth surface $T$ is the normalization of $H$ in this marked-partition
function field.  Indeed $a$ is integral over the coefficient ring and, away
from the elliptic conductor, is recovered rationally by

$$
a=\frac{-2p^3+8pr+2p-9q^2}{2p^2+24r-3}.
$$

No two linear forms in $p,q,r$ have constant nonzero bracket.  Exact rational
linear algebra also shows that $1$ is absent from the linear span of all
brackets of target degree at most three; the ranks are

$$
(3,4),\quad(25,26),\quad(77,78)
$$

for the bracket matrix and its constant-augmented matrix.  These are bounded
negative searches only.

The product-invariant version of the remaining problem is therefore:

$$
\boxed{
\text{Find }U,V\in\mathbb C[p,q,r]/(H)
\text{ such that }
\{U,V\}_{x,y}=1.}
$$

Such a pair would retain the displayed collision and would be a counterexample
to the plane Jacobian conjecture.  It is a narrower subproblem of the boxed
equation on $T$ above.  Conversely, failure of the broader Poisson equation for
structural reasons would close a substantial new construction class.

## 6. The newer weighted-lift family and the missing plane chart

A same-day, unrefereed follow-on
[research note](https://github.com/algal/jacobianfun/blob/main/RESEARCH.md)
generalizes the threefold example to arbitrary generic fiber degree.  Its
two-variable core has

$$
P=c\gamma+p(w),\qquad Q=w\gamma+q(w),
\qquad q'(w)=\frac{w p'(w)}{c}.
$$

Then

$$
\det\frac{\partial(P,Q)}{\partial(w,\gamma)}=-c\gamma.
$$

To turn this into a plane Keller map one would need a rational chart
$(x,y)\mapsto(w,\gamma)$ satisfying

$$
\gamma J(w,\gamma)=\text{nonzero constant}
$$

while keeping both $P$ and $Q$ polynomial.  The log-symplectic chart

$$
\gamma=x,\qquad w=\frac yx
$$

cancels the Jacobian defect perfectly, but $p(y/x)$ and $q(y/x)$ have poles.
The threefold lift has a third weighted scale that cancels those poles; the
plane does not.  This is the exact dimension gap in that entire family, not an
accident of the first cubic.

The linked note and code were published on the same day as the announcement
and are not peer-reviewed literature.  Their exact examples pass the supplied
symbolic verifier, but their role here is as construction data, not external
authority.

## 7. Current attack queue

1. **Exceptional pseudo-plane Poisson attack.**  First solve or obstruct the Darboux
   equation on the smooth surface
   $\mathcal B^2=a+a^2\mathcal C$; then impose descent to the smaller product
   ring along the elliptic conductor.  The exact three-bracket identity shows
   that cohomology alone is insufficient, so the next tools are valuations,
   the $\mathbb C^*$ grading, locally nilpotent derivations, and higher-jet
   compatibility across the two conductor branches.
2. **Boundary-preserving lift.**  Impose $E^{-1}(L_-)\subseteq L_-$ on the
   Dubouloz--Palka Belyi--Shabat formulas and their deformations.  The first
   degree-two family gives the rational constant-Jacobian pair above but has an
   unavoidable pole.  A higher-degree map satisfying the divisor condition
   would restrict to a plane counterexample.
3. **Boundary-crossing $2+3$ slices.**  Search nonlinear coefficient surfaces
   that cross the quadratic-leading-coefficient divisor.  Fixed top and middle
   affine coefficient planes cannot work in one monic chart.
4. **Arithmetic sieve before geometry.**  Count normalized coprime
   factorizations over small finite fields.  The executable
   [`search_resultant_poisson.py`](../research/n2/search_resultant_poisson.py)
   rejects all ten zero-centered sparse monic-quintic coordinate planes at the
   first tested primes as literal $\mathbb A^2$ models.  This is a heuristic
   sieve, not a characteristic-zero proof.
5. **Respect the degree frontier.**  Any resulting pair must be tested against
   the established geometric-degree lower bound and the provisional
   coordinate-degree-$108$ frontier {cite}`guccione2022` before a large
   symbolic expression is mistaken for a viable candidate.

The honest status is therefore stronger than “no result,” but weaker than
“close to a proof”: the PDF exposes a universal determinant mechanism, the
most obvious degree-ten surfaces are now exactly excluded, and one explicit
noninjective affine-plane scaffold survives with a single sharply formulated
Poisson-coordinate bottleneck.
