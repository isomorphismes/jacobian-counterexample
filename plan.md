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

## Publication policy

The exact algebra can be stated decisively.  Priority, attribution, and claims
about community acceptance must remain dated and source-qualified until the
record stabilizes.
