#!/usr/bin/env python3
"""Exact certificates from the dimension-two attack.

These assertions do not claim to solve the plane Jacobian conjecture.  They
certify the explicit quotient and sextic near-models and the algebraic
identities used by the descent obstructions.
"""

from __future__ import annotations

from collections import Counter
from itertools import permutations

import sympy as sp


def jacobian(f: sp.Expr, g: sp.Expr, variables: tuple[sp.Symbol, sp.Symbol]):
    x, y = variables
    return sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x))


def certify_equivariant_quotient():
    x, y, z, lam = sp.symbols("x y z lam", nonzero=True)
    U = 1 + x * y
    F1 = U**3 * z + y**2 * U * (4 + 3 * x * y)
    F2 = y + 3 * x * U**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
    F3 = 2 * x - 3 * x**2 * y - x**3 * z
    scaling = {x: lam * x, y: y / lam, z: z / lam**2}
    assert sp.factor(F1.subs(scaling, simultaneous=True) - F1 / lam**2) == 0
    assert sp.factor(F2.subs(scaling, simultaneous=True) - F2 / lam) == 0
    assert sp.factor(F3.subs(scaling, simultaneous=True) - lam * F3) == 0

    u, v = sp.symbols("u v")
    c = 2 - 3 * u - v
    a = (1 + u) ** 3 * v + u**2 * (1 + u) * (4 + 3 * u)
    b = u + 3 * (1 + u) ** 2 * v + 3 * u**2 * (4 + 3 * u)
    p = sp.expand(a * c**2)
    q = sp.expand(b * c)
    assert sp.factor(jacobian(p, q, (u, v)) + 2 * c**2) == 0

    # The old quotient coordinates factor through one affine blow-down.
    X = c
    Y = c * (u + 1)
    G1 = X * Y + Y**2 - Y**3
    G2 = 2 * X + 4 * Y - 3 * Y**2
    assert sp.expand(p - G1) == 0
    assert sp.expand(q - G2) == 0

    XX, YY = sp.symbols("XX YY")
    cubic_1 = XX * YY + YY**2 - YY**3
    cubic_2 = 2 * XX + 4 * YY - 3 * YY**2
    assert jacobian(cubic_1, cubic_2, (XX, YY)) == -2 * XX

    quotient_points = ((0, 0), (-sp.Rational(3, 2), sp.Rational(13, 2)))
    for point in quotient_points:
        assert (p.subs({u: point[0], v: point[1]}), q.subs({u: point[0], v: point[1]})) == (0, 0)
    for point in ((0, 0), (2, 2)):
        assert (
            cubic_1.subs({XX: point[0], YY: point[1]}),
            cubic_2.subs({XX: point[0], YY: point[1]}),
        ) == (0, 0)


def certify_linear_slice_formula():
    """Check the exact restriction used in the linear-coordinate obstruction."""
    x, r, alpha, beta, gamma = sp.symbols("x r alpha beta gamma", nonzero=True)
    y = r - 1 / x
    U = 1 + x * y
    g = (
        alpha * y**2 * U * (4 + 3 * x * y)
        + beta * (y + 3 * x * y**2 * (4 + 3 * x * y))
        + gamma * (2 * x - 3 * x**2 * y)
    )
    root_relation = {gamma: alpha * r**3 + 3 * beta * r**2}
    expected = r * (alpha * r + 4 * beta) + (alpha * r + 2 * beta) / x
    assert sp.factor((g - expected).subs(root_relation)) == 0


def certify_marked_plane_differential_identity():
    """Symbolically certify D*J=s*s_x from the differentiated root equations."""
    q1, q2, q1p, q2p, Ax, Bx, Aw, Bw, s, sx = sp.symbols(
        "q1 q2 q1p q2p Ax Bx Aw Bw s sx"
    )
    D = q1 * q2p - q1p * q2
    # Solve the three differentiated equations over their rational function field.
    solution = sp.solve(
        [q1 * Ax + q2 * Bx, q1p * Ax + q2p * Bx - sx, q1 * Aw + q2 * Bw + s],
        (Ax, Bx, Aw),
        dict=True,
    )[0]
    J = Ax * Bw - Aw * Bx
    assert sp.factor((D * J - s * sx).subs(solution)) == 0


