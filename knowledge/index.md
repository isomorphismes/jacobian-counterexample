---
title: Exact audit and structural analysis
tags: [jacobian-conjecture, keller-map, counterexample, index]
---

# Exact audit and structural analysis

On 20 July 2026, Levent Alpöge publicly announced a concrete polynomial map of
affine three-space as a counterexample to the Jacobian conjecture
{cite}`alpoge2026x`.  Later that day Andy Jiang (@davikrehalt) posted its
projective symmetric-product marked-root formulation {cite}`jiang2026x`.
This book records an independent exact audit, a short hand proof, and a
structural interpretation that turns the example into the forgetful map from a
binary cubic with a marked simple root to its coefficients.

:::{admonition} Bottom line
:class: important
The displayed map really does have constant Jacobian determinant \(-2\) and a
fiber containing three distinct points.  In fact, that fiber is exactly three
reduced points and the map has geometric degree three.  It refutes the standard
Jacobian conjecture in dimension \(3\), and hence in every dimension
\(n\geq3\) after adjoining identity coordinates.  The dimension-two problem is
not affected.
:::

The conclusion rests only on finite polynomial identities over
\(\mathbb Q\).  It has been checked in SymPy, SageMath, and Magma, but the
short proof in [Structural determinant certificate](structural-certificate.md)
does not require trusting a determinant expansion.

The explicit formula, Jiang's projective restriction, Lou's
resultant-normalized chart, and the incidence model used in this book are
isomorphic presentations of one degree-three etale morphism.  They are not
literal coordinate identities: Lou's formula is left--right linearly
equivalent to the announced map, while the projective-to-affine
identifications require choices.  The exact comparison is recorded in the
[literature audit](literature-audit.md).

## What is new in this audit

Beyond reproducing the announcement, the notes establish:

1. a two-line rational-coordinate proof of \(\det JF=-2\);
2. a global binary-cubic identity explaining all coefficients;
3. the exact reduced fiber ideal at the announced target;
4. an integer-coefficient normalization \(H=X+\text{higher terms}\) with
   \(\det JH=1\);
5. an explicit inverse branch for every simple root of a cubic;
6. exact fiber cardinalities \(3,1,0\), an omitted triple-root curve, and
   generic degree \(3\);
7. the discriminant hypersurface as the nonproperness set, with explicit
   escaping families.
8. exact obstructions to every direct marked-root, polynomial-graph, linear
   target-slice, and natural equivariant nonlinear descent to dimension two;
9. an equivariant noninjective plane quotient with Jacobian \(-2c^2\), and an
   octahedral degree-six cusp cover with Jacobian \(108x^3\);
10. the general coefficient--resultant determinant law, an exact rejection of
    the Bring--Jerrard degree-ten factor surface, and a noninjective
    quadratic-factor $\mathbb A^2$ scaffold reducing one new route to an
    explicit Poisson equation;
11. the identification of that scaffold with Miyanishi's exceptional
    pseudo-plane $S(2,2,1)$, a rational constant-Jacobian near-solution from
    the Dubouloz--Palka formulas, and exact generator, homogeneous, quadratic,
    and boundary-preservation no-go theorems.

## Reading paths

- For the shortest decisive argument, read [the map](map-definition.md),
  [the structural determinant proof](structural-certificate.md), and
  [the exact fiber](fiber-scheme.md).
- For the conceptual explanation, continue through
  [generic fibers and binary cubics](generic-fiber.md) and
  [behavior at infinity](infinity.md).
- For historical status and cautious attribution, see the
  [literature audit](literature-audit.md).
- For the active plane attack, start with [the current plane status](plane-status.md),
  then read [the descent obstructions](plane-descent-obstructions.md),
  [the two exact near-models](plane-near-models.md),
  [the factorization--resultant route](resultant-factor-route.md),
  [the pseudo-plane Poisson obstructions](pseudoplane-poisson-obstructions.md), and the
  [focused program](plane-program.md).
- For independent reproduction, use [reproducibility](reproducibility.md) or
  run the included [SymPy notebook](notebooks/sympy-verification.ipynb).

## Editorial status

The mathematical identities are stated as theorems because they are proved
inside this repository.  Public priority and reception are stated more
cautiously: the construction was only hours old when this audit was assembled,
and no refereed paper for the new map had yet appeared.  The web audit is frozen
at 2026-07-20, Europe/Warsaw.
