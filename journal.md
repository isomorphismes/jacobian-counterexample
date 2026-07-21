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

## 2026-07-20 — Lou factorization audit and plane resultant attack

- Downloaded Aaron Lou's six-page derivation, extracted its text, rendered all
  six pages with Poppler, and visually inspected every page under the PDF
  verification workflow.
- Proved by exact expansion that Lou's map is `R o F o S`, where
  `S(x,y,z)=(x,y,-z)` and `R(A,B,C)=(C,B,A)`.  Its product cubic is the existing
  marked binary cubic after the corresponding sign change.
- Generalized the PDF's 5-by-5 determinant to
  `det D(coeff(PQ),Res(P,Q))=+/-(s-r)Res(P,Q)^2` using root coordinates and
  Vandermonde determinants.  Exact symbolic cases include `(1,1)`, `(1,2)`,
  `(1,3)`, and `(2,3)`.
- Identified quadratic-times-cubic factorization as the clean direct plane
  blueprint: resultant weight one, generic degree ten, and no residual scaling
  gauge.  Proved that the Bring--Jerrard slice is connected with
  `chi_c=0`, and derived unit obstructions for fixed top and middle coefficient
  slices in the monic quadratic chart.
- Constructed the normalized two-quadratic Danielewski surface and its exact
  `A^2` chart.  The induced product-coefficient map has the collision
  `(1,0),(-1,-2) -> (-1,-1,-1/4)` and a symplectic rational complement-factor
  involution.  Reduced the missing Keller condition first to `{U,V}=1` on the
  smooth surface `B^2=a+a^2*C`, and then to the narrower conductor-descent
  equation in `C[p,q,r]/(H)`.
- Found the exact identity expressing `1` as a sum of three degree-two brackets
  on the smooth surface.  It is not one bracket and hence not a solution, but
  it rules out a purely de Rham-cohomological obstruction.
- Excluded every linear target projection and, by exact rational linear
  algebra, excluded a constant from the span of all brackets through target
  degree three.  Small-finite-field counts were added as a heuristic sieve for
  sparse quintic coefficient planes.
- Audited the same-day weighted-lift follow-on.  Its plane core has determinant
  defect `-c*gamma`; the log-symplectic chart cancels the defect but introduces
  poles, while the third weighted scale in dimension three polynomializes it.
- Added exact SymPy and Magma certificates, bounded-search code, an Obsidian and
  Jupyter Book chapter, and updates to the durable memory and research plan.
- Recognized the smooth target as the classical affine pseudo-plane
  `S(2,2,1)`.  More precisely, the resultant-one factor surface is the
  universal cover `X^2*Y=Z^2-1`, the source plane is its complement of the line
  `X=0,Z=-1`, and the map to `B^2=a+a^2*C` is the standard `Z/2` quotient.
  Thus the construction exactly recovers Miyanishi's Galois affine
  pseudo-covering framework for a hypothetical split plane Keller map.
- Verified that this is the exceptional pseudo-plane type `r=2`: its canonical
  class vanishes, so the usual canonical-divisor obstruction is silent.
  Dubouloz--Palka construct nonproper etale self-maps of this surface, but not
  the needed map from it to `A^2`; the 2026 Borisov--Gabber--Vasiu manuscript
  explicitly records this exceptional direction as conditional on the plane
  Jacobian conjecture.
- Composed Dubouloz--Palka's basic open embedding with the inverse plane chart.
  This gives the exact rational pair
  `U=x*(1+x^2*y)`,
  `V=2*y*(2+x^2*y)/(1+x^2*y)^2`, with `J(U,V)=4` and the retained collision.
  Their standard deformation family only adds `P(U)` to `V`; the double pole
  on `1+x^2*y=0` remains.  Reformulated the next construction problem as
  finding a noninvertible etale endomorphism of the universal cover whose
  inverse image of the omitted line is contained in that line.
- Computed a two-chart Darboux atlas on the pseudo-plane; its transition has
  the exact inverse-square twist `Q=-2*p-1/q^2`.  Valuation and logarithmic
  residue arguments exclude constant Poisson mates for each generator
  `a,B,C` in all degrees.  A full weight classification excludes every
  homogeneous pair, and an exact coefficient ideal excludes all pairs of
  ambient total degree at most two.  The live search begins with mixed,
  nonhomogeneous cubic ansatzes.
- Audited the Chebyshev form of all equivariant universal-cover endomorphisms.
  Conjugation to the plane chart has constant Jacobian but a genuine pole for
  every degree greater than one.  The standard non-equivariant deformation
  automorphisms preserve the omitted boundary line, so the entire published
  family fails the boundary-avoidance requirement.

## 2026-07-20 — provenance and equivalence audit

- Verified the primary X posts and their exact UTC chronology.  Levent
  Alpöge's 02:19:17 post is the original public announcement located for the
  explicit formula, determinant, and collision; Andy Jiang's 12:02:19 post
  gives the projective symmetric-product construction and explicitly presents
  it as GPT output.
