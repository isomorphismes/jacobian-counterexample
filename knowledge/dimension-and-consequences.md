---
title: Dimensions, reductions, and consequences
tags: [dimension, reduction, dixmier-conjecture]
---

# Dimensions, reductions, and consequences

## Every dimension at least three

For \(n>3\), define

\[
F^{(n)}(x,y,z,t_4,\ldots,t_n)
=(F_1(x,y,z),F_2(x,y,z),F_3(x,y,z),t_4,\ldots,t_n).
\]

Its Jacobian matrix is block diagonal, so

\[
\det JF^{(n)}=-2.
\]

Padding the three colliding points with the same extra coordinates preserves
the collision.  Hence the conjecture is false in every dimension \(n\ge3\).

## Dimension two remains separate

Nothing here projects to a two-variable Keller counterexample.  As immediately
pre-announcement literature records, even \(n=2\) remained unresolved
{cite}`bisi2026,makarlimanov2025,rodriguez2026`.  A counterexample in dimension
three settles the unrestricted all-dimensional statement negatively, but does
not settle the plane problem.

## Compatibility with classical reductions

Bass--Connell--Wright and Yagzhev reduce the all-dimensional conjecture to maps
of the form identity plus a cubic homogeneous part, after adding variables
{cite}`bass1982`.  Drużkowski gives a further cubic-linear reduction
{cite}`druzkowski1983`, and de Bondt--van den Essen give a symmetric reduction
{cite}`debondt2005`.

Therefore this example implies the existence of counterexamples in those
reduced forms in some larger dimensions.  It does **not** imply the existence
of a cubic counterexample in dimension three.  There is no conflict with
Wang's degree-at-most-two theorem {cite}`wang1980` or special cubic results in
dimension three {cite}`wright1993`.

## Dixmier conjecture

The standard rank-preserving implication \(DC_n\Rightarrow JC_n\) sends a
Keller map to a Weyl algebra endomorphism.  For the normalized map \(H\), let

\[
\delta_i=\sum_j (JH^{-1})_{ji}\,\partial_j.
\]

Since \(\det JH=1\), every coefficient of \(JH^{-1}\) is polynomial.  The
identities

\[
\delta_i(H_j)=\delta_{ij},\qquad [\delta_i,\delta_j]=0
\]

show that

\[
X_i\longmapsto H_i,\qquad \partial_i\longmapsto\delta_i
\]

defines an endomorphism of the third Weyl algebra.  The included SymPy
certificate checks these relations exactly.  Were this endomorphism an
automorphism, the standard centralizer argument would force every \(X_j\) to
lie in \(\mathbb C[H_1,H_2,H_3]\), giving a polynomial inverse for \(H\) and
contradicting its three-point fiber.  It is therefore an explicit
non-automorphic Weyl-algebra endomorphism: the rank-three Dixmier conjecture is
false.

Belov-Kanel--Kontsevich and Tsuchimoto proved the opposite indexed implication
\(JC_{2n}\Rightarrow DC_n\); together with the older
\(DC_n\Rightarrow JC_n\), this yields stable equivalence
{cite}`belov2007,tsuchimoto2005`.

This conclusion should be kept rank-specific: it does not by itself settle the
rank-one or rank-two Dixmier conjectures.

## Field scope

The same polynomial and collision work over any field of characteristic not
equal to \(2\).  In odd positive characteristic this is another counterexample,
but the positive-characteristic analogue was already false for elementary
Frobenius reasons.  The historical breakthrough is over characteristic zero.
