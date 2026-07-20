# Exact SageMath certificates for the dimension-three Keller counterexample.

R.<x,y,z> = PolynomialRing(QQ, order='lex')

F1 = (1+x*y)^3*z + y^2*(1+x*y)*(4+3*x*y)
F2 = y + 3*x*(1+x*y)^2*z + 3*x*y^2*(4+3*x*y)
F3 = 2*x - 3*x^2*y - x^3*z
F = vector(R, [F1,F2,F3])
J = matrix(R, [[f.derivative(v) for v in (x,y,z)] for f in F])
assert J.det() == -2

points = [
    (0,0,-QQ(1)/4),
    (1,-QQ(3)/2,QQ(13)/2),
    (-1,QQ(3)/2,QQ(13)/2),
]
target = vector(QQ, [-QQ(1)/4,0,0])
for px,py,pz in points:
    assert vector(QQ, [f(x=px,y=py,z=pz) for f in F]) == target

I = R.ideal([F1+QQ(1)/4,F2,F3])
expected_basis = [z-QQ(27)/4*x^2+QQ(1)/4, y+QQ(3)/2*x, x^3-x]
assert I == R.ideal(expected_basis)
assert I.dimension() == 0
assert I.vector_space_dimension() == 3

S.<X,Y,Z> = PolynomialRing(QQ)
U = 1+2*X*Y
H = vector(S, [
    X-3*X^2*Y-2*X^3*Z,
    Y+6*X*U^2*Z+6*X*Y^2*(4+6*X*Y),
    U^3*Z+Y^2*U*(4+6*X*Y),
])
JH = matrix(S, [[h.derivative(v) for v in (X,Y,Z)] for h in H])
assert JH.det() == 1
assert JH(X=0,Y=0,Z=0) == identity_matrix(QQ,3)

T.<p,q,r,xx,uu> = PolynomialRing(QQ, order='lex')
E1 = p*xx^3+r*uu^3-xx*uu*(uu+1)
E2 = q*xx^2+3*r*uu^2-xx*(4*uu+2)
A = 27*p^2*r^2-18*p*q*r+16*p+q^3*r-q^2
B = 4-3*q*r
assert E1.resultant(E2,uu) == r*xx^3*(A*xx^3+B*xx-2*r)

QX.<v> = PolynomialRing(QQ)
assert (43*v^3+4*v-2).is_irreducible()

# Binary cubic / marked-root identities.
A,B,C = F
U0 = 1+x*y
V0 = x
assert C*U0^3-2*U0^2*V0+B*U0*V0^2-2*A*V0^3 == 0
assert 3*C*U0^2-4*U0*V0+B*V0^2 == 2*V0
assert -2*U0^2+2*B*U0*V0-6*A*V0^2 == -2*U0

omitted = R.ideal([F1-QQ(1)/3,F2-2,F3-QQ(2)/3])
assert omitted == R.ideal([1])

print('PASS: all SageMath certificates verified exactly over Q.')
