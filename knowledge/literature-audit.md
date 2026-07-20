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

These papers establish the immediate pre-announcement context; they naturally
do not discuss a formula announced later.

## Foundational references

Keller's 1939 paper is the traditional source {cite}`keller1939`, although
Rodríguez Díaz traces the plane statement to Kraus in 1884.  The standard
modern reduction is Bass--Connell--Wright {cite}`bass1982`; important later
reductions include Drużkowski {cite}`druzkowski1983` and the symmetric
reduction of de Bondt--van den Essen {cite}`debondt2005`.

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
