---
title: Focused program for dimension two
tags: [dimension-two, plan, computation, infinity]
---

# Focused program for dimension two

The broad search has narrowed to four credible fronts: solve or obstruct the
explicit factor-invariant Poisson equation, construct a boundary-crossing
quadratic--cubic slice, deform the first possible non-Galois degree-six cover,
or finish the genuinely nonlinear descent audit for the threefold map.

A third, tightly constrained route is nonlinear descent from the threefold
map.  Linear slices, equivariant triangular nonlinear slices, and arbitrary
target polynomials on the natural collision graph are now excluded exactly.
What remains is a genuinely nonequivariant target coordinate $R$ for which
$R(F)$ could be a source coordinate.  Finding one would immediately restrict
the threefold collision to a plane Keller counterexample; proving that no
common coordinate exists would close the last direct descent mechanism.

## Factor front: solve one explicit Poisson equation

The strongest new scaffold in
[The factorization--resultant route](resultant-factor-route.md) is a polynomial
map to the smooth surface

\[
\Phi=(a,\mathcal B,\mathcal C):\mathbb A^2
\longrightarrow
\{\mathcal B^2=a+a^2\mathcal C\}\subset\mathbb A^3
\]

with an exact two-point collision.  Its rational deck involution has Jacobian
$+1$, so it evades the collision-tangent obstruction.  The task is

\[
\text{find }U,V\in
\mathbb C[a,\mathcal B,\mathcal C]/(\mathcal B^2-a-a^2\mathcal C)
\quad\text{with}\quad \{U,V\}_{x,y}=1.
\]

A solution is a plane counterexample.  No linear pair works, although an exact
sum of three quadratic brackets equals $1$, so de Rham cohomology alone cannot
obstruct it.  Descent to the smaller product-coefficient ring adds an elliptic
conductor; linear projections and target-degree-three bracket spans in that
smaller ring are excluded exactly.

This surface is the exceptional affine pseudo-plane $S(2,2,1)$.  The source
map factors as an affine-plane chart in the universal cover
$X^2Y=Z^2-1$, followed by its $\mathbb Z/2$ quotient.  The canonical class
obstruction that rules out most pseudo-planes vanishes at type $r=2$.
Dubouloz--Palka's etale self-maps give the exact rational Darboux pair

\[
x(1+x^2y),\qquad
\frac{2y(2+x^2y)}{(1+x^2y)^2},
\qquad J=4,
\]

but its double pole is genuine.  A two-divisor valuation argument proves that
the first coordinate $\mathcal B$ has no regular constant Poisson mate, so
every triangular shear of this pair is excluded at once.  The full
equivariant Chebyshev family also hits the omitted boundary.  The next ansatz
must change the first Darboux coordinate or produce a non-fibration-preserving
cover endomorphism whose preimage of the omitted line stays in that line.

The same valuation and residue analysis excludes a constant mate for each of
$a,\mathcal B,\mathcal C$.  A weight classification excludes every
$\mathbb C^*$-homogeneous pair, and an exact Gröbner certificate excludes all
pairs represented by ambient polynomials of total degree at most two.  A live
ansatz is therefore necessarily mixed, nonhomogeneous, and at least cubic.

The parallel degree-ten program uses normalized quadratic--cubic factors.
Fixed top or middle coefficient slices that remain in a monic chart are killed
by a nonconstant-unit obstruction, and the Bring--Jerrard slice has
$\chi_c=0$.  A successful slice must be nonlinear and cross the divisor where
the marked quadratic loses its leading coefficient.

## Construction front: deform the sextic cusp cover

The octahedral model in [Plane near-models](plane-near-models.md) has exactly
the desired monodromy and exactly the wrong normalization.  The next target is
a finite normal surface $Y\to\mathbb A^2$ with:

1. degree-six $S_4$ coset monodromy and cusp passport
   $(2^3),(3^2),(4,1,1)$;
2. a proper open subset $X\cong\mathbb A^2$;
3. every ramified divisor contained in $Y\setminus X$;
4. one unramified divisor over the nonproper curve retained in $X$, so a
   generic fiber can fall from six points to one along that curve;
5. nontrivial divisor class relations preventing boundary-supported functions
  from becoming nonconstant units on $X$.

An incidence equation $h(u,v,t)=0$ for such a cover must be nonmonic in the
root variable.  A connected finite étale cover of all of $\mathbb A^2$ would
be trivial; the leading coefficient must vanish on the nonproper curve so the
missing roots escape to infinity rather than ramify at affine source points.

The computational task is now finite enough to encode: enumerate degree-six
passports and normal surface completions, compute normalization and class
groups, then test candidate opens for coordinate ring $\mathbb C[x,y]$.

## Proof front: kill degree six at the boundary

The same data suggest a new conditional theorem:

> If every finite normalization realizing an allowed degree-six cusp passport
> either is $\mathbb A^2$ or has no $\mathbb A^2$ open with all ramification
> in its boundary, then plane Keller maps have geometric degree at least seven.

The first alternative is already killed by Ax--Grothendieck, as shown for the
octahedral model.  The second is a log-surface and divisor-class problem.  A
systematic attack should compute boundary dual graphs, discrepancies, class
groups, and the logarithmic canonical divisor for every allowed passport.

## Newton front: the $(72,108)$ survivor

Independently, specialize the Makar-Limanov and Lee--Li recurrences to the
primitive $2:3$ slope forced by the only degree pair below $125$.  The goals
are:

- generate every admissible integral Newton chain with machine-checkable
  certificates;
- apply the descending-divisor restrictions from the 2024 preprint;
- solve the resulting coefficient equations exactly, one edge at a time;
- either eliminate $(72,108)$ or produce a sharply parameterized candidate.

This is much more realistic than an unrestricted coefficient search with
thousands of variables.

## Exact search infrastructure already in place

- `research/n2/low_degree_collision.sage` proves that the normalized collision
  ideal through total degree three is the unit ideal.
- `research/n2/search_graph_sections.py` rejects every quadratic graph through
  the threefold collision under every linear target projection; the chapter
  theorem rejects graphs of all degrees.
- `artifacts/sympy/verify_plane_attack.py` certifies the quotient, slice, marked
  differential, nonlinear tangent and invariant-quotient obstructions, and
  sextic identities over $\mathbb Q$.
- `artifacts/magma/06_plane_attack_certificates.m` independently checks both
  explicit near-models.
- `artifacts/sympy/verify_resultant_route.py` and
  `artifacts/magma/07_resultant_route.m` certify the factorization--resultant
  identities and the noninjective affine-plane scaffold.
- `research/n2/search_resultant_poisson.py` performs the bounded exact Poisson
  search and the finite-field sparse-plane sieve.

The unrestricted degree-four Gröbner calculation was stopped after 23 minutes;
no conclusion is recorded from it.  In light of the established degree and
covering constraints, future compute should target admissible Newton chains
rather than resume a blind dense search.

## Acceptance rule

No candidate is promoted unless all of the following are exact:

- the two-variable Jacobian is a nonzero constant as a polynomial identity;
- a non-singleton fiber is certified scheme-theoretically;
- all formulas are polynomial on the whole affine plane;
- normalization and boundary claims are proved, not inferred from numerical
  paths;
- the construction survives the current degree, monodromy, and infinity
  restrictions.
