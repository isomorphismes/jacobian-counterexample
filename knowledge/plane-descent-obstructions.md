---
title: Exact obstructions to descending the cubic construction
tags: [dimension-two, theorem, marked-roots, descent]
---

# Exact obstructions to descending the cubic construction

The threefold counterexample is affine-linear in its extra variable and is a
forgetful map for a marked binary cubic.  Every direct way we found to remove
that variable can be excluded uniformly, not merely by a bounded search.

## Affine-linear coordinate theorem

**Theorem.** Let $P,Q\in\mathbb C[x,y]$ satisfy $J(P,Q)=\kappa\ne0$.  If
one coordinate is affine-linear in one source variable, then $(P,Q)$ is a
polynomial automorphism.

Write

$$
P=a(x)y+b(x),\qquad Q=\sum_{i=0}^m q_i(x)y^i.
$$

For $a\ne0$, the coefficient of $y^m$ in the Jacobian is

$$
m a'q_m-aq_m'=0,
$$

so $q_m=\lambda a^m$.  Subtracting $\lambda P^m$ from $Q$ and repeating
gives

$$
Q=h(P)+e(x).
$$

Therefore

$$
\kappa=J(P,Q-h(P))=-a(x)e'(x).
$$

Both factors are units of $\mathbb C[x]$, hence constants, and the resulting
map is triangular after a target shear.  If $a=0$, then
$\kappa=b'(x)Q_y$, and the same unit argument again gives a triangular map.

This pinpoints the dimensional break: “linear in the extra variable” is a rich
threefold ansatz, but a trivial plane ansatz.

## Marked affine planes of binary forms

The obstruction survives every degree.  Let

$$
Q_{a,b}=Q_0+aQ_1+bQ_2

$$

be a genuine affine two-plane of binary forms, dehomogenize by
$q_i(w)=Q_i(w,1)$, and use the same projective-root chart as the threefold
example,

$$
w=\frac{1+xy}{x}=y+\frac1x.
$$

Suppose polynomial outputs $A,B$ satisfy

$$
q_0(w)+Aq_1(w)+Bq_2(w)=0.
$$

Put

$$
s=q_0'+Aq_1'+Bq_2',\qquad
D=q_1q_2'-q_1'q_2.
$$

Since $(x,w)$ has the same area form as $(x,y)$, differentiation at fixed
$w$ and at fixed $x$ gives

$$
q_1A_x+q_2B_x=0,
\quad q_1'A_x+q_2'B_x=s_x,
\quad q_1A_w+q_2B_w=-s.
$$

Taking the indicated determinants yields the exact identity

$$
\boxed{D(w)J(A,B)=s\,s_x.}
$$

If $J(A,B)=\kappa\ne0$, integration in $x$ gives

$$
s^2=2\kappa D(w)x+H(w).
$$

This is impossible in $\mathbb C(w)(x)$: the right side has valuation one
at its linear factor in $x$, whereas every rational square has even
valuations.  Finally $D=0$ would imply $q_2/q_1\in\mathbb C$, contradicting
independence of the two direction forms.

**Consequence.** No affine two-plane of binary cubics, quartics, sextics, or
forms of any degree can reproduce the marked-root construction in this chart.
The third free coefficient in dimension three is essential.

## Polynomial graphs and linear target projections

Another tempting descent is to choose a polynomial graph $z=g(x,y)$, perhaps
one passing through all three colliding source points, and retain two linear
combinations of the three outputs.  This also fails for every polynomial
$g$.

The highest homogeneous parts of the restricted outputs are

$$
(F_{1,\rm top},F_{2,\rm top},F_{3,\rm top})
=(y^3R,3y^2R,-R),
$$

where

$$
R=
\begin{cases}
x^3g_d,&\deg g=d\ge1,\\
x^2(cx+3y),&g=c.
\end{cases}
$$

In either case $R_x\ne0$, and the three leading Jacobians are

$$
\begin{aligned}
J(y^3R,3y^2R)&=-3y^4RR_x,\\
J(y^3R,-R)&=3y^2RR_x,\\
J(3y^2R,-R)&=6yRR_x.
\end{aligned}
$$

Row-reducing any rank-two linear target projection gives one of these three
pivot cases.  The gaps between the coordinate degrees make its displayed term
the unique highest Jacobian term, so it cannot be a nonzero constant.

This includes the simple interpolating graph

$$
z=\frac{27x^2-1}{4},
$$

which contains all three known colliding points.  The exact quadratic
coefficient search in `research/n2/search_graph_sections.py` independently
returns the unit ideal in every target-projection chart.

## Arbitrary target polynomials on the collision graph

The same quadratic graph admits a stronger, purely local obstruction.  Put

$$
(A,B,C)=F\left(x,y,\frac{27x^2-1}{4}\right)
$$

and order the tangent minors as
$\bigl(J(A,B),J(A,C),J(B,C)\bigr)$.  At the three colliding points they form
the exact matrix

$$
M=
\begin{pmatrix}
0&0&-2\\
-81/8&-3/2&106\\
81/8&3/2&106
\end{pmatrix}.
$$

Its rows satisfy

$$
M_+ + M_- +106M_0=0.
$$

