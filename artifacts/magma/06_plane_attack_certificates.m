// Exact certificates for the plane quotient and degree-six cusp near-model.
// These identities are research progress, not a solution of the plane
// Jacobian conjecture.

Qq := Rationals();

R<u, v> := PolynomialRing(Qq, 2);
c := 2 - 3*u - v;
a := (1 + u)^3*v + u^2*(1 + u)*(4 + 3*u);
b := u + 3*(1 + u)^2*v + 3*u^2*(4 + 3*u);
p := a*c^2;
q := b*c;
jacobian_quotient := Derivative(p, 1)*Derivative(q, 2)
    - Derivative(p, 2)*Derivative(q, 1);
assert jacobian_quotient eq -2*c^2;

X := c;
Y := c*(u + 1);
assert p eq X*Y + Y^2 - Y^3;
assert q eq 2*X + 4*Y - 3*Y^2;
assert Evaluate(p, [ Qq | 0, 0 ]) eq 0;
assert Evaluate(q, [ Qq | 0, 0 ]) eq 0;
assert Evaluate(p, [ Qq | -3/2, 13/2 ]) eq 0;
assert Evaluate(q, [ Qq | -3/2, 13/2 ]) eq 0;

S<X0, Y0> := PolynomialRing(Qq, 2);
G1 := X0*Y0 + Y0^2 - Y0^3;
G2 := 2*X0 + 4*Y0 - 3*Y0^2;
jacobian_cubic := Derivative(G1, 1)*Derivative(G2, 2)
    - Derivative(G1, 2)*Derivative(G2, 1);
assert jacobian_cubic eq -2*X0;
assert Evaluate(G1, [ Qq | 0, 0 ]) eq 0;
assert Evaluate(G2, [ Qq | 0, 0 ]) eq 0;
assert Evaluate(G1, [ Qq | 2, 2 ]) eq 0;
assert Evaluate(G2, [ Qq | 2, 2 ]) eq 0;

T<t> := PolynomialRing(Qq);
P := 64*t^3 - 96*t^2 + 30*t + 1;
Q := 16*t^2 - 16*t + 1;
assert P^2 - Q^3 eq 108*t*(1 - t);
assert 2*Q*Derivative(P) - 3*Derivative(Q)*P eq 108;

W<x, y> := PolynomialRing(Qq, 2);
sextic_u := x^2 - 16*x*y + 16*y^2;
sextic_v := x^3 + 30*x^2*y - 96*x*y^2 + 64*y^3;
jacobian_sextic := Derivative(sextic_u, 1)*Derivative(sextic_v, 2)
    - Derivative(sextic_u, 2)*Derivative(sextic_v, 1);
assert jacobian_sextic eq 108*x^3;
assert sextic_v^2 - sextic_u^3 eq 108*x^4*y*(x - y);

// The natural quadratic graph has a first-order obstruction for arbitrary
// nonlinear target polynomials, not only for linear target projections.
GraphRing<xg, yg> := PolynomialRing(Qq, 2);
zg := (27*xg^2 - 1)/4;
Ug := 1 + xg*yg;
Ag := Ug^3*zg + yg^2*Ug*(4 + 3*xg*yg);
Bg := yg + 3*xg*Ug^2*zg + 3*xg*yg^2*(4 + 3*xg*yg);
Cg := 2*xg - 3*xg^2*yg - xg^3*zg;
JAB := Derivative(Ag, 1)*Derivative(Bg, 2)
    - Derivative(Ag, 2)*Derivative(Bg, 1);
JAC := Derivative(Ag, 1)*Derivative(Cg, 2)
    - Derivative(Ag, 2)*Derivative(Cg, 1);
JBC := Derivative(Bg, 1)*Derivative(Cg, 2)
    - Derivative(Bg, 2)*Derivative(Cg, 1);
row0 := [ Evaluate(f, [ Qq | 0, 0 ]) : f in [ JAB, JAC, JBC ] ];
row_plus := [ Evaluate(f, [ Qq | 1, -3/2 ]) : f in [ JAB, JAC, JBC ] ];
row_minus := [ Evaluate(f, [ Qq | -1, 3/2 ]) : f in [ JAB, JAC, JBC ] ];
assert row0 eq [ Qq | 0, 0, -2 ];
assert row_plus eq [ Qq | -81/8, -3/2, 106 ];
assert row_minus eq [ Qq | 81/8, 3/2, 106 ];
assert [ row_plus[i] + row_minus[i] + 106*row0[i] : i in [1..3] ]
    eq [ Qq | 0, 0, 0 ];

// Invariant zero-fiber equations for the closest equivariant nonlinear
// slices.  The first identity also exposes the exceptional lambda=-1/12
// completion used in the written obstruction.
InvRing<lambda, ui, vi> := PolynomialRing(Qq, 3);
Ui := 1 + ui;
ai := Ui^3*vi + ui^2*Ui*(4 + 3*ui);
bi := ui + 3*Ui^2*vi + 3*ui^2*(4 + 3*ui);
ci := 2 - 3*ui - vi;
kA := ai + lambda*bi^2;
kB := bi + lambda*ai*ci;
assert 3*ai eq (bi - ui)*Ui;
assert Evaluate(kA, [ InvRing | lambda, -1, vi ]) eq 4*lambda;
assert Evaluate(kB, [ InvRing | lambda, -1, vi ]) eq 2;
assert 12*(ai - bi^2/12) eq 4*Ui - (bi - 2*Ui)^2;

print "PASS: plane quotient, nonlinear descent, and octahedral cusp identities verified.";
