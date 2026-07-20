---
title: Discriminant and behavior at infinity
tags: [nonproperness, discriminant, infinity]
---

# Discriminant and behavior at infinity

The cubic model identifies exactly where inverse branches escape.

## Discriminant hypersurface

For

\[
p(w)=cw^3-2w^2+bw-2a,
\]

the discriminant is \(4\Delta(a,b,c)\), where

\[
\boxed{
\Delta=b^2-cb^3-16a+18abc-27a^2c^2.}
\]

Thus \(\Delta=0\) is the locus where the binary cubic has a multiple root.

## Explicit escape through every discriminant point

Every point of \(\Delta=0\) has a repeated finite root \(\rho\) and can be
written

\[
(a,b,c)=\left(\rho^2-c\rho^3, 4\rho-3c\rho^2, c\right).
\]

For \(t\ne0\), define

\[
(x,y,z)=
\left(
\frac1t,\,
\rho-t,\,
5t^2-3\rho t-ct^3
\right).
\]

Exact substitution gives

\[
F(x,y,z)=
\left(
\rho^2+\rho t-c\rho^3,
4\rho+2t-3c\rho^2,
c
\right).
\]

As \(t\to0\), the source escapes to infinity and the image converges to the
chosen discriminant point.  Hence every point of \(V(\Delta)\) is a
nonproperness value.

This family can also be read as a uniform perturbation proof.  If \(\rho\) is a
repeated root at \((a_0,b_0,c_0)\), set

\[
(a_\varepsilon,b_\varepsilon,c_\varepsilon)
=(a_0+\varepsilon\rho/2,b_0+\varepsilon,c_0).
\]

Then \(\rho\) stays a root and its derivative becomes \(\varepsilon\), so its
inverse has \(x=2/\varepsilon\) and escapes.

Conversely, let \(I=\{Q=0\}\) be the full projective-root incidence inside
\(\mathbb A^3\times\mathbb P^1\).  The projection
\(I\to\mathbb A^3\) is projective and quasi-finite, hence finite.  Over
\(\Delta\ne0\), all roots are simple, so \(I=I^{\mathrm{sm}}\) and the
marked-root isomorphism identifies this finite étale map with the restriction
of \(F\).
All root-gradient normalizations and the inverse formulas remain bounded in a
neighborhood of a limiting target, so no inverse branch can escape.  Therefore
the nonproperness set is exactly

\[
\boxed{S_F=V(\Delta).}
\]

## The simplest escaping curve

Taking \(\rho=0,c=0\), and replacing \(t\) by \(1/s\), gives

\[
(x,y,z)=(s,-1/s,5/s^2),\qquad F(x,y,z)=(0,2/s,0).
\]

As \(|s|\to\infty\), the source escapes and the image tends to the origin.

## Why nonproperness is not an objection

The Keller condition says that \(F\) is étale: it has no critical points and is
locally invertible.  It does **not** assume properness.  A proper étale
self-map of complex affine space would be a finite covering and global
topology would force degree one.  The Jacobian conjecture asserted, in effect,
that polynomiality plus the constant-Jacobian condition was already strong
enough to prevent escape at infinity.

This example shows exactly the opposite: the discriminant is where two or three
otherwise finite inverse branches run to infinity.  The escape curve is the
mechanism of the counterexample, not a loophole in it.  This is consonant with
the long-standing focus on nonproperness and ramification at infinity
{cite}`jelonek1993,rodriguez2026,truong2026`.