def certify_nonlinear_collision_graph_obstruction():
    """Certify the first-order obstruction for arbitrary target polynomials.

    On the quadratic graph through the three colliding source points, the
    three tangent bivectors satisfy a relation whose coefficients sum to 108.
    A target two-form therefore cannot evaluate to the same nonzero constant
    at all three points.  This applies to R(F), S(F) for arbitrary R and S,
    not just to linear target projections.
    """
    x, y, z = sp.symbols("x y z")
    U = 1 + x * y
    graph = (27 * x**2 - 1) / 4
    A = (U**3 * z + y**2 * U * (4 + 3 * x * y)).subs(z, graph)
    B = (y + 3 * x * U**2 * z + 3 * x * y**2 * (4 + 3 * x * y)).subs(
        z, graph
    )
    C = (2 * x - 3 * x**2 * y - x**3 * z).subs(z, graph)
    minors = (jacobian(A, B, (x, y)), jacobian(A, C, (x, y)), jacobian(B, C, (x, y)))
    points = (
        (0, 0),
        (1, -sp.Rational(3, 2)),
        (-1, sp.Rational(3, 2)),
    )
    tangent_bivectors = sp.Matrix(
        [[minor.subs({x: px, y: py}) for minor in minors] for px, py in points]
    )
    expected = sp.Matrix(
        [
            [0, 0, -2],
            [-sp.Rational(81, 8), -sp.Rational(3, 2), 106],
            [sp.Rational(81, 8), sp.Rational(3, 2), 106],
        ]
    )
    assert tangent_bivectors == expected
    assert expected[1, :] + expected[2, :] + 106 * expected[0, :] == sp.zeros(1, 3)
    # If every row paired with one target two-form to give kappa, the same
    # relation would read 108*kappa=0.
    assert 1 + 1 + 106 == 108


def certify_equivariant_nonlinear_slice_obstructions():
    """Exact invariant identities for two natural nonlinear target shears."""
    x, y, z, lam = sp.symbols("x y z lam")
    Uxy = 1 + x * y
    F1 = Uxy**3 * z + y**2 * Uxy * (4 + 3 * x * y)
    F2 = y + 3 * x * Uxy**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
    F3 = 2 * x - 3 * x**2 * y - x**3 * z

    u, v = sp.symbols("u v")
    U = 1 + u
    a = U**3 * v + u**2 * U * (4 + 3 * u)
    b = u + 3 * U**2 * v + 3 * u**2 * (4 + 3 * u)
    c = 2 - 3 * u - v
    source_invariants = {u: x * y, v: x**2 * z}

    # x^2(F1 + lambda F2^2) is the quotient equation for the weight -2
    # shear A + lambda B^2.  At u=-1 it equals 4*lambda; for lambda=0
    # it has the factor u+1.
    k_a = sp.expand(a + lam * b**2)
    assert sp.expand(k_a.subs(source_invariants) - x**2 * (F1 + lam * F2**2)) == 0
    assert sp.expand(k_a.subs(u, -1) - 4 * lam) == 0
    assert sp.rem(sp.Poly(a, u, domain=sp.QQ.frac_field(v)), sp.Poly(U, u)) == 0

    # The useful elimination identity exposes the exceptional lambda=-1/12
    # completion without making it a coordinate.
    formal_b = sp.symbols("formal_b")
    a_in_u_b = (formal_b - u) * U / 3
    assert sp.factor(
        a - a_in_u_b.subs(formal_b, b)
    ) == 0
    assert sp.factor(
        12 * (a_in_u_b - formal_b**2 / 12)
        - (4 * U - (formal_b - 2 * U) ** 2)
    ) == 0

    # Likewise x(F2 + lambda F1 F3) is the quotient equation for the
    # weight -1 shear B + lambda AC, and it never meets u=-1.
    k_b = sp.expand(b + lam * a * c)
    assert sp.expand(k_b.subs(source_invariants) - x * (F2 + lam * F1 * F3)) == 0
    assert k_b.subs(u, -1) == 2


