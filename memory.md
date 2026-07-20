# Research memory

Last curated: 2026-07-20, Europe/Warsaw.

## Durable conclusion

The submitted formula is a genuine polynomial Keller map over `Q` with
constant Jacobian determinant `-2` and a non-singleton fiber.  It therefore
refutes the standard Jacobian conjecture in dimension `3`, conditional only on
the formula being transcribed exactly as displayed.  Cartesian product with an
identity map gives counterexamples in all dimensions `n >= 3`.  It says nothing
by itself about dimension `2`.

## Canonical map and target

Use the coordinate order `(x,y,z)` and the output order `(F1,F2,F3)` exactly as
in [map-definition.md](knowledge/map-definition.md).  The certified target is
`q = (-1/4,0,0)`.

The exact fiber ideal over `Q` is

```text
(F1 + 1/4, F2, F3)
  = (z - 27*x^2/4 + 1/4, y + 3*x/2, x^3 - x).
```

This proves that the fiber has length three and consists precisely of the three
listed rational points.  Because `x^3-x` is square-free in characteristic zero,
the fiber is reduced.

## Human determinant certificate

On the dense open set `x != 0`, set

```text
u = 1 + x*y,
w = x^2*z + 3*x*y - 2.
```

The source change `(x,y,z) -> (x,u,w)` has determinant `x^3`.  Define

```text
a = u^3*w + u*(u+1),
b = 3*u^2*w + 4*u + 2.
```

Then

```text
F1 = a/x^2,   F2 = b/x,   F3 = -x*w.
```

Direct differentiation gives `det(dF/d(x,u,w)) = -2/x^3`; the chain rule gives
`det JF = -2` for `x != 0`, hence everywhere because both sides are
polynomials.  The full derivation is in
[structural-certificate.md](knowledge/structural-certificate.md).

## Strong normalization

Let `L(x,y,z)=(z,y,2x)`, the linear part of `F`, and let
`D=diag(2,1,1)`.  Then

```text
G = L^(-1) o F = (F3/2,F2,F1),
H = D^(-1) o G o D.
```

`H` has integer coefficients, `det JH=1`, and `dH_0=I`.  Its explicit formula
and collision are in [normalization.md](knowledge/normalization.md).

## New structural facts derived in this audit

For a target `(a,b,c)`, define

```text
Q(U,V) = c*U^3 - 2*U^2*V + b*U*V^2 - 2*a*V^3.
```

With `(A,B,C)=F(x,y,z)`, `U=1+xy`, and `V=x`, the polynomial identities
`Q=0`, `Q_U=2V`, and `Q_V=-2U` hold.  Thus the source is the space of target
cubics with a marked simple projective root, and `F` forgets that root.

For a finite root `w` of

```text
p(w) = c*w^3 - 2*w^2 + b*w - 2*a,
```

put `h=p'(w)/2`.  Its unique preimage is

```text
x=1/h,  y=w-h,  z=5*h^2-3*w*h-c*h^3.
```

The root at infinity, present exactly when `c=0`, gives
`(0,b,a-4*b^2)`.  Hence fibers have cardinalities `3`, `1`, or `0` according
as the cubic has three simple roots, a double and a simple root, or a triple
root.  The geometric degree is exactly `3`.

The image complement is the triple-root curve

```text
(a,b,c) = (rho^2/3, 2*rho, 2/(3*rho)),  rho != 0.
```

The nonproperness set is the discriminant hypersurface

```text
b^2-c*b^3-16*a+18*a*b*c-27*a^2*c^2 = 0.
```

See [generic-fiber.md](knowledge/generic-fiber.md) and
[infinity.md](knowledge/infinity.md).

The rational escape curve

```text
(x,y,z) = (s,-1/s,5/s^2)
```

satisfies `F=(0,2/s,0)`.  It proves nonproperness as `|s| -> infinity`.  This
does not rescue the conjecture: properness is an extra sufficient hypothesis,
not part of the Keller condition.

## Dimension-two attack

