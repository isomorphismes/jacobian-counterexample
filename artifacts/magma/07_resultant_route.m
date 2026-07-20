// Exact certificates for the factorization/resultant plane attack.
// These identities expose a concrete open construction problem; they do not
// claim a solution of the two-dimensional Jacobian conjecture.

Qq := Rationals();

// Lou's linear-times-quadratic coefficient/resultant determinant.
R1<x, beta, gamma, delta, epsilon> := PolynomialRing(Qq, 5);
c3 := x*gamma;
c2 := x*delta + beta*gamma;
c1 := x*epsilon + beta*delta;
c0 := beta*epsilon;
rho12 := x^2*epsilon - x*beta*delta + beta^2*gamma;
outputs12 := [ c3, c2, c1, c0, rho12 ];
jacobian12 := Matrix(R1, 5, 5,
    [ Derivative(outputs12[i], j) : j in [1..5], i in [1..5] ]);
// The list order above fills by columns; its transpose is the usual Jacobian,
// and transposition preserves the determinant.
assert Determinant(jacobian12) eq -rho12^2;

// The clean plane blueprint: quadratic times cubic.  Coefficients are ordered
// from the leading term down.  The exact multiplier is +1 in this convention.
R23<a0, a1, a2, b0, b1, b2, b3> := PolynomialRing(Qq, 7);
product23 := [
    a0*b0,
    a0*b1 + a1*b0,
    a0*b2 + a1*b1 + a2*b0,
    a0*b3 + a1*b2 + a2*b1,
    a1*b3 + a2*b2,
    a2*b3
];
rho23 :=
      a0^3*b3^2 - a0^2*a1*b2*b3 - 2*a0^2*a2*b1*b3
    + a0^2*a2*b2^2 + a0*a1^2*b1*b3 + 3*a0*a1*a2*b0*b3
    - a0*a1*a2*b1*b2 - 2*a0*a2^2*b0*b2 + a0*a2^2*b1^2
    - a1^3*b0*b3 + a1^2*a2*b0*b2 - a1*a2^2*b0*b1
    + a2^3*b0^2;
outputs23 := product23 cat [ rho23 ];
jacobian23 := Matrix(R23, 7, 7,
    [ Derivative(outputs23[i], j) : j in [1..7], i in [1..7] ]);
assert Determinant(jacobian23) eq rho23^2;

// The literal linear-times-linear analogue collapses to one affine chart of a
// smooth quadric: D^2-4*G*E=1 and the missing ruling is G=0,D=-1.
R2<B, G> := PolynomialRing(Qq, 2);
D := 1 + 2*B*G;
E := B + B^2*G;
assert D^2 - 4*G*E eq 1;
assert Evaluate(D, [ Rationals() | 0, 0 ]) eq 1;

// Ordered quadratic factors restricted to an explicit affine-plane chart.
S<X, Y> := PolynomialRing(Qq, 2);
U := 1 + X^2*Y;
V := -Y - X^2*Y^2/2;
assert U^2 + 2*X^2*V eq 1;
p := V - X^2;
q := -X*U;
r := (V^2 - U^2)/4;

aa := X^2;
bb := X*(1 + X^2*Y);
cc := 2*Y + X^2*Y^2;
assert bb^2 - aa - aa^2*cc eq 0;
assert p eq -aa - cc/2;
assert q eq -bb;
assert r eq cc^2/16 - aa*cc/4 - 1/4;

Jaa_bb := Derivative(aa, 1)*Derivative(bb, 2)
    - Derivative(aa, 2)*Derivative(bb, 1);
Jaa_cc := Derivative(aa, 1)*Derivative(cc, 2)
    - Derivative(aa, 2)*Derivative(cc, 1);
Jbb_cc := Derivative(bb, 1)*Derivative(cc, 2)
    - Derivative(bb, 2)*Derivative(cc, 1);
assert Jaa_bb eq 2*aa^2;
assert Jaa_cc eq 4*bb;
assert Jbb_cc eq 2 + 4*aa*cc;

