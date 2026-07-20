# Research journal

This file is chronological and append-only.  Commands shown are representative;
all decisive outputs are also encoded as executable assertions.

## 2026-07-20 — intake and independent audit

- The workspace was empty and was not a Git repository.
- Froze the submitted coordinate order `(x,y,z)` and copied the formula without
  expansion.
- Ran SageMath over `QQ`; it returned `det(JF) = -2` and all three submitted
  points mapped to `(-1/4,0,0)`.
- Repeated the calculation in SymPy and Magma using exact rationals.  No
  floating-point or sampled-point argument was used.
- Searched the exact monomials on the web.  Found the same map in Levent
  Alpöge's 2026-07-20 announcement, a MathOverflow answer quoting it, and an
  independent public Sage snippet.  At intake there was no refereed paper for
  the new example.

## 2026-07-20 — hand certificate

- Introduced `u=1+xy` and `w=x^2*z+3xy-2` on `x != 0`.
- Rewrote the three outputs as weighted rational expressions
  `(a/x^2,b/x,-xw)`.
- Computed the small weighted Jacobian by hand; its numerator collapses to
  `-2`.  The source change contributes `x^3`, proving `det JF=-2`.
- Added a second weighted-coordinate certificate in Magma using
  `t=1+xy, s=x^2*z`.  This is algebraically independent in presentation from
  the full expanded determinant.

## 2026-07-20 — fiber scheme

- Computed a lexicographic Gröbner basis over `QQ`:

  ```text
  [z - 27*x^2/4 + 1/4, y + 3*x/2, x^3 - x].
  ```

- Verified ideal equality in Magma, dimension zero, vector-space length three,
  and radicality.  This upgrades “three known preimages” to “exactly three
  reduced preimages” for the chosen target.

## 2026-07-20 — normalization and generic degree

- Applied the inverse of the linear part, then diagonal conjugation, to produce
  an integer-coefficient map `H` with `det JH=1` and `dH_0=I`.
- Eliminated the auxiliary coordinate from the rational normal form.  The
  inverse `x` coordinate obeys an explicit depressed cubic.
- Found the stronger binary-cubic model: source points are normalized marked
  simple roots.  This proves generic degree three, gives all inverse branches,
  classifies every fiber as size `3`, `1`, or `0`, and identifies the omitted
  triple-root curve.
- Computed the binary-cubic discriminant and proved it is exactly the
  nonproperness hypersurface using an explicit uniform escape family and the
  proper projective root incidence off the discriminant.
- Verified the nonproper escape curve `(s,-1/s,5/s^2) -> (0,2/s,0)` and recorded
  why nonproperness is evidence for, not an objection to, the counterexample.

## 2026-07-20 — artifact construction

- Built a single-source knowledge tree that opens as an Obsidian vault and
  builds as a Jupyter Book.
- Added exact SymPy, SageMath, and Magma programs, pytest integration, CI, and
  reproducibility metadata.
- GitHub CLI 2.96.0 was installed, but `gh auth status` reported that the active
  account `nasqret` had an invalid token.  Local Git work proceeded independently.

## 2026-07-20 — final local validation

- SymPy certificate: pass.
- SageMath 10.8 certificate: pass.
- Magma V2.22-3 suite: all five certificate files pass.
- Pytest: `8 passed`.
- Clean Jupyter Book build: success with zero warnings.
- GitHub SSH handshake authenticated as `nasqret`; API-backed repository
  creation remained blocked by the expired `gh` token and absence of a
  connected in-app browser.

## 2026-07-20 — private publication

- Refreshed GitHub authorization through the official device-login flow.
- Initialized local branch `main` and committed the complete audited tree as
  `e88224c`.
- Created the private repository
  `https://github.com/nasqret/jacobian-counterexample` and pushed `main` over
  the already-validated SSH transport.