The plane conjecture remains unresolved.  The threefold construction does not
descend by any of its natural low-complexity routes:

- a plane Keller coordinate affine-linear in one source variable forces a
  triangular automorphism;
- for every affine two-plane of binary forms in the root chart `w=y+1/x`, the
  differentiated root equation gives `D(w)*J(A,B)=s*s_x`; a nonzero constant
  Jacobian would make a rational square equal to a function with an odd
  valuation;
- restricting the threefold map to any polynomial graph `z=g(x,y)` and taking
  any rank-two constant linear target projection leaves a unique nonzero
  highest Jacobian term;
- on the interpolating graph `z=(27*x^2-1)/4`, the tangent-minor rows at the
  three collision points obey `M_+ + M_- + 106*M_0=0`; because the target
  two-form is identical at a common image, this excludes arbitrary nonlinear
  target polynomial pairs with nonzero constant restricted Jacobian;
- the homogeneous target shears `A+B^2*phi(B*C)` and
  `B+A*C*psi(A*C^2)` never pull back to source coordinates: their invariant
  zero-fiber quotients are not `A^1` (two infinity points or a nonconstant
  unit);
- no nonzero linear combination of `F1,F2,F3` is a coordinate, by exact fiber
  topology and unit arguments.

The `C*` weights `(1,-1,-2)` on the source and `(-2,-1,1)` on the target give a
new explicit plane quotient.  With `u=xy`, `v=x^2*z`, `c=2-3*u-v`, it is a
noninjective polynomial map with determinant `-2*c^2`.  It factors through

```text
G(X,Y) = (X*Y + Y^2 - Y^3, 2*X + 4*Y - 3*Y^2),
det JG = -2*X,
G(0,0) = G(2,2).
```

An independent degree-six cusp model is

```text
U = x^2 - 16*x*y + 16*y^2,
V = x^3 + 30*x^2*y - 96*x*y^2 + 64*y^3,
det J(U,V) = 108*x^3,
V^2 - U^3 = 108*x^4*y*(x-y).
```

It realizes the octahedral passport `(2^3),(3^2),(4,1,1)` but its finite
normalization is again `A^2`; Zariski Main plus Ax--Grothendieck excludes the
entire function-field extension from being reparametrized into a plane Keller
counterexample.  A viable degree-six construction therefore needs a finite
normalization `Y != A^2` with a proper `A^2` open and nontrivial boundary
divisor classes.

The current literature filter is geometric degree at least six.  The strongest
quantitative bound located is a preprint bound of maximum coordinate degree at
least `108`, with `(72,108)` the only surviving pair below `125`.  These status
claims and their peer-review labels are recorded in
[plane-status.md](knowledge/plane-status.md).

## Verification state

- SymPy exact determinant, points, both inverse charts, normalization, fiber
  ideal, nonproperness family, and Weyl relations: passing.
- SageMath exact determinant, fiber ideal, elimination, binary cubic, omitted
  target, and normalization: passing.
- Magma V2.22-3 direct, weighted, fiber, normalization, binary-cubic, and
  omitted-target certificates: passing.
- Plane quotient, marked-plane, linear and equivariant nonlinear slice,
  collision-tangent, and octahedral cusp identities: passing in SymPy, with
  both explicit near-models independently checked in Magma.
- Sage normalized collision ideal through total degree three: unit ideal.
- Pytest: fourteen exact certificate tests after the plane artifacts were added.
- Jupyter Book 1.0.0 HTML build: passing with zero warnings.
- Private GitHub repository published on branch `main`:
  `https://github.com/nasqret/jacobian-counterexample`.

## Source hygiene

Do not use arXiv:2209.01451 as authority for the conjecture's status or for the
injectivity equivalence.  It is a claimed proof preprint, not an accepted
resolution, and is unnecessary here.  Prefer Bass--Connell--Wright, van den
Essen, the recent refereed historical paper, and the exact primary announcement
links recorded in [literature-audit.md](knowledge/literature-audit.md).
