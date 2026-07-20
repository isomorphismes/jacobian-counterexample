#!/usr/bin/env python3
"""Bounded exact searches around the quadratic-factor A^2 scaffold.

This program has two independent modes:

1. Over QQ it asks whether 1 lies in a bounded span of Poisson brackets of
   polynomials in the three product coefficients p,q,r.  Failure is only a
   bounded negative result, never a proof of the plane Jacobian conjecture.
2. Over small finite fields it counts coprime 2+3 factorizations above each
   sparse monic-quintic coefficient plane.  Point counts are a cheap sieve for
   implausible A^2 slices, not a characteristic-zero isomorphism test.
"""

from __future__ import annotations

import argparse
from itertools import combinations, product

import sympy as sp


def plane_scaffold():
    x, y = sp.symbols("x y")
    u = 1 + x**2 * y
    v = -y - x**2 * y**2 / 2
    p = sp.expand(v - x**2)
    q = sp.expand(-x * u)
    r = sp.expand((v**2 - u**2) / 4)
    return x, y, (p, q, r)


def target_exponents(degree: int):
    return [
        (i, j, k)
        for i in range(degree + 1)
        for j in range(degree + 1 - i)
        for k in range(degree + 1 - i - j)
    ]


def poisson(f, g, x, y):
    return sp.Poly(
        sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x)),
        x,
        y,
    )


def coefficient_matrix(polynomials, x, y):
    monomials = {(0, 0)}
    for polynomial in polynomials:
        monomials.update(polynomial.monoms())
    monomials = sorted(monomials)
    row = {monomial: index for index, monomial in enumerate(monomials)}
    matrix = sp.zeros(len(monomials), len(polynomials))
    for column, polynomial in enumerate(polynomials):
        for monomial, coefficient in polynomial.terms():
            matrix[row[monomial], column] = coefficient
    constant = sp.zeros(len(monomials), 1)
    constant[row[(0, 0)], 0] = 1
    return matrix, constant


def bounded_poisson_search(max_degree: int):
    x, y, generators = plane_scaffold()
    for degree in range(1, max_degree + 1):
        basis = [
            sp.expand(generators[0] ** i * generators[1] ** j * generators[2] ** k)
            for i, j, k in target_exponents(degree)
        ]
        brackets = [poisson(a, b, x, y) for a, b in combinations(basis, 2)]
        matrix, constant = coefficient_matrix(brackets, x, y)
        rank = matrix.rank()
        augmented_rank = matrix.row_join(constant).rank()
        print(
            f"target degree <= {degree}: basis={len(basis)}, "
            f"bracket rank={rank}, augmented rank={augmented_rank}, "
            f"constant_in_span={rank == augmented_rank}"
        )


def trim(polynomial):
    while len(polynomial) > 1 and polynomial[-1] == 0:
        polynomial.pop()
    return polynomial


def polynomial_remainder(dividend, divisor, prime):
    dividend = dividend[:]
    divisor = trim(divisor[:])
    inverse_lead = pow(divisor[-1], -1, prime)
    while len(dividend) >= len(divisor) and not (
        len(dividend) == 1 and dividend[0] == 0
    ):
        coefficient = dividend[-1] * inverse_lead % prime
        shift = len(dividend) - len(divisor)
        for index, value in enumerate(divisor):
            dividend[index + shift] = (
                dividend[index + shift] - coefficient * value
            ) % prime
        trim(dividend)
    return dividend


def coprime(left, right, prime):
    while not (len(right) == 1 and right[0] == 0):
        left, right = right, polynomial_remainder(left, right, prime)
    return len(trim(left)) == 1


def sparse_plane_counts(primes):
    # Indices 0,...,4 mean c4,...,c0 in
    # t^5+c4*t^4+c3*t^3+c2*t^2+c1*t+c0.
    planes = list(combinations(range(5), 2))
    for prime in primes:
        counts = {plane: 0 for plane in planes}
        for p1, p0, q2, q1, q0 in product(range(prime), repeat=5):
            quadratic = [p0, p1, 1]
            cubic = [q0, q1, q2, 1]
            if not coprime(quadratic, cubic, prime):
                continue
            coefficients = [0] * 6
            for i, left in enumerate(quadratic):
                for j, right in enumerate(cubic):
                    coefficients[i + j] = (
                        coefficients[i + j] + left * right
                    ) % prime
            lower_descending = (
                coefficients[4],
                coefficients[3],
                coefficients[2],
                coefficients[1],
                coefficients[0],
            )
            for plane in planes:
                if all(
                    lower_descending[index] == 0
                    for index in range(5)
                    if index not in plane
                ):
                    counts[plane] += 1
        print(f"F_{prime}, comparison |A^2|={prime**2}")
        for plane, count in counts.items():
            free = ",".join(f"c{4 - index}" for index in plane)
            print(f"  free ({free}): {count}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--poisson-degree",
        type=int,
        default=3,
        help="largest target degree for the exact bracket-span search",
    )
    parser.add_argument(
        "--primes",
        default="3,5,7,11",
        help="comma-separated primes for the sparse-plane point-count sieve",
    )
    args = parser.parse_args()
    bounded_poisson_search(args.poisson_degree)
    primes = [int(value) for value in args.primes.split(",") if value]
    sparse_plane_counts(primes)


if __name__ == "__main__":
    main()