Now let $R,S\in\mathbb C[a,b,c]$ be **arbitrary target
polynomials**, not necessarily linear.  All three source points have the same
target value, so the coefficients of the target two-form
$dR\wedge dS$ are the same vector $\omega\in\mathbb C^3$ at all three.
The chain rule says that the three restricted Jacobians are $M_i\omega$.
If they were one nonzero constant $\kappa$, the row relation would give

$$
(1+1+106)\kappa=108\kappa=0,
$$

a contradiction.  Thus this natural collision graph cannot be repaired by
*any* nonlinear polynomial change of target functions.  The matrix and row
relation are part of the exact SymPy certificate.

## Nonlinear equivariant target slices

There is one more tempting escape from the linear-slice theorem.  The target
weights $(-2,-1,1)$ permit triangular homogeneous coordinates such as

$$
R_\phi=A+B^2\phi(BC),
\qquad
S_\psi=B+AC\psi(AC^2).
$$

Could $R_\phi(F)$ or $S_\psi(F)$ become a source coordinate even though no
linear output does?  They cannot.

Recall the source invariants $u=xy$, $v=x^2z$ and the semi-invariant
numerators $a,b,c$ from [Plane near-models](plane-near-models.md).  If
$r=R_\phi(F)$ were a coordinate, then $V(r)\cong\mathbb A^2$ would carry the
restricted $\mathbb C^*$-action.  Its tangent weights at the origin are
$(1,-1)$.  Every algebraic torus action on the affine plane is linearizable
{cite}`gutwirth1962`, so its invariant ring would be a polynomial ring in one
variable.  Exactness of invariants for the reductive group $\mathbb C^*$,
together with the fact that every weight-two source polynomial is
$x^2\mathbb C[u,v]$, instead gives

$$
\mathbb C[V(r)]^{\mathbb C^*}
 =\mathbb C[u,v]/(k_\phi),
\qquad
k_\phi=a+b^2\phi(bc).
$$

This curve is not $\mathbb A^1$.  If $\phi$ has degree $m$ and nonzero
leading coefficient $\ell$, then

$$
(k_\phi)_{\rm top}
=9\ell(-3)^m u^{2m+4}(v+3u)^{2m+2}.
$$

It has two distinct points at infinity, whereas $\mathbb A^1$ has one.  For
$\phi=0$, already
$a=(1+u)(3u^3+u^2v+4u^2+2uv+v)$ is reducible.  Hence no $R_\phi(F)$ is a
coordinate.

The weight-minus-one family is even more rigid.  If
$s=S_\psi(F)$ were a coordinate, the same argument with tangent weights
$(1,-2)$ would give

$$
\mathbb C[V(s)]^{\mathbb C^*}
=\mathbb C[u,v]/\bigl(b+ac\psi(ac^2)\bigr)\cong\mathbb C[t].
$$

But at $u=-1$ one has $a=0$ and $b=2$.  Therefore $1+u$ is a visibly
nonconstant unit on this quotient curve, impossible in $\mathbb C[t]$.

The closest special case is $R=A+\lambda B^2$.  For
$k=a+\lambda b^2$,

$$
k(-1,v)=4\lambda.
$$

Thus $1+u$ is a nonconstant unit when $\lambda\ne0$, while $\lambda=0$
returns the reducible $F_1$ slice.  Even the unusually simple value
$\lambda=-1/12$ does not escape: using
$a=(b-u)(1+u)/3$ gives

$$
12k=4(1+u)-\bigl(b-2(1+u)\bigr)^2,
$$

but the apparent affine-line parameter misses $1+u=0$ and is a punctured
line.  This rules out the most natural nonlinear slice that fills the missing
divisor of the $F_1=-1/4$ fiber.  It does **not** classify every nonlinear
target coordinate, so genuinely nonequivariant slices remain an open route.

## No linear output can be the lowering coordinate

Let $L=\alpha F_1+\beta F_2+\gamma F_3=h(x,y)z+g(x,y)$.  Its $z$-coefficient
is

$$
h=\alpha(1+xy)^3+3\beta x(1+xy)^2-\gamma x^3.
$$

On a component $1+xy=rx$ of $h=0$, where

$$
\alpha r^3+3\beta r^2-\gamma=0,
$$

the constant term reduces exactly to

$$
g=r(\alpha r+4\beta)+\frac{\alpha r+2\beta}{x}.
$$

Each such component is a copy of $\mathbb C^*$.  Additivity of the compactly
supported Euler characteristic shows that a generic fiber of $L$ has

$$
\chi_c=1+N,
$$

where $N$ counts the components on which the displayed Laurent polynomial is
nonconstant, with the elementary $x=0$ correction when $\alpha=0$.  Unless
$L$ is proportional to $F_1$, one has $N\ge1$, so the generic fiber is not
$\mathbb A^2$.  The remaining cases are also impossible:

- $F_1$ is reducible as a polynomial, so it is not a coordinate;
- if $\alpha=0,\beta\ne0$, the generic Euler characteristic is at least two;
- $F_3=x(2-3xy-x^2z)$ has generic fiber with a nonconstant unit and Euler
  characteristic zero.

Thus no nonzero linear combination of the three outputs is a source
coordinate.  Linear target slicing cannot turn the threefold collision into a
plane Keller collision.
