# Plan for the synthetic discovery dialogue

## Purpose

Write a short, self-contained paper that asks a precise question:

> How short can a mathematically honest conversation be if its goal is to
> reconstruct the announced three-dimensional Keller counterexample without
> inserting its nonlinear coefficients or its known collision?

The paper is an expository reconstruction. It is not a transcript, a claim
about Fable's private run, or evidence about model training data. Its thesis is
conditional: after two natural modeling choices, the remaining narrowing is a
finite case test, elementary elimination, ordinary coordinate rescaling, and
one small exact calculation.

## Audience and notation budget

The intended reader is an advanced undergraduate or beginning graduate
student who knows polynomial maps, basic projective space, and determinants.
Every specialized word is translated before use:

- “generic degree” means the typical number of inverse images;
- “mark a root” means remember which linear factor was chosen;
- “resultant” means the polynomial test for a shared root;
- “linear affine chart” means the complement of one projective hyperplane;
- “matched coordinate rescaling” replaces “torus action”;
- “exact polynomial row reduction” introduces a Gröbner basis.

The dialogue will not use the repository-specific symbols
`M_{omega,tau}`, `X_tau`, “neutral gauge,” “error support,” or
“artificial-amnesia.” Locally nilpotent derivations, syzygy modules, the full
sixteen equations, and the full Gröbner basis remain outside the main
narrative.

## Epistemic convention

Each of the six exchanges has four parts:

1. a broad **User** question;
2. a short prose-first **Model** suggestion;
3. the minimum exact mathematics needed to justify it;
4. a **Checkpoint** with three fields:
   **Chosen**, **Deduced**, and **Still owed**.

This is the paper's Lakatos--Lamport superposition. The next user question
acts as an objection to the gap left by the previous answer; the checkpoint
makes all dependencies explicit. A front-page reader's contract states that
the final nonlinear numbers and the collision are hidden from the coefficient
reconstruction.

## The six exchanges

### 1. Why try three inverse images?

- Start with a Keller map and its typical finite fiber.
- Degree one is the inverse case; in characteristic zero degree two is Galois,
  and the known Galois case is invertible.
- **Choice:** test generic degree three, the first value not excluded this way.
- **Not claimed:** degree three is forced or guarantees a counterexample.

### 2. What familiar operation is naturally three-to-one?

- A cubic with three distinct roots has three possible remembered roots.
- Encode a remembered root as `C=LQ`, with `L` linear and `Q` quadratic.
- Forgetting `L` is three-to-one over a squarefree cubic.
- Require `L,Q` to share no root; normalize their resultant to one.
- **Choice:** the marked-cubic model.
- **Deduction:** three sheets and no local folding on the normalized locus.

### 3. Can both sides become ordinary three-space?

- **Choice:** search only standard linear affine charts in projective cubic
  space.
- A hyperplane meets the curve of triple-root cubics in exactly three
  multiplicity patterns: `1+1+1`, `2+1`, or `3`.
- An elementary additive count gives `0,1,0`; only `2+1` can be affine
  three-space.
- The next exchange must prove sufficiency by giving global coordinates.

### 4. Can the surviving source be parametrized without division?

- Choose the simple representative `c_2=1` and write
  `L=xT+beta S`, `Q=gamma T^2+delta TS+epsilon S^2`.
- The two level equations give `beta=1+xy` by one subtraction.
- One remaining affine coordinate gives explicit polynomial formulas for
  `gamma,delta,epsilon` and a polynomial inverse.
- Multiplication now constructs the map; its chart supplies the scaling rule,
  degree bounds `(7,6,4)`, linear dependence on `z`, and linear part
  `(z,y,2x)`.
- **Conventions:** the scale and sign of the last coordinate, output order,
  and factors of two.
- Mark the construction as complete here.

### 5. What remains after the nonlinear numbers are hidden?

- Retain only the scaling rule, degree bounds, `z`-linearity, linear part, and
  the nonvanishing of two endpoint coefficients inherited from the chart.
- Enumerate exactly sixteen monomial positions (`7+6+3`) instead of 239 dense
  positions.
- Fixing the three linear terms leaves thirteen unknown coefficients.
- Two matched source--target rescalings set the endpoint coefficients to one,
  leaving eleven unknowns.
- **Not claimed:** these restrictions hold for all Keller maps or describe the
  boundary where an endpoint coefficient vanishes.

### 6. Can exact algebra restore the numbers?

- Use `u=xy`, `v=x^2z` to reduce the Jacobian to one `3 x 3` determinant in
  two variables.
- Its sixteen nonconstant coefficients give sixteen equations in eleven
  unknowns.
- One exact Gröbner calculation has one set-theoretic complex solution; its
  quotient has length two, so “unique” is never called “reduced.”
- Undoing the two rescalings gives one orbit on the inherited nonzero stratum.
- No nonlinear coefficient and no collision equation enters the solve.
- Choosing a least-height integral representative is explicitly labeled a
  later presentation convention.

## Final conceptual section

After the dialogue, state the construction in one theorem:

> For a tangent but nonosculating linear chart, the normalized pairs
> `(L,Q)` with `Res(L,Q)=1` and `c_2(LQ)=1` form affine three-space.
> Multiplication `(L,Q) -> LQ` is an everywhere locally invertible polynomial
> map to affine three-space and is generically three-to-one.

Its proof uses only the global chart, the resultant determinant, and the three
possible markings of a cubic. Then display the explicit map and its
three-point fiber.

## Claim audit

The conclusion may say:

- the conditional derivation has six short conceptual moves;
- no nonlinear coefficient or collision is inserted in the exact solve;
- the two modeling choices are natural and textually describable;
- the final expanded formula is the coordinate shadow of a short geometric
  construction.

It may not say:

- that this was the historical Fable/LLM transcript;
- that degree three forces the marked-cubic model;
- that all affine models reduce to linear charts;
- that there was no ansatz or only one assumption;
- that discovery was inevitable, trivial, or computation-free;
- that the calculation classifies all Keller maps.

## Artifacts and verification

- LaTeX source: `src/six_questions_keller_map.tex`
- Final PDF: `output/pdf/six_questions_keller_map.pdf`
- Exact replay: `artifacts/sympy/verify_dialogue_reconstruction.py`
- Build target: `make dialogue-paper`
- Publication regression: source structure, six exchanges, reader's contract,
  attribution links, final PDF signature and size.
- Final gate: exact replay, full Pytest suite, clean Jupyter Book build,
  warning-free two-pass LaTeX build, Poppler rendering, and inspection of every
  page.
