---
title: Literature and provenance audit
tags: [literature, provenance, status]
---

# Literature and provenance audit

This page separates the exact mathematics from the rapidly changing public
record.  Searches were performed on 2026-07-20.

## Same-day provenance

The earliest indexed public source found for the exact formula is Levent
Alpöge's [X announcement](https://x.com/__alpoge__/status/2079028340955197566),
posted 2026-07-20 at 02:19:17 UTC.  The post gives the displayed polynomial,
the determinant −2, and the three-point collision; it credits Akhil for asking
about the problem and Fable for working during the World Cup final.  The
precise authorship and priority language should be confirmed with the
announcer before formal publication {cite}`alpoge2026x`.

Qiaochu Yuan reproduced the exact map and conclusion in a
[MathOverflow answer](https://mathoverflow.net/questions/130777/could-the-jacobian-conjecture-be-undecidable/513385).
Jean Abou Samra posted an independent
[Sage verification](https://gitlab.com/-/snippets/6011973) at approximately
06:31 UTC.  Exact-phrase searches found no indexed pre-announcement occurrence,
but a negative search is not proof of priority.

At 12:02:19 UTC the same day, Andy Jiang (@davikrehalt) posted the
[projective symmetric-product formulation](https://x.com/davikrehalt/status/2079175065695035442):
restrict the map

$$
\mathbb P^1\times\operatorname{Sym}^2(\mathbb P^1)
\longrightarrow \operatorname{Sym}^3(\mathbb P^1),
\qquad (p,D)\longmapsto p+D,
$$

after deleting its ramification divisor and the inverse image of a hyperplane
tangent but not osculating to the small diagonal.  Jiang explicitly presented
the formulation in the post as GPT output.  It is exactly the projective form
of the marked-simple-root construction developed here {cite}`jiang2026x`.

Later the same day, Aaron Lou ([@aaron_lou](https://x.com/aaron_lou)) hosted
[a self-contained factorization--resultant derivation](https://aaronlou.com/jacobian_counterexample_derivation.pdf)
{cite}`lou2026note`.
Exact left--right linear equivalence shows that its map is the announced map
after $z\mapsto-z$ in the source and reversal of the three outputs in the
target.  It is valuable independent reconstruction and motivation, not a
distinct counterexample.  A same-day
[weighted-lift repository](https://github.com/algal/jacobianfun) gives further
exact families; it is self-published and unrefereed, and is treated only as
construction data in this audit.

As of the cutoff, no refereed paper or arXiv preprint devoted to this new map
was found.  The appropriate wording is therefore: an exact, reproducible
counterexample with provisional same-day provenance, not yet vetted through
peer review.

## Equivalence of the four presentations

The Alpöge formula, Jiang's projective model, Lou's resultant chart, and this
repository's marked-root incidence are presentations of one algebraic
morphism, but they are not literally the same formulas and the identifications
are not canonical.

Let

$$
\mu:\mathbb P^1\times\operatorname{Sym}^2(\mathbb P^1)
\longrightarrow\operatorname{Sym}^3(\mathbb P^1)
$$

be Jiang's map, let $R$ be its ramification divisor, and let $H_\infty$ be a
hyperplane tangent but not osculating to the small diagonal.  If $\lambda$
defines $H_\infty$, normalization gives

$$
[C]\longmapsto \frac{C}{\lambda(C)}:
\operatorname{Sym}^3(\mathbb P^1)\setminus H_\infty
\xrightarrow{\sim}\{C:\lambda(C)=1\}=H_\tau.
$$

Upstairs, deleting $R$ says precisely that the marked root is simple; the two
unmarked roots may still coincide.  Therefore

$$
\bigl(\mathbb P^1\times\operatorname{Sym}^2(\mathbb P^1)\bigr)
\setminus\bigl(R\cup\mu^{-1}(H_\infty)\bigr)
\simeq X_\tau,
$$

and $\mu$ becomes the forgetful map $X_\tau\to H_\tau$.  A tangent,
nonosculating hyperplane meets the twisted cubic in $2p+q$ with $p\ne q$; all
such choices are equivalent under $\operatorname{PGL}_2$.

Lou writes the marked cubic as a linear factor times a quadratic and imposes
both the affine coefficient level and $\operatorname{Res}(\ell,q)=1$.  Those
conditions fix the projective and factor-rescaling gauges and give an explicit
global $\mathbb A^3$ chart on the same open incidence.  If $G$ is Lou's
coordinate map and $F$ is Alpöge's, the exact relation is

$$
G=R_0\circ F\circ S_0,
\qquad S_0(x,y,z)=(x,y,-z),\quad R_0(A,B,C)=(C,B,A).
$$

This is **left--right linear equivalence**, or an isomorphism of morphisms, not
strict conjugacy: the source and target changes are independent.  Etaleness,
geometric degree three, fiber structure, and nonproperness are invariant under
these identifications; the chosen bases, signs, affine levels, and the
numerical Jacobian constant are presentation-dependent.  Higher-degree
weighted-lift families are descendants of the same idea, not equivalent maps
when their geometric degrees differ.

## Status immediately before the announcement

Rodríguez Díaz's June 2026 refereed historical article described control of
ramification at infinity as the persistent obstacle {cite}`rodriguez2026`.
Bisi et al. described the conjecture as open even in dimension two
{cite}`bisi2026`.  Makar-Limanov analyzed constraints on a hypothetical plane
counterexample {cite}`makarlimanov2025`, while Truong studied properness as the
critical obstruction in reduced classes {cite}`truong2026`.

The dedicated [plane status chapter](plane-status.md) contains the extended
2026 audit: geometric degree at least six, the provisional degree-108 bound,
the surviving $(72,108)$ Newton configuration, and the exact distinction
between peer-reviewed restrictions and recent preprints.

These papers establish the immediate pre-announcement context; they naturally
do not discuss a formula announced later.

## Foundational references

Keller's 1939 paper is the traditional source {cite}`keller1939`, although
Rodríguez Díaz traces the plane statement to Kraus in 1884.  The standard
modern reduction is Bass--Connell--Wright {cite}`bass1982`; important later
reductions include Drużkowski {cite}`druzkowski1983` and the symmetric
reduction of de Bondt--van den Essen {cite}`debondt2005`.

## The exceptional pseudo-plane connection

The quadratic-factor scaffold in this repository is exactly the affine
pseudo-plane

$$
S(2,2,1)=\{u(1+uv)=w^2\}.
$$

Miyanishi developed affine pseudo-coverings specifically to study a possible
factorization of a plane Keller map through such an intermediate surface
{cite}`miyanishi2005,miyanishi2015lectures`.  The standard canonical-class
obstruction is silent here: this is type $r=2$, for which
$K_S=(r-2)F_0$ vanishes.

Dubouloz--Palka's refereed 2018 paper proves that this pseudo-plane admits
large families of nonproper etale endomorphisms and gives explicit
Belyi--Shabat formulas {cite}`duboulozpalka2018`.  These are maps $S\to S$,
not the missing map $S\to\mathbb A^2$.  Exact conjugation in the
[factorization chapter](resultant-factor-route.md) shows that their plane-chart
transition is a constant-Jacobian rational map with a genuine pole, and that
the published deformation family cannot avoid the omitted boundary line.

The current Borisov--Gabber--Vasiu manuscript treats related standard affine
pseudo-planes, constructs maps to affine space in positive characteristic,
and explicitly contrasts them with the unresolved characteristic-zero
$r=2$ case {cite}`borisovgabbervasiu2026`.  It is a current manuscript, not a
refereed status authority; it is used here to cross-check the boundary of the
known theorem, not to certify a plane result.

## Claimed proofs that are not status authorities

The user-supplied arXiv:2209.01451 is Quan Xu's unrefereed claimed proof
{cite}`xu2022`.  It must not be cited as an established theorem.  Other useful
cautionary examples include:

- Varshavsky's explicitly withdrawn preprint after an erroneous proposition
  {cite}`varshavsky1999`;
- Kuo--Parusiński--Păunescu's withdrawn plane proof {cite}`kuo2005`;
- Bartenwerfer's 2022 claim and the subsequent correction/critique
  {cite}`bartenwerfer2022,brzostowski2023`.

The new example does not require trusting any global theorem or claimed proof:
its decisive content is a determinant identity and an explicit collision.

## Attribution policy for this repository

This repository is an **independent audit and structural analysis**, not a claim
to have first discovered the displayed formula.  Until a stable paper appears,
cite Alpöge's original formula announcement, Jiang's projective formulation,
the public replications or derivations actually used, and this repository
according to their distinct roles.
