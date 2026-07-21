# One map, three public descriptions

Status date: 20 July 2026. This note compares the two local paper drafts and
the three public presentations they synthesize. It separates mathematical
equivalence from provenance. It is not a priority determination.

## Short answer

The constructions are equivalent as presentations of one algebraic morphism:
forgetting a marked simple root of a binary cubic in a special affine slice.
They are **not** literally the same coordinate formula.  The displayed
identification between the polynomial maps usually denoted by $F$ and $G$ is
*left--right linearly equivalent*: independent linear changes are made in the
source and the target.  It is therefore not, as displayed, a dynamical
conjugacy by one common coordinate change.  No claim about the possible
existence of some other nonlinear conjugacy is needed here.

The public roles are distinct:

1. [Levent Alpöge's post](https://x.com/__alpoge__/status/2079028340955197566)
   gives the explicit polynomial formula, determinant, and collision, and
   credits Fable for working on it.
2. [Andy Jiang's post](https://x.com/davikrehalt/status/2079175065695035442)
   gives the projective symmetric-product construction and labels the text as
   GPT output.
3. [Aaron Lou's note](https://aaronlou.com/jacobian_counterexample_derivation.pdf)
   gives a factorization--resultant derivation and an explicit global affine
   chart.
4. This repository compares, verifies, and explains these presentations. Its
   compiler does not claim discovery of the formula or either construction.

## What the two retained paper artifacts contain

The live file `src/distinguished_root_map.tex` is now the revised canonical
synthesis.  An earlier working copy at that path was a longer direct-coordinate
draft; its useful material was absorbed into the canonical paper, and stale
descriptions of that working copy should not be applied to the current file.
The older coordinate-free paper is retained unchanged as historical version 1.

| Feature | Current canonical synthesis | Historical version 1 |
|---|---|---|
| Artifact | `src/distinguished_root_map.tex` and `output/pdf/one_map_three_descriptions.pdf` | `output/pdf/marked_root_binary_cubic.tex` and `.pdf` |
| Opening | Exact formula, determinant, collision, referee-status note | Intrinsic marked-root theorem and incidence variety |
| Expository order | Plain-language mechanism, then projective, resultant, and coordinate lenses | Coordinate-free construction first, coordinates later |
| Projective lens | Jiang--GPT symmetric-product map, with a beginner translation | Intrinsic affine normalization of Jiang's projective model |
| Resultant lens | Lou's gauge, kernel proof, and global chart | More detailed invariant resultant development and étaleness proof |
| Explicit lens | Alpöge--Fable formula plus the exact bridge $G=R_0FS_0$ | Recovers both coordinate orders after the intrinsic proof |
| Provenance | Role-specific statement on page one and in the bibliography | All three public sources recorded in a provenance paragraph |
| Best use | Short public entry point and comparison of the three approaches | Deeper coordinate-free reference |

There is no mathematical contradiction between the artifacts and no false
core identity was found.  The canonical synthesis keeps the historical
paper's invariant proof while adding the direct root-marking intuition, an
exact source--target equivalence statement, and a shorter beginner-first path.

## The shared morphism

Think of a cubic as three points of the projective line, counted with
multiplicity. Mark one root, then forget which root was marked:

```text
cubic + one marked simple root  ───────────────▶  cubic
                                      forget
```

A general cubic has three simple roots, so it has three possible markings.
The marking is deleted when the marked root becomes repeated. This removes
ramification upstairs without removing every corresponding limiting value
downstairs. The lost inverse branches therefore escape the affine chart
instead of meeting at a finite critical point.

Three languages describe that arrow:

| Lens | Source object | Map | What it explains fastest |
|---|---|---|---|
| Explicit algebra | $(x,y,z)\in\mathbf A^3$ | Alpöge's displayed $F$ | Exact determinant and three-point collision |
| Projective marked roots | $(p,\{q,r\})$ away from marked collisions | $(p,\{q,r\})\mapsto\{p,q,r\}$ | Degree three, ramification deletion, special hyperplane |
| Resultant-normalized factors | $C=\ell q$, $\operatorname{Res}(\ell,q)=1$ | $(\ell,q)\mapsto\ell q$ | Gauge fixing, affine chart, clean differential proof |

The coordinate-free incidence description used by this repository is a
synthesis of the last two lenses, not a fourth discovery claim.

## Exact bridge between the projective and resultant gauges

In the elementary draft, write

$$
L=vT-uS,\qquad Q=AT^2+BTS+CS^2,
$$

and normalize

$$
h=vB-uA=-2,\qquad r=Q(u,v)=2.
$$

Set

$$
\ell(T,S)=L(T,-S)=vT+uS,
\qquad q(T,S)=\tfrac12 Q(T,-S).
$$

Lou's factor coordinates are then

$$
x=v,\quad \beta=u,\quad \gamma=A/2,
\quad \delta=-B/2,\quad \varepsilon=C/2.
$$

The two normalizations become

$$
x\delta+\beta\gamma=-h/2=1,
$$

and

$$
\operatorname{Res}(\ell,q)
=x^2\varepsilon-x\beta\delta+\beta^2\gamma
=r/2=1.
$$

Thus the apparently different gauge conditions are identical after the
displayed sign and scale change.

At affine-chart level, put

$$
S_0(x,y,z)=(x,y,-z),
\qquad R_0(a,b,c)=(c,b,a).
$$

If $F$ is the explicit map in Alpöge's post and $G$ is the polynomial map
in the resultant chart, then exactly

$$
\boxed{G=R_0\circ F\circ S_0.}
$$

This is left--right equivalence. It preserves étaleness, geometric degree,
fiber cardinalities, and nonproperness.  The displayed relation is not a
conjugacy $G=L^{-1}FL$, because its source and target changes are different;
no stronger nonconjugacy assertion is being made.

## What is intrinsic and what is a choice

Intrinsic data:

- the forgetful marked-root morphism;
- deletion of precisely the repeated marked-root locus;
- generic degree three and the $3,1,0$ simple-root fiber counts;
- nonproperness along the discriminant;
- the omitted triple-root curve.

Coordinate choices:

- a basis of the two-dimensional vector space of linear forms;
- the particular tangent-but-not-osculating hyperplane;
- signs and scalar normalizations of forms and resultants;
- the order and scaling of the three target coordinates;
- the numerical constant appearing as the Jacobian determinant.

Every tangent-but-not-osculating hyperplane to the twisted cubic is equivalent
under a projective linear change of the underlying projective line. Those
choices change the formula, not the marked-root mechanism.

## Actual structure of the canonical paper

The canonical paper has a page-one certificate followed by six numbered
sections and no table of contents:

1. **Provenance and the three viewpoints.** It assigns the public roles,
   translates the minimum terminology, and displays one unifying diagram.
2. **Jiang--GPT: mark a root, then forget it.** It develops the symmetric-power
   map, the ramification deletion, and the tangent-but-not-osculating affine
   slice.
3. **Lou: fix the factorization gauge by a resultant.** It factors
   $C=\ell q$, imposes resultant one, proves étaleness by the kernel argument,
   and gives the global $\mathbf A^3$ chart.
4. **Alpöge--Fable: recovering the displayed formula.** It gives the exact
   sign-and-scale bridge, displays $G=R_0FS_0$, and recovers the determinant
   and collision.
5. **Fibers, the discriminant, and escape to infinity.** It gives the $3,1,0$
   set-theoretic counts, distinguishes the image from the properness set, and
   explains the escaping sheets.
6. **Scope, history, and reproducibility.** It records standard literature,
   the consequence for all dimensions at least three, the still-separate plane
   case, real-slice visualization limits, licenses, and reproducible artifacts.

This realized ordering keeps the shortest exact certificate on page one,
gives a nonexpert the root-marking metaphor before the invariant proof, and
lets experts reach the coordinate bridge without carrying two papers at once.

## Visualization warning

The map is defined on $\mathbf C^3$, which has six real dimensions. Every
three-dimensional plot in the website and animation shows only the real slice
$\mathbf R^3\subset\mathbf C^3$. It illustrates exact real curves and
points, but it is not a picture of the whole complex morphism.
