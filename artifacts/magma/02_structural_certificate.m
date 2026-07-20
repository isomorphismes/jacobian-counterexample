// A compact determinant certificate using weighted coordinates.
//
// On x != 0 put t = 1 + x*y and s = x^2*z.  Then
//   x^2 F1 = A(t,s),  x F2 = B(t,s),  F3 = x C(t,s).
// Comparing the source and target Jacobians shows that det(J_F) is the
// determinant of the weighted matrix W below.  Both sides are polynomials,
// so the identity established on x != 0 holds everywhere.

Q := Rationals();
R<x, y, z> := PolynomialRing(Q, 3);
S<t, s> := PolynomialRing(Q, 2);

F1 := (1 + x*y)^3*z + y^2*(1 + x*y)*(4 + 3*x*y);
F2 := y + 3*x*(1 + x*y)^2*z + 3*x*y^2*(4 + 3*x*y);
F3 := 2*x - 3*x^2*y - x^3*z;

A := t^3*s + t*(t - 1)^2*(1 + 3*t);
B := t - 1 + 3*t^2*s + 3*(t - 1)^2*(1 + 3*t);
C := 5 - 3*t - s;

ts := [ R | 1 + x*y, x^2*z ];
assert x^2*F1 eq Evaluate(A, ts);
assert x*F2 eq Evaluate(B, ts);
assert F3 eq x*Evaluate(C, ts);

W := Matrix(S, 3, 3, [
    -2*A, Derivative(A, 1), Derivative(A, 2),
      -B, Derivative(B, 1), Derivative(B, 2),
       C, Derivative(C, 1), Derivative(C, 2)
]);

assert Determinant(W) eq S ! -2;

print "PASS: weighted-coordinate determinant certificate verified over Q.";
