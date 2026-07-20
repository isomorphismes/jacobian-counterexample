#!/usr/bin/env sage
"""Exact unit-ideal certificate for normalized plane collisions through degree 3."""

from sage.all import PolynomialRing, QQ


dmax = 3
monomials = [
    (i, degree - i)
    for degree in range(2, dmax + 1)
    for i in range(degree, -1, -1)
]
names = [f"p{i}{j}" for i, j in monomials] + [
    f"q{i}{j}" for i, j in monomials
]

coefficient_ring = PolynomialRing(QQ, names, order="degrevlex")
coefficients = coefficient_ring.gens()
n = len(monomials)
source_ring = PolynomialRing(coefficient_ring, ["x", "y"])
x, y = source_ring.gens()

P = x + sum(
    coefficients[k] * x**i * y**j for k, (i, j) in enumerate(monomials)
)
Q = y + sum(
    coefficients[n + k] * x**i * y**j
    for k, (i, j) in enumerate(monomials)
)

jacobian_minus_one = P.derivative(x) * Q.derivative(y) - P.derivative(y) * Q.derivative(x) - 1
equations = list(jacobian_minus_one.dict().values())
equations += [P(x=1, y=0), Q(x=1, y=0)]
basis = coefficient_ring.ideal(equations).groebner_basis()

print("variables:", coefficient_ring.ngens())
print("equations:", len(equations))
print(basis)
assert list(basis) == [coefficient_ring.one()]