- Proved the exact comparison with the intrinsic model.  Normalizing the
  complement of Jiang's tangent nonosculating hyperplane gives the affine
  slice `H_tau`; deleting the projective ramification divisor says exactly
  that the marked root is simple.  Lou's resultant-one condition fixes the
  remaining factor-rescaling gauge.
- Corrected the terminology for Lou's coordinate formula: `G = R0 o F o S0`
  is left--right linear equivalence, not strict conjugacy, because the source
  and target changes are independent.
- Added both X posts to the literature database and placed role-specific
  citations in the paper, README, knowledge index, factorization chapter,
  research memory, and citation metadata.
- Recompiled the seven-page coordinate-free paper twice with all citations and
  cross-references resolved.  Rendered and visually inspected every page; no
  clipping, overlap, or bad bibliography break remains.  The final PDF text
  contains both credits and the explicit equivalence statement.
- Rebuilt the Jupyter Book with zero warnings and reran the exact test suite:
  `24 passed`.

## 2026-07-21 — unified paper and public explainer

- Compared the direct-coordinate working draft with the retained intrinsic
  paper and the three public presentations.  Designated
  `src/distinguished_root_map.tex` as the canonical seven-page synthesis and
  kept `marked_root_binary_cubic.pdf` as a labeled historical version 1.
- Separated contribution roles throughout: Alpöge's post supplies the explicit
  map and records its credit to Fable; Jiang's post supplies the projective
  marked-root construction and explicitly labels it GPT output; Lou supplies
  the factorization--resultant chart; Naskrecki is identified only with the
  repository compilation, audit, exposition, and landing page.
- Recorded the exact bridge between the two coordinate maps as
  `G=R0 o F o S0`.  Tightened the language after independent review: this
  displayed relation is left--right linear equivalence, not conjugacy by the
  same coordinate change; the repository makes no unproved global
  nonconjugacy claim.
- Strengthened the short paper's root-gradient scaling explanation, finite-flat
  degree-three sentence, and proof that the nonproperness set is precisely the
  cubic discriminant.  The final two-pass LaTeX build has seven A4 pages, no
  warnings or overfull boxes; every page was rendered and visually inspected.
- Built a responsive static landing page with a plain-language marked-root
  infographic, exact certificate, three-lens comparison, proof spine,
  role-specific provenance timeline, historical literature, public-license
  notices, and an accessible synchronized Three.js source/target viewer.
  Exact curve coordinates remain available when WebGL is absent.
- Generated a text-free abstract hero image for the project and preserved both
  the source PNG, optimized WebP, and generation prompt.  All spatial artifacts
  state that they show only `R^3` inside the six-real-dimensional `C^3`.
- Implemented a fourteen-section Manim Voiceover explainer driven by the same
  exact curve fixture as the browser.  Completed and inspected a 480p smoke
  render and a 1920x1080/30 fps release render.  The embedded 275.732-second
  MP4 uses a clearly disclosed offline Piper `en_US-libritts-high` speaker-0
  draft, progressive MP4 layout, and 104 nonoverlapping WebVTT cues whose text
  exactly equals the canonical narration.  Human narration remains preferred.
- Added MIT licensing for software and CC BY 4.0 for the paper, prose, diagrams,
  artwork, transcript, captions, and released film, while preserving distinct
  third-party terms for Piper, its voice model, LibriTTS, software, posts, and
  papers.
- Added publication-contract, animation, caption, media-integrity, TypeScript,
  browser, and Pages-assembly tests.  Browser QA covers desktop, a true
  390-pixel mobile viewport, reduced motion, transcript keyboard access, and
  the no-WebGL fallback with no unexpected console or request failures.
- Corrected the landing-page Keller, Bass--Connell--Wright, and Druzkowski DOI
  links against the canonical bibliography and verified the primary X posts,
  Lou PDF, and historical DOI resolvers from the release environment.
- Scanned every committed revision and the full release tree for common secret
  patterns and sensitive filenames.  No credential was found; the only
  personal metadata is the expected named Git commit identity already used by
  the repository owner.
- Closed the local release gate with all three exact algebra systems passing,
  `69` Python tests and `11` Vitest tests passing, a clean paper and Jupyter
  Book build, a zero-vulnerability npm audit, and desktop, mobile,
  reduced-motion, and WebGL-fallback browser checks.
- Published release commit `e27b8e6`, changed
  `nasqret/jacobian-counterexample` from private to public, enabled GitHub
  Pages with the committed custom workflow, and obtained green verification
  and deployment runs.
- Verified the public repository, landing page, PDF, Jupyter Book, WebVTT
  captions, and HTTP byte-range delivery of the MP4.  Repeated the complete
  browser suite against the live Pages URL in clean desktop, 390-pixel mobile,
  reduced-motion, and no-WebGL contexts with no console or request failures.

