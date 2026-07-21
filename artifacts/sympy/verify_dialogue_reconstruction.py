#!/usr/bin/env python3
"""Exact replay for the six-question synthetic reconstruction paper.

The program is self-contained: it regenerates the displayed identities from
their formulas with exact SymPy arithmetic and imports no other project
certificate.
"""
from __future__ import annotations

from itertools import product
from math import comb
import sympy as sp


def zero(expr: sp.Expr) -> bool:
    return sp.expand(expr) == 0


def main() -> None:
    x, y, z = sp.symbols("x y z")
    beta, gamma, delta, epsilon = sp.symbols("beta gamma delta epsilon")

    # 1. Five-dimensional factor map and master determinant.
    c3 = x * gamma
    c2 = x * delta + beta * gamma
    c1 = x * epsilon + beta * delta
    c0 = beta * epsilon
    R = x**2 * epsilon - x * beta * delta + beta**2 * gamma
    master = sp.Matrix([c3, c2, c1, c0, R]).jacobian(
        [x, beta, gamma, delta, epsilon]
    ).det()
    assert zero(master + R**2)
    print("PASS master determinant: det = -R^2")

    # 2. Global chart and its inverse.
    chart = {
        beta: 1 + x * y,
        gamma: (2 - 3 * x * y + x**2 * z) / 2,
        delta: (y + 3 * x * y**2 - x * z - x**2 * y * z) / 2,
        epsilon: -z * (1 + x * y) ** 2 + y**2 * (4 + 3 * x * y),
    }
    assert zero(c2.subs(chart) - 1)
    assert zero(R.subs(chart) - 1)
    y_inverse = 2 * beta * delta - x * epsilon
    z_inverse = 4 * y_inverse * delta + 2 * gamma * y_inverse**2 - epsilon
    assert zero(y_inverse.subs(chart) - y)
    assert zero(z_inverse.subs(chart) - z)

    # Verify the other composition after using the two equations defining M.
    # A Groebner reduction is an exact way to test equality in the coordinate ring.
    I_M = sp.groebner([c2 - 1, R - 1], epsilon, delta, gamma, beta, x, order="lex")
    pullback = {
        y: y_inverse,
        z: z_inverse,
    }
    for variable in (beta, gamma, delta, epsilon):
        remainder = I_M.reduce(sp.together(chart[variable].subs(pullback) - variable))[1]
        assert remainder == 0
    print("PASS global polynomial chart and both inverse compositions")

    # 3. Translation derivation and slice.
    D_values = {
        x: 0,
        beta: 0,
        gamma: x**2 / 2,
        delta: -x * beta / 2,
        epsilon: -beta**2,
    }

    def D(poly: sp.Expr) -> sp.Expr:
        return sp.expand(sum(sp.diff(poly, var) * val for var, val in D_values.items()))

    assert zero(D(c2))
    assert zero(D(R))
    assert zero(D(y_inverse))
    assert I_M.reduce(D(z_inverse) - 1)[1] == 0
    print("PASS translation derivation preserves M and sends z to 1 on M")

    # 4. Construction of the explicit map.
    source_sign = {z: -z}
    F_from_chart = sp.Matrix(
        [
            c0.subs(chart).subs(source_sign),
            (2 * c1.subs(chart)).subs(source_sign),
            (2 * c3.subs(chart)).subs(source_sign),
        ]
    ).applyfunc(sp.expand)
    U = 1 + x * y
    F = sp.Matrix(
        [
            U**3 * z + y**2 * U * (4 + 3 * x * y),
            y + 3 * x * U**2 * z + 3 * x * y**2 * (4 + 3 * x * y),
            2 * x - 3 * x**2 * y - x**3 * z,
        ]
    )
    assert all(zero(a - b) for a, b in zip(F_from_chart, F))
    jac = sp.factor(F.jacobian([x, y, z]).det())
    assert jac == -2
    pts = (
        (0, 0, sp.Rational(-1, 4)),
        (1, sp.Rational(-3, 2), sp.Rational(13, 2)),
        (-1, sp.Rational(3, 2), sp.Rational(13, 2)),
    )
    images = [tuple(sp.simplify(f.subs(dict(zip((x, y, z), p)))) for f in F) for p in pts]
    assert images == [(sp.Rational(-1, 4), 0, 0)] * 3
    assert len(set(pts)) == 3
    print("PASS explicit map: det JF = -2 and exact three-point collision")

    # 5. Weight/support enumeration.
    source_weights = (1, -1, -2)
    output_weights = (-2, -1, 1)
    degree_caps = (7, 6, 4)
    supports: list[list[tuple[int, int, int]]] = []
    for target_weight, cap in zip(output_weights, degree_caps):
        terms = []
        for i in range(cap + 1):
            for j in range(cap + 1 - i):
                for k in range(min(1, cap - i - j) + 1):
                    if i * source_weights[0] + j * source_weights[1] + k * source_weights[2] == target_weight:
                        terms.append((i, j, k))
        supports.append(terms)
    assert [len(s) for s in supports] == [7, 6, 3]
    assert sum(comb(d + 3, 3) for d in degree_caps) == 239
    print("PASS support enumeration: 239 dense slots reduce to 16 = 7+6+3")

    # 6. Reconstruct the 16 Keller equations independently.
    u, v = sp.symbols("u v")
    A1, A2, A3, B0, B1, B2, C1, C2, D0, D1, D2, p, q = sp.symbols(
        "A1 A2 A3 B0 B1 B2 C1 C2 D0 D1 D2 p q"
    )
    A = v * (1 + A1*u + A2*u**2 + A3*u**3) + u**2 * (B0 + B1*u + B2*u**2)
    B = u * (1 + C1*u + C2*u**2) + v * (D0 + D1*u + D2*u**2)
    C = 2 + p*u + q*v
    quotient_matrix = sp.Matrix(
        [
            [-2*A, sp.diff(A, u), sp.diff(A, v)],
            [-B, sp.diff(B, u), sp.diff(B, v)],
            [C, sp.diff(C, u), sp.diff(C, v)],
        ]
    )
    error = sp.Poly(sp.expand(quotient_matrix.det() + 2), u, v)
    expected_exponents = {
        (0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2),
        (3,0),(3,1),(3,2),(4,0),(4,1),(5,0),(5,1),(6,0)
    }
    assert set(error.monoms()) == expected_exponents
    equations = [sp.expand(coeff) for _, coeff in error.terms()]
    print("PASS invariant determinant reduction and 16 coefficient equations")

    # 7. Neutral-gauge Groebner ideal equality.
    neutral_eqs = [eq.subs({p: 1, q: 1}) for eq in equations]
    gens = (A3, B2, A2, B1, A1, B0, D2, C2, D1, C1, D0)
    G = sp.groebner(neutral_eqs, *gens, order="grevlex", domain=sp.QQ)
    triangular = [
        (D0-9)**2,
        162*A3 + D0 - 3,
        162*B2 + D0 - 3,
        27*A2 - D0,
        108*B1 - 3*D0 - 1,
        18*A1 + D0 + 9,
        324*B0 + 7*D0 + 81,
        9*D2 - 2*D0 + 9,
        9*C2 - 2*D0 + 9,
        D1 + D0 - 3,
        18*C1 + 11*D0 - 27,
    ]
    assert all(G.reduce(t)[1] == 0 for t in triangular)
    H = sp.groebner(triangular, *gens, order="grevlex", domain=sp.QQ)
    assert all(H.reduce(eq)[1] == 0 for eq in neutral_eqs)
    assert G.reduce(D0-9)[1] != 0
    assert G.reduce((D0-9)**2)[1] == 0
    neutral_point = {
        A1:-1, A2:sp.Rational(1,3), A3:-sp.Rational(1,27),
        B0:-sp.Rational(4,9), B1:sp.Rational(7,27), B2:-sp.Rational(1,27),
        C1:-4, C2:1, D0:9, D1:-6, D2:1,
    }
    assert all(sp.expand(eq.subs(neutral_point)) == 0 for eq in neutral_eqs)
    print("PASS two-sided ideal equality; one set-theoretic point; nonradical length-two structure")

    # 8. Ungauged family, constant determinant, and collision.
    family = {
        A1:-p,
        A2:p**2/3,
        A3:-p**3/27,
        B0:-4*p**2/(9*q),
        B1:7*p**3/(27*q),
        B2:-p**4/(27*q),
        C1:-4*p,
        C2:p**2,
        D0:9*q/p,
        D1:-6*q,
        D2:p*q,
    }
    assert all(sp.factor(eq.subs(family)) == 0 for eq in equations)
    A_family = sp.factor(A.subs(family))
    B_family = sp.factor(B.subs(family))
    C_family = C
    v0 = -(2+p*u)/q
    assert sp.factor(B_family.subs(v, v0) - 2*(2*p*u-9)/p) == 0
    assert sp.factor(A_family.subs(v, v0) + (p*u-6)*(p*u-3)/(9*q)) == 0
    u0 = sp.Rational(9,2)/p
    v_collision = -sp.Rational(13,2)/q
    target = sp.Rational(1,4)/q
    assert sp.factor(A_family.subs({u:u0,v:v_collision}) - target) == 0
    assert sp.factor(B_family.subs({u:u0,v:v_collision})) == 0
    assert sp.factor(C_family.subs({u:u0,v:v_collision})) == 0
    print("PASS ungauged p,q-family and post-solve collision formulas")

    # 9. Least-height integral representatives.
    # The divisibility argument is short enough to encode as a bounded sanity check
    # around the proven lower bound |p| >= 3.
    def coeffs_for(P: int, Q: int):
        return [sp.simplify(expr.subs({p:P,q:Q})) for expr in list(family.values()) + [p,q]]
    minima = []
    for P in range(-12,13):
        for Q in range(-12,13):
            if P == 0 or Q == 0:
                continue
            vals = coeffs_for(P,Q)
            if all(val.is_Integer for val in vals):
                minima.append((max(abs(int(val)) for val in vals),P,Q))
    min_height = min(h for h,_,_ in minima)
    min_pairs = sorted((P,Q) for h,P,Q in minima if h == min_height)
    assert min_height == 12 and min_pairs == [(-3,-1),(-3,1),(3,-1),(3,1)]
    print("PASS least-height integral representatives: height 12 at (p,q)=(+-3,+-1)")
    print("PASS six-question reconstruction audit")


if __name__ == "__main__":
    main()
