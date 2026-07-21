---
title: Research directions
tags: [open-questions, research]
---

# Research directions

The counterexample closes the all-dimensional conjecture but opens a more
concrete research program.

## Recover the search family

The map is affine-linear in $z$:

$$
F(x,y,z)=A(x,y)z+B(x,y).
$$

Its $z$-coefficient row

$$
((1+xy)^3,\,3x(1+xy)^2,\,-x^3)
$$

is built from the unimodular pair $x,1+xy$.  Understanding the parameter
space of such rows and solving the constant-Jacobian equations coefficient by
coefficient may yield smaller examples or a classification.

## Minimize complexity

Natural optimization targets are:

- maximum coordinate degree;
- total monomial count;
- coefficient height;
- a homogeneous or sparse normal form;
- the dimension introduced by cubic stabilization.

The present normalized example has coordinate degrees $(4,6,7)$ and integral
coefficients.  Classical results show that maximum degree $2$ is impossible,
but the gap between $2$ and $7$ in dimension three is now concrete.

## Make stabilization explicit

Apply Bass--Connell--Wright/Yagzhev and Drużkowski reductions algorithmically to
this exact map.  Record the resulting dimensions, coefficient growth, and the
transported collision.  This would turn an existential corollary into a
compilable cubic counterexample.

## Plane obstruction

The missing step is now precise: affine-linearity, affine two-planes of marked
forms, polynomial graph restrictions, linear target slices, and the natural
equivariant nonlinear target shears are all ruled out.  The active construction
target is a non-Galois degree-six cusp cover
whose finite normalization is not affine two-space but contains affine
two-space as a proper étale open.  See
[the exact obstructions](plane-descent-obstructions.md),
[near-models](plane-near-models.md), and [the focused program](plane-program.md).

## Geometry and topology

- Compute the topology and stratification of the discriminant complement.
- Describe the $S_3$ monodromy of the three inverse branches.
- Study the embedding of the marked-root space into compactifications and the
  divisors responsible for escape.
- Write the induced rank-three Weyl algebra endomorphism explicitly.

## Formal verification

Translate the structural proof into Lean, Isabelle, or Coq.  The core requires
only polynomial normalization, the chain rule, and a three-point inequality,
making it unusually suitable for a short proof-assistant certificate.
