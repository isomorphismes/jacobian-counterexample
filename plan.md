# Research and dissemination plan

Status date: 2026-07-20.

## Acceptance gates

- [x] Freeze the exact submitted formula and coordinate order.
- [x] Verify the determinant over `QQ` in three computer algebra systems.
- [x] Verify the collision by exact substitution.
- [x] Replace raw CAS expansion with a short human-readable determinant proof.
- [x] Determine the entire scheme-theoretic target fiber.
- [x] Normalize to determinant `1`, identity linear part, and integer
  coefficients.
- [x] Extend the counterexample explicitly to every `n >= 3`.
- [x] Derive the generic inverse cubic and prove generic degree `3`.
- [x] Exhibit and interpret a nonproper escape curve.
- [x] Audit pre-announcement literature and current online provenance.
- [x] Build Obsidian, Jupyter Book, SymPy, SageMath, and Magma artifacts.
- [x] Validate all exact certificates, the notebook, tests, and a clean book build.
- [x] Publish the committed tree to the private GitHub repository
  `nasqret/jacobian-counterexample`.
- [x] Audit the 2026 literature frontier for the plane case, separating
  peer-reviewed theorems from preprints and failed proof claims.
- [x] Prove that every plane Keller map affine-linear in one source variable is
  triangular.
- [x] Prove the marked affine-two-plane odd-valuation obstruction in every
  binary-form degree.
- [x] Exclude every polynomial graph restriction and rank-two linear target
  projection of the threefold counterexample.
- [x] Exclude arbitrary nonlinear target polynomial pairs on the natural
  quadratic collision graph by the exact three-tangent relation.
- [x] Exclude the natural homogeneous triangular nonlinear target slices by
  computing their torus-invariant zero-fiber quotients.
- [x] Compute and certify the noninjective equivariant plane quotient with
  square Jacobian defect.
- [x] Construct and certify the octahedral degree-six cusp near-model and
  exclude its full function-field extension by normalization.
- [x] Audit Aaron Lou's factorization derivation and prove its exact left--right
  linear equivalence to the canonical threefold map.
- [x] Verify and document that Alpöge's formula, Jiang's projective
  symmetric-product model, Lou's resultant chart, and the intrinsic
  marked-root model present the same morphism up to source--target
  isomorphism; record their distinct provenance.
- [x] Derive and certify the general coefficient--resultant determinant law and
  identify the consecutive `(2,3)` split as the clean degree-ten plane route.
- [x] Exclude the connected Bring--Jerrard factor surface by Euler
  characteristic and exclude natural monic coefficient slices by units.
- [x] Construct and certify the noninjective quadratic-factor `A^2` scaffold
  and reduce its Keller condition to one explicit Poisson equation.
- [x] Identify that scaffold with Miyanishi's standard Galois affine
  pseudo-covering of the exceptional pseudo-plane `S(2,2,1)` and audit the
  Dubouloz--Palka etale endomorphism formulas.
- [x] Extract the resulting constant-Jacobian rational plane pair and certify
  its exact, boundary-supported pole.
- [x] Exclude constant mates for all three pseudo-plane generators, every
  homogeneous pair, and every pair of ambient total degree at most two.
- [x] Exclude the published equivariant Chebyshev endomorphisms and their
  standard deformation family by the omitted-line criterion.
- [ ] Obtain at least two named, independent human checks outside this
  repository.
- [ ] Freeze a public timestamp or archival DOI after attribution is confirmed.
- [ ] Submit a short note to a suitable peer-reviewed journal.

## Immediate dissemination checklist

1. Ask the announcer to confirm the exact formula and preferred attribution.
2. Send `knowledge/_build/html/` and the Magma/Sage/SymPy certificates to
   specialists in polynomial automorphisms.
3. Ask independent checkers specifically to audit the chain-rule determinant
   proof and the normalization, not just rerun the same CAS command.
4. Separate the one-page mathematical certificate from the historical and AI
   provenance narrative.
5. Update the literature page as a preprint, DOI, erratum, or priority claim
   appears.

## Research questions opened by the example

- Reconstruct the low-parameter search family of maps linear in `z` from which
  this example arose.
- Determine the full nonproperness set and the image complement.
- Describe the monodromy of the generic cubic cover.
- Apply Bass--Connell--Wright stabilization explicitly and minimize the
  dimension of a cubic homogeneous counterexample.
- Search for lower total degree or coefficient height in dimension `3`.
- Test whether analogous “unimodular row” constructions can or cannot descend
  to dimension `2`.
- Solve or structurally obstruct `{U,V}=1` in the explicit quartic
  factor-invariant ring, starting at its elliptic singular curve.
- Search the Belyi--Shabat endomorphisms of `X^2*Y=Z^2-1` for a noninvertible
  map `E` with `E^{-1}({X=0,Z=-1})` contained in that omitted line.  Such a map
  would restrict to a polynomial plane Keller counterexample; the basic
  degree-two family fails because `Z=0` maps into the omitted line.
- Build a sparse mixed, nonhomogeneous cubic Poisson ansatz on `S(2,2,1)`,
  using the two Darboux charts and their inverse-square transition to impose
  regularity before solving coefficient equations.
- Search nonlinear quadratic--cubic coefficient surfaces that cross the
  marked-factor leading-coefficient boundary; screen them first by units,
  Euler characteristic, connectedness, and finite-field point counts.
- Classify degree-six cusp passports and the finite normal surfaces realizing
  them; search for a normalization with a proper `A^2` Keller open.
- Compute boundary divisor class groups and log-canonical data for those
  normalizations.
- Encode the integral Newton-chain recurrences for the surviving `(72,108)`
  configuration and eliminate chains with exact certificates.

## Publication policy

The exact algebra can be stated decisively.  Priority, attribution, and claims
about community acceptance must remain dated and source-qualified until the
record stabilizes.
