// Exact binary-cubic and omitted-value certificates.
//
// For an output (a,b,c), consider the binary cubic
//
//   Q(U,V) = c*U^3 - 2*U^2*V + b*U*V^2 - 2*a*V^3.
//
// At every source point put U=1+x*y and V=x.  The three identities checked
// below expose the construction behind the canonical Keller map.

Qq := Rationals();
R<x, y, z> := PolynomialRing(Qq, 3, "lex");

F1 := (1 + x*y)^3*z + y^2*(1 + x*y)*(4 + 3*x*y);
F2 := y + 3*x*(1 + x*y)^2*z + 3*x*y^2*(4 + 3*x*y);
F3 := 2*x - 3*x^2*y - x^3*z;

S<a, b, c, U, V> := PolynomialRing(Qq, 5);
binary_cubic := c*U^3 - 2*U^2*V + b*U*V^2 - 2*a*V^3;
binary_cubic_U := Derivative(binary_cubic, 4);
binary_cubic_V := Derivative(binary_cubic, 5);

// Euler's identity is an independent sanity check on variable order and
// differentiation in the binary-cubic ring.
assert U*binary_cubic_U + V*binary_cubic_V eq 3*binary_cubic;

source_substitution := [ R | F1, F2, F3, 1 + x*y, x ];
assert Evaluate(binary_cubic, source_substitution) eq R ! 0;
assert Evaluate(binary_cubic_U, source_substitution) eq 2*x;
assert Evaluate(binary_cubic_V, source_substitution) eq -2*(1 + x*y);

// The target (1/3,2,2/3) is omitted.  Its specialized cubic is
// (2/3)*(U-V)^3.  The direct fiber ideal is the unit ideal, so this is a
// scheme-theoretic exact certificate rather than a numerical search.
third := (Qq ! 1)/(Qq ! 3);
omitted_target := [ Qq | third, 2, 2*third ];
specialized_cubic := Evaluate(binary_cubic,
    [ S | omitted_target[1], omitted_target[2], omitted_target[3], U, V ]);
assert 3*specialized_cubic eq 2*(U - V)^3;

omitted_fiber := ideal< R |
    F1 - omitted_target[1],
    F2 - omitted_target[2],
    F3 - omitted_target[3]
>;
unit_ideal := ideal< R | R ! 1 >;
assert omitted_fiber eq unit_ideal;

// A smaller consequence certificate mirrors the hand obstruction.  For the
// specialized cubic, Q_U=2*V and Q_V=-2*U force U=V=0, whereas the source
// chart U=1+x*y, V=x never contains that pair.
specialized_U := Derivative(specialized_cubic, 4);
specialized_V := Derivative(specialized_cubic, 5);
chart_substitution := [ R | 0, 0, 0, 1 + x*y, x ];
chart_obstruction := ideal< R |
    Evaluate(specialized_U, chart_substitution) - 2*x,
    Evaluate(specialized_V, chart_substitution) + 2*(1 + x*y)
>;
assert chart_obstruction eq unit_ideal;

print "PASS: binary-cubic identities and omitted-target unit ideal verified.";