def certify_octahedral_sextic_model():
    t = sp.symbols("t")
    P = 64 * t**3 - 96 * t**2 + 30 * t + 1
    Q = 16 * t**2 - 16 * t + 1
    assert sp.expand(P**2 - Q**3 - 108 * t * (1 - t)) == 0
    assert sp.expand(2 * Q * sp.diff(P, t) - 3 * sp.diff(Q, t) * P) == 108

    x, y = sp.symbols("x y")
    u = x**2 - 16 * x * y + 16 * y**2
    v = x**3 + 30 * x**2 * y - 96 * x * y**2 + 64 * y**3
    assert jacobian(u, v, (x, y)) == 108 * x**3
    assert sp.expand(v**2 - u**3 - 108 * x**4 * y * (x - y)) == 0

    # The homogeneous forms have no common projective zero, which is the
    # elementary finiteness check for this weighted homogeneous map.
    ratio = sp.symbols("ratio")
    u_chart = sp.expand(u.subs({x: 1, y: ratio}))
    v_chart = sp.expand(v.subs({x: 1, y: ratio}))
    assert sp.gcd(sp.Poly(u_chart, ratio), sp.Poly(v_chart, ratio)) == 1
    assert u.subs({x: 0, y: 1}) != 0

    # The passport itself forces the octahedral monodromy.  Fix one
    # permutation of type (2,2,2), enumerate the compatible permutations of
    # type (3,3), and compute the generated groups exactly.  There are 24
    # labeled triples; every group has the element-order distribution of S4.
    identity = tuple(range(6))

    def compose(left, right):
        return tuple(left[right[i]] for i in range(6))

    def inverse(permutation):
        result = [0] * 6
        for i, value in enumerate(permutation):
            result[value] = i
        return tuple(result)

    def cycle_type(permutation):
        seen = set()
        lengths = []
        for i in range(6):
            if i in seen:
                continue
            j = i
            length = 0
            while j not in seen:
                seen.add(j)
                length += 1
                j = permutation[j]
            lengths.append(length)
        return tuple(sorted(lengths, reverse=True))

    def generated_group(generators):
        group = {identity}
        frontier = [identity]
        while frontier:
            element = frontier.pop()
            for generator in generators:
                product = compose(element, generator)
                if product not in group:
                    group.add(product)
                    frontier.append(product)
        return group

    def permutation_order(permutation):
        product = identity
        for order in range(1, 13):
            product = compose(product, permutation)
            if product == identity:
                return order
        raise AssertionError("unexpected permutation order")

    sigma_0 = (1, 0, 3, 2, 5, 4)
    compatible_groups = []
    for sigma_infinity in permutations(range(6)):
        if cycle_type(sigma_infinity) != (3, 3):
            continue
        sigma_1 = inverse(compose(sigma_0, sigma_infinity))
        if cycle_type(sigma_1) == (4, 1, 1):
            compatible_groups.append(generated_group((sigma_0, sigma_infinity)))

    assert len(compatible_groups) == 24
    assert {len(group) for group in compatible_groups} == {24}
    assert {
        tuple(sorted(Counter(permutation_order(g) for g in group).items()))
        for group in compatible_groups
    } == {((1, 1), (2, 9), (3, 8), (4, 6))}


def run_all():
    certify_equivariant_quotient()
    certify_linear_slice_formula()
    certify_marked_plane_differential_identity()
    certify_nonlinear_collision_graph_obstruction()
    certify_equivariant_nonlinear_slice_obstructions()
    certify_octahedral_sextic_model()


if __name__ == "__main__":
    run_all()
    print("PASS: all exact plane-attack certificates verified over Q.")