// Universal-cover interpretation: the source chart lies in
// Xc^2*Yc=Zc^2-1 and (aa,cc,bb) is the Z/2 quotient.
coverX := X;
coverY := cc;
coverZ := 1 + X^2*Y;
assert coverX^2*coverY - coverZ^2 + 1 eq 0;
assert aa eq coverX^2;
assert cc eq coverY;
assert bb eq coverX*coverZ;

// The basic pseudo-plane endomorphism yields a rational Darboux pair with
// constant bracket 4.  Its genuine boundary pole is the remaining defect.
KS := FieldOfFractions(S);
ratU := KS!bb;
ratV := KS!(2*cc)/(KS!(1 + aa*cc));
ratBracket := Derivative(ratU, 1)*Derivative(ratV, 2)
    - Derivative(ratU, 2)*Derivative(ratV, 1);
assert ratBracket eq 4;
assert KS!(1 + aa*cc) eq KS!((1 + X^2*Y)^2);

COV<XX, YY, ZZ> := PolynomialRing(Qq, 3);
coverRelation := XX^2*YY - ZZ^2 + 1;
liftX := XX*ZZ;
liftY := 4*YY;
liftZ := 2*ZZ^2 - 1;
assert liftX^2*liftY - liftZ^2 + 1 eq 4*ZZ^2*coverRelation;

TR<TA, TC, TB> := PolynomialRing(Qq, 3);
targetRelation := TB^2 - TA - TA^2*TC;
assert TB^2*(4*TC) - (1 + 2*TA*TC)^2 + 1
    eq 4*TC*targetRelation;
etaA := TB^2;
etaB := TB*(1 + 2*TA*TC);
etaC := 4*TC;
assert etaB^2 - etaA - etaA^2*etaC
    eq -4*TC*TB^2*targetRelation;

Poisson := func< left, right |
    Derivative(left, 1)*Derivative(right, 2)
    - Derivative(left, 2)*Derivative(right, 1) >;
assert Poisson(bb, cc)/2 + Poisson(aa*bb, cc^2)/2
    - 4*Poisson(aa*cc, bb*cc) eq 1;

assert [ Evaluate(h, [ Qq | 1, 0 ]) : h in [ p, q, r ] ]
    eq [ Qq | -1, -1, -1/4 ];
assert [ Evaluate(h, [ Qq | -1, -2 ]) : h in [ p, q, r ] ]
    eq [ Qq | -1, -1, -1/4 ];
assert [ Evaluate(h, [ Qq | 1, 0 ]) : h in [ aa, bb, cc ] ]
    eq [ Qq | 1, 1, 0 ];
assert [ Evaluate(h, [ Qq | -1, -2 ]) : h in [ aa, bb, cc ] ]
    eq [ Qq | 1, 1, 0 ];

H := -16*p^4*r + 4*p^3*q^2 + 128*p^2*r^2 + p^2
    - 144*p*q^2*r + 27*q^4 - 256*r^3 + 12*r - 1;
assert H eq 0;

Jpq := Derivative(p, 1)*Derivative(q, 2)
    - Derivative(p, 2)*Derivative(q, 1);
Jpr := Derivative(p, 1)*Derivative(r, 2)
    - Derivative(p, 2)*Derivative(r, 1);
Jqr := Derivative(q, 1)*Derivative(r, 2)
    - Derivative(q, 2)*Derivative(r, 1);
assert Jpq eq -2*X^4*Y^2 + 2*X^4 - 4*X^2*Y - 1;
assert Jpr eq -X*(X^2*Y + 1)*(X^2*Y^2 - X^2 + 2*Y);
assert Jqr eq -(2*X^6*Y^4 - 2*X^6*Y^2 + 8*X^4*Y^3 - 4*X^4*Y
    + 9*X^2*Y^2 - 2*X^2 + 2*Y)/4;
assert [ Evaluate(h, [ Qq | 1, 0 ]) : h in [ Jpq, Jpr, Jqr ] ]
    eq [ Qq | 1, 1, 1/2 ];
assert [ Evaluate(h, [ Qq | -1, -2 ]) : h in [ Jpq, Jpr, Jqr ] ]
    eq [ Qq | 1, 1, 1/2 ];

print "PASS: resultant Jacobians and the quadratic-factor plane scaffold verified.";
