// Direct exact-arithmetic verification of the proposed Keller map.
// This file is self-contained and has been tested in Magma V2.22-3.

Q := Rationals();
R<x, y, z> := PolynomialRing(Q, 3);

F1 := (1 + x*y)^3*z + y^2*(1 + x*y)*(4 + 3*x*y);
F2 := y + 3*x*(1 + x*y)^2*z + 3*x*y^2*(4 + 3*x*y);
F3 := 2*x - 3*x^2*y - x^3*z;
F := [ R | F1, F2, F3 ];

J := Matrix(R, 3, 3,
    [ Derivative(F[i], j) : i in [1..3], j in [1..3] ]);

assert Determinant(J) eq R ! -2;
assert [ TotalDegree(f) : f in F ] eq [ 7, 6, 4 ];

q14 := (Q ! 1)/(Q ! 4);
half := (Q ! 1)/(Q ! 2);

P0 := [ Q | 0, 0, -q14 ];
Pplus := [ Q | 1, -3*half, 13*half ];
Pminus := [ Q | -1, 3*half, 13*half ];
target := [ Q | -q14, 0, 0 ];

assert P0 ne Pplus and P0 ne Pminus and Pplus ne Pminus;
assert [ Q | Evaluate(f, P0) : f in F ] eq target;
assert [ Q | Evaluate(f, Pplus) : f in F ] eq target;
assert [ Q | Evaluate(f, Pminus) : f in F ] eq target;

print "PASS: direct determinant and three preimages verified over Q.";