## 2026-07-21 — formula rendering and real-slice viewer revision

- Replaced formula-shaped Pango strings in the fourteen-section film with
  genuine Manim `MathTex`/`Tex` objects backed by one thirty-formula registry.
  All formulas passed TeX-to-SVG preflight, a formula-card render, and a full
  low-resolution scene smoke test.
- Rendered and inspected a new 1920-by-1080, 30 fps Piper-narrated release.
  The progressive H.264/AAC MP4 lasts 278.231380 seconds, decodes without
  errors, and remains synchronized with 104 nonoverlapping WebVTT cues.
- Converted the root README and twenty-one Jupyter Book chapters from raw
  parenthesis/bracket delimiters to GitHub- and MyST-native dollar math.  Added
  regressions for unmatched/nested delimiters, math-like code spans, malformed
  spacing commands, and bibliography math; the clean book build has no
  warnings.
- Rebuilt the real-slice viewer around a simultaneous eleven-line pencil and a
  775-vertex mapped surface mesh with three actual rulings.  Thick cores,
  additive halos, collision markers, improved lighting, and synchronized
  source/target framing make the geometry legible.
- Reduced viewer cost through intersection-triggered Three.js loading,
  event-driven rendering, memoized discretization, a capped device-pixel
  ratio, and a 1.35-million-pixel canvas budget.
- Independent integration review found and prompted fixes for nested display
  delimiters, missing TeX command slashes, mislabeled mesh rulings, and a zoom
  control state mismatch.  Dedicated regression tests now cover each class.
- Closed the nonvisual local gates with 75 Pytests, 17 Vitest tests, strict
  TypeScript, production assembly, clean Jupyter Book, and exact SymPy,
  SageMath, and Magma certificates passing.  The in-app browser exposed no
  session during this revision, so fresh interactive screenshots remain a
  clearly recorded follow-up rather than an inferred pass.

## 2026-07-21 — film typography revision

- Recorded Aaron Lou's X handle, [@aaron_lou](https://x.com/aaron_lou), in the
  canonical paper, knowledge book, website, transcript metadata, and visible
  film credits while leaving the spoken narration unchanged.
- Traced the film's irregular letter and word spacing to ManimPango shaping
  19--42 point prose at a very small internal size, which quantized glyph
  advances before the vectors reached the 1080p renderer.
- Bundled pinned Inter 4.001 with its SIL OFL 1.1 license and SHA-256, then
  generated reproducible `opsz=14`, `wght=400/700` static Modified Versions
  with the repository-unique family `Jacobian Counterexample Film Text`.
  OpenType names 16 and 17 make Pango select both faces; a render-time outline
  probe rejects silent fallback.  Registered both files from the repository
  and routed every prose object through one renderer that shapes at four times
  display size before uniform downscaling.  Mathematical formulas remain
  native `MathTex`/`Tex`.
- Pinned ManimPango, Pango, Cairo, and Pycairo to the versions used for the
  release.  Added source-policy, exact-font-integrity, and runtime-pin
  regressions so later edits cannot silently reintroduce platform-dependent
  prose or the undersampled path.
- Inspected a complete low-resolution smoke render, native 1080p samples from
  all fourteen sections, the densest labels, and the credits.  Also moved the
  resultant-one label away from a pre-existing card collision found during the
  audit.
- Fixed the Piper cache identity so unset optional synthesis controls survive
  Manim Voiceover's JSON normalization.  A real-cache probe now finds the
  stored clip without loading the voice model.
- Released a progressive 1920-by-1080, 30 fps H.264/AAC replacement lasting
  276.598698 seconds with 104 regenerated, nonoverlapping WebVTT cues.  The
  full media stream decodes without error and the caption text remains exactly
  equal to the canonical narration.

## 2026-07-21 — Litt pencil-bundle revision

- Recorded Daniel Litt's ([@littmath](https://x.com/littmath)) conceptual
  explanation of the marked-root source as an affine-line bundle over an
  affine plane, obtained from a family of pencils with a horizontal section
  and the diagonal deleted
  ([thread](https://x.com/littmath/status/2079347618417971212),
  [full gloss](https://x.com/littmath/status/2079353531430289734)).
- Preserved the provenance boundary: this explains the Jiang--GPT and
  Alpöge--Fable construction rather than introducing a fourth one. Litt also
  made that equivalence explicit in a later
  [comment](https://x.com/littmath/status/2079475742401003816).
- Recorded Litt's own statement that the gloss was developed with substantial
  [ChatGPT assistance](https://x.com/littmath/status/2079414119720165633).
  The canonical paper revision uses the geometry as motivation and retains
  the polynomial chart and inverse as the global proof that the source is
  affine three-space.
- Added exact SymPy regressions for the pencil identity, common base point,
  and affine-plane parametrization.  The verifier and all 78 Pytests pass;
  the Jupyter Book rebuilds cleanly, and the warning-free eight-page PDF was
  rendered and inspected page by page.
