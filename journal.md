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

## 2026-07-20 — full-force plane attack

- Re-audited the current plane literature.  The safe established covering
  constraint is geometric degree at least six.  The strongest degree-108
  statement remains a preprint; below degree 125 it leaves only `(72,108)`.
  Recorded the known gap in Żołądek's separate gcd theorem and did not use it.
- Proved that a plane Keller map with one coordinate affine-linear in a source
  variable is triangular.  This eliminates the most literal analogue of the
  threefold map's `z`-linearity.
- For an arbitrary affine two-plane of binary forms and the root chart
  `w=y+1/x`, derived `D(w) J(A,B)=s s_x`.  A Keller determinant would force a
  rational square to have an odd valuation, excluding cubics, quartics,
  sextics, and all higher degrees in this construction class.
- Proved by leading homogeneous terms that no polynomial graph `z=g(x,y)` and
  no rank-two linear projection of the three outputs can have constant plane
  Jacobian.  A separate exact Gröbner search rejected every quadratic graph
  through the known collision in all three projection charts.
- Strengthened the natural quadratic graph obstruction from linear projections
  to arbitrary target polynomials.  The three tangent-minor rows satisfy
  `M_+ + M_- + 106*M_0=0`; at a common target the same two-form must pair with
  all three, forcing `108*kappa=0`.
- Tested the most promising nonlinear target slice `A+lambda*B^2`.  Although a
  nonzero lambda fills the missing `1+xy=0` divisor of the linear slice, its
  invariant zero-fiber quotient has the nonconstant unit `1+u`.  Extended the
  obstruction to the full homogeneous triangular families
  `A+B^2*phi(B*C)` and `B+A*C*psi(A*C^2)` using two infinity points and units.
- Proved that no nonzero linear combination of the three outputs is a source
  coordinate, using an exact Laurent formula on the components of its
  `z`-coefficient curve and compactly supported Euler characteristic.
- Discovered the `C*` equivariance of the threefold map and descended it to a
  noninjective plane map with determinant `-2*(2-3*u-v)^2`.  Factored it through
  a noninjective cubic map with determinant `-2*X` and isolated a valuation
  mismatch that prevents the obvious rational pole cancellation.
- Constructed the octahedral degree-six cusp model from
  `P(t)^2-Q(t)^3=108*t*(1-t)`.  In its finite normalization coordinates its
  determinant is `108*x^3` and its cusp pullback is
  `108*x^4*y*(x-y)`.  Zariski Main and Ax--Grothendieck exclude every
  reparametrization of this exact extension as a Keller counterexample.
- Added exact SymPy, Sage, Magma, pytest, Obsidian, and Jupyter Book artifacts.
  The next concrete target is a degree-six normalization `Y != A^2` with a
  proper `A^2` open and nontrivial boundary divisor classes.
