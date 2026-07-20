---
title: Adversarial checks and common objections
tags: [faq, audit, objections]
---

# Adversarial checks and common objections

## “The determinant is \(-2\), not \(1\)”

The standard hypothesis is any nonzero constant.  In any case,
[the normalized map](normalization.md) has determinant exactly \(1\), integer
coefficients, and identity linear part.

## “A nonzero Jacobian only gives local injectivity”

Correct—and the conjecture claimed that this local condition, for a polynomial
self-map of affine space, forced global polynomial invertibility.  The explicit
collision disproves precisely that claim.

## “The map is nonproper, so it is not a counterexample”

Properness is not a hypothesis of the Jacobian conjecture.  Adding it would
make the global conclusion much easier.  The escape at infinity explains how
the valid Keller map fails globally; see [Discriminant and behavior at
infinity](infinity.md).

## “The three substitutions may miss a zero of the determinant”

The determinant was computed as a polynomial identity, not sampled at the
three points.  The hand proof works on a dense open set and then uses polynomial
identity, while three CAS implementations independently expand it.

## “Perhaps the three points are equal in disguise”

Their \(x\)-coordinates are \(0,1,-1\), so they are distinct over
characteristic zero.  The fiber Gröbner basis proves they are exactly the three
reduced points over the target.

## “Ax--Grothendieck or simple connectedness forbids this”

Ax--Grothendieck says an **injective** polynomial self-map is surjective; this
map is not injective.  Simple connectedness rules out nontrivial **finite**
étale covers; this map is étale but nonproper and therefore not finite.  Its
image even omits an explicit curve.

## “Known degree-three or prime-degree theorems forbid it”

The coordinate degrees are \((7,6,4)\).  Cubic-homogeneous reductions raise
dimension, and the recent prime field-extension result often mentioned in this
context is explicitly two-dimensional.  Neither applies to this map.

## “A preprint already proved the conjecture”

The user-supplied arXiv:2209.01451 is an unrefereed claimed proof, not accepted
literature.  Its conclusion is contradicted by these exact identities.  The
history of this problem contains many withdrawn or corrected proof claims; see
the [literature audit](literature-audit.md).
