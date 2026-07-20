---
title: The plane problem after the threefold example
tags: [dimension-two, status, literature]
---

# The plane problem after the threefold example

:::{admonition} Current verdict
:class: warning
The two-dimensional Jacobian conjecture is **not solved here**.  As of
2026-07-20, no accepted proof or counterexample in dimension two was found in
the literature audit.  This chapter separates established restrictions,
preprint claims, and the new exact calculations in this repository.
:::

The threefold map has geometric degree three.  That mechanism does not simply
drop a variable: in the plane, geometric degrees $2,3,4,5$ are excluded in
the established literature, so the first possible degree of a noninvertible
Keller map is

\[
\mu=[\mathbb C(x,y):\mathbb C(P,Q)]\geq 6.
\]

The low-sheeted conclusion is cited through Żołądek's Theorem 6.12 and is used
as established input by Makar-Limanov's refereed 2021 paper
{cite}`zoladek2008,orevkov1987,makarlimanov2021`.  Żołądek's
*separate* gcd-of-degrees argument has a known gap and is not used here.

A Galois function-field extension cannot be a counterexample: the Keller
condition plus Galoisness forces polynomial invertibility
{cite}`campbell1973`.  Thus a first
counterexample should be sought as a composite, non-Galois cover, with degree
six the first plausible target.

The factorization route in this repository produces exactly such an
intermediate-cover framework.  Its degree-two top extension is the standard
Galois affine pseudo-covering

\[
\mathbb A^2\longrightarrow
S(2,2,1)=\{u(1+uv)=w^2\}.
\]

A second etale map from this pseudo-plane to $\mathbb A^2$ would compose to
a non-Galois plane Keller map of even geometric degree.  Since total degrees
two through five are excluded, the second map would have generic degree at
least three.  Miyanishi's canonical-divisor obstruction eliminates broad
classes of pseudo-planes, but vanishes for this exceptional type $r=2$
{cite}`miyanishi2005,miyanishi2015lectures`.  The exceptional direction
remains tied to the classical plane conjecture in the 2026
Borisov--Gabber--Vasiu manuscript {cite}`borisovgabbervasiu2026`.

## Degree and Newton constraints

The strongest quantitative degree statement located is the 2022 preprint of
Guccione--Guccione--Horruitiner--Valqui.  It reports that either

\[
\max(\deg P,\deg Q)\geq 125
\]

or, up to exchanging the coordinates, the single pair

\[
(\deg P,\deg Q)=(72,108)
\]

survives below $125$ {cite}`guccione2022`.  In particular, its safe headline is a lower bound of
$108$, but it remains a preprint and is labeled that way throughout this
vault.

For the exceptional pair, divide by the gcd $36$ to obtain the primitive
ratio $2:3$.  Chau's theorem on the nonproper value set then forces all its
branches to share one point at infinity and gives a cusp-type leading
resultant of the form {cite}`chau2004`

\[
C\left(A^3u^3-B^2v^2\right)^M
\quad+
\text{terms of lower }(2,3)\text{-weight}.
\]

This is why the degree-six cusp cover in
[Plane near-models](plane-near-models.md) is not an arbitrary toy: it matches
the first allowed covering degree and the forced $2:3$ geometry at infinity.

Further refereed restrictions include homothetic Newton polygons for a
normalized reduced counterexample, restrictions on admissible edges, and
Makar-Limanov's field-degree inequality, which in particular gives a gap
$n-m>6$ in his notation.  The 2024 integral Newton-chain work and Lee--Li's
inner-polynomial program are promising but remain preprints
{cite}`makarlimanov2021,makarlimanov2025,makartrakhtenberg2024,leeli2024`.

## Claims deliberately kept provisional

Moskowicz's 2024 preprint claims that prime geometric degree is impossible
{cite}`moskowicz2024`.
It is useful motivation, but the audit found no journal publication, so no
argument in this book depends on it.  The stronger, established
$\mu\geq6$ restriction is enough to rule out transplanting the degree-three
cover.

The 2022 paper claiming a complete proof in dimension two was formally
corrected: its key proposition is false and its conclusions were withdrawn
{cite}`bartenwerfer2022,bartenwerfer2023correction`.
Other recent complete-proof preprints remain unaccepted.  The recurring gap is
control at infinity, exactly where a nonproper Keller map can lose sheets.

## Working specification for a counterexample

A credible plane counterexample must simultaneously have:

- geometric degree at least six and non-Galois monodromy;
- no affine ramification, although several sheets may disappear at infinity;
- a finite normalization that contains the source $\mathbb A^2$ as an open
  subset but is not itself $\mathbb A^2$;
- nontrivial boundary divisor classes, so deleting the ramified boundary does
  not create a nonconstant unit on the source;
- the known Newton-polygon, degree, and nonproper-curve constraints.

The last three requirements are the main structural difference between a true
Keller cover and the explicit near-models obtained so far.
