// Exact ideal certificate for the fiber over (-1/4, 0, 0).
// The triangular presentation proves that this fiber consists of exactly
// three reduced Q-rational points.

Q := Rationals();
R<x, y, z> := PolynomialRing(Q, 3, "lex");

F1 := (1 + x*y)^3*z + y^2*(1 + x*y)*(4 + 3*x*y);
F2 := y + 3*x*(1 + x*y)^2*z + 3*x*y^2*(4 + 3*x*y);
F3 := 2*x - 3*x^2*y - x^3*z;

q14 := (Q ! 1)/(Q ! 4);
fiber_ideal := ideal< R | F1 + q14, F2, F3 >;
triangular_ideal := ideal< R |
    4*z - 27*x^2 + 1,
    2*y + 3*x,
    x*(x - 1)*(x + 1)
>;

assert fiber_ideal eq triangular_ideal;
assert Dimension(fiber_ideal) eq 0;
assert IsRadical(fiber_ideal);

P0 := [ Q | 0, 0, -q14 ];
Pplus := [ Q | 1, -3/2, 13/2 ];
Pminus := [ Q | -1, 3/2, 13/2 ];

for p in [ P0, Pplus, Pminus ] do
    assert forall{ g : g in Basis(fiber_ideal) | Evaluate(g, p) eq 0 };
end for;

print "PASS: target fiber has the certified triangular ideal.";
