// Exact certificate for the preferred integral normalization.
//
// Let L(x,y,z)=(z,y,2*x) be the linear part of the canonical map and
// D=diag(2,1,1).  The map below is
//
//     H = D^(-1) o L^(-1) o F o D.
//
// Thus it has determinant one and identity linear part.  The assertions
// also certify a three-point fiber after the same linear change of variables.

Zints := Integers();
R<X, Y, Z> := PolynomialRing(Zints, 3);

T := 1 + 2*X*Y;
H1 := X - 3*X^2*Y - 2*X^3*Z;
H2 := Y + 6*X*T^2*Z + 6*X*Y^2*(4 + 6*X*Y);
H3 := T^3*Z + Y^2*T*(4 + 6*X*Y);
H := [ R | H1, H2, H3 ];

// Certify the stated linear conjugation directly, without expanding it by
// hand.  Multiplication by 4 in the first identity keeps the calculation in
// Z[X,Y,Z].
F1 := (1 + X*Y)^3*Z + Y^2*(1 + X*Y)*(4 + 3*X*Y);
F2 := Y + 3*X*(1 + X*Y)^2*Z + 3*X*Y^2*(4 + 3*X*Y);
F3 := 2*X - 3*X^2*Y - X^3*Z;
scaled_source := [ R | 2*X, Y, Z ];

assert 4*H1 eq Evaluate(F3, scaled_source);
assert H2 eq Evaluate(F2, scaled_source);
assert H3 eq Evaluate(F1, scaled_source);

JH := Matrix(R, 3, 3,
    [ Derivative(H[i], j) : i in [1..3], j in [1..3] ]);
assert Determinant(JH) eq R ! 1;

origin := [ Zints | 0, 0, 0 ];
assert [ Zints | Evaluate(h, origin) : h in H ] eq origin;
JH_at_origin := Matrix(Zints, 3, 3,
    [ Evaluate(JH[i,j], origin) : i in [1..3], j in [1..3] ]);
assert JH_at_origin eq IdentityMatrix(Zints, 3);

Q := Rationals();
q14 := (Q ! 1)/(Q ! 4);
half := (Q ! 1)/(Q ! 2);

P0 := [ Q | 0, 0, -q14 ];
Pplus := [ Q | half, -3*half, 13*half ];
Pminus := [ Q | -half, 3*half, 13*half ];
target := [ Q | 0, 0, -q14 ];

assert P0 ne Pplus and P0 ne Pminus and Pplus ne Pminus;
assert [ Q | Evaluate(h, P0) : h in H ] eq target;
assert [ Q | Evaluate(h, Pplus) : h in H ] eq target;
assert [ Q | Evaluate(h, Pminus) : h in H ] eq target;

print "PASS: preferred determinant-one identity-linear-part normalization verified.";
