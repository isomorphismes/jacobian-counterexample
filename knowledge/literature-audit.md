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
posted 2026-07-20.  Decoding the public status identifier gives 02:19:17 UTC.
The post credits a Claude Fable interaction; the precise authorship and priority
language should be confirmed with the announcer before formal publication.

Qiaochu Yuan reproduced the exact map and conclusion in a
[MathOverflow answer](https://mathoverflow.net/questions/130777/could-the-jacobian-conjecture-be-undecidable/513385).
Jean Abou Samra posted an independent
[Sage verification](https://gitlab.com/-/snippets/6011973) at approximately
06:31 UTC.  Exact-phrase searches found no indexed pre-announcement occurrence,
but a negative search is not proof of priority.

Later the same day, Aaron Lou hosted
[a self-contained factorization--resultant derivation](https://aaronlou.com/jacobian_counterexample_derivation.pdf).
Exact conjugacy shows that its map is the announced map after $z\mapsto-z$ and
reversal of the three outputs.  It is valuable independent reconstruction and
motivation, not a distinct counterexample.  A same-day
[weighted-lift repository](https://github.com/algal/jacobianfun) gives further
exact families; it is self-published and unrefereed, and is treated only as
construction data in this audit.

As of the cutoff, no refereed paper or arXiv preprint devoted to this new map
was found.  The appropriate wording is therefore: an exact, reproducible
counterexample with provisional same-day provenance, not yet vetted through
peer review.

## Status immediately before the announcement

Rodríguez Díaz's June 2026 refereed historical article described control of
ramification at infinity as the persistent obstacle {cite}`rodriguez2026`.
Bisi et al. described the conjecture as open even in dimension two
{cite}`bisi2026`.  Makar-Limanov analyzed constraints on a hypothetical plane
counterexample {cite}`makarlimanov2025`, while Truong studied properness as the
critical obstruction in reduced classes {cite}`truong2026`.

The dedicated [plane status chapter](plane-status.md) contains the extended
2026 audit: geometric degree at least six, the provisional degree-108 bound,
the surviving `(72,108)` Newton configuration, and the exact distinction
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

\[
S(2,2,1)=\{u(1+uv)=w^2\}.
\]

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
cite the original announcement, the public replication, and this repository
according to their distinct roles.
