#!/usr/bin/env python3
"""Exact certificates for the dimension-three Keller counterexample.

Nothing in this file uses floating-point arithmetic or numerical sampling.
Every public function raises AssertionError if its certificate fails.
"""

from __future__ import annotations

import sympy as sp


def canonical_map():
    x, y, z = sp.symbols("x y z")
    F = sp.Matrix(
        [
            (1 + x * y) ** 3 * z
            + y**2 * (1 + x * y) * (4 + 3 * x * y),
            y
            + 3 * x * (1 + x * y) ** 2 * z
            + 3 * x * y**2 * (4 + 3 * x * y),
            2 * x - 3 * x**2 * y - x**3 * z,
        ]
    )
    return (x, y, z), F


def certify_direct():
    variables, F = canonical_map()
    x, y, z = variables
    assert sp.expand(F.jacobian(variables).det()) == -2

    points = [
        (0, 0, -sp.Rational(1, 4)),
        (1, -sp.Rational(3, 2), sp.Rational(13, 2)),
        (-1, sp.Rational(3, 2), sp.Rational(13, 2)),
    ]
    target = sp.Matrix([-sp.Rational(1, 4), 0, 0])
    for point in points:
        values = {x: point[0], y: point[1], z: point[2]}
        assert F.subs(values).applyfunc(sp.expand) == target
    return points, target


def certify_structural_determinant():
    x, y, z, u, w = sp.symbols("x y z u w")
    a = u**3 * w + u * (u + 1)
    b = 3 * u**2 * w + 4 * u + 2
    weighted_jacobian = sp.Matrix(
        [
            [-2 * a / x**3, sp.diff(a, u) / x**2, u**3 / x**2],
            [-b / x**2, sp.diff(b, u) / x, 3 * u**2 / x],
            [-w, 0, -x],
        ]
    )
    assert sp.factor(weighted_jacobian.det()) == -2 / x**3

    u_source = 1 + x * y
    w_source = x**2 * z + 3 * x * y - 2
    source_change = sp.Matrix([x, u_source, w_source]).jacobian((x, y, z))
    assert sp.factor(source_change.det()) == x**3

    _, F = canonical_map()
    substitutions = {u: u_source, w: w_source}
    assert sp.factor(F[0] - (a / x**2).subs(substitutions)) == 0
    assert sp.factor(F[1] - (b / x).subs(substitutions)) == 0
    assert sp.factor(F[2] - (-x * w).subs(substitutions)) == 0


def certify_fiber_ideal():
    (x, y, z), F = canonical_map()
    source = [F[0] + sp.Rational(1, 4), F[1], F[2]]
    triangular = [
        z - sp.Rational(27, 4) * x**2 + sp.Rational(1, 4),
        y + sp.Rational(3, 2) * x,
        x**3 - x,
    ]
    source_basis = sp.groebner(source, z, y, x, order="lex", domain=sp.QQ)
    triangular_basis = sp.groebner(
        triangular, z, y, x, order="lex", domain=sp.QQ
    )
    for polynomial in triangular:
        assert sp.expand(source_basis.reduce(polynomial)[1]) == 0
    for polynomial in source:
        assert sp.expand(triangular_basis.reduce(polynomial)[1]) == 0
    assert [sp.expand(poly.as_expr()) for poly in source_basis.polys] == triangular


def normalized_map():
    X, Y, Z = sp.symbols("X Y Z")
    U = 1 + 2 * X * Y
    H = sp.Matrix(
        [
            X - 3 * X**2 * Y - 2 * X**3 * Z,
            Y + 6 * X * U**2 * Z + 6 * X * Y**2 * (4 + 6 * X * Y),
            U**3 * Z + Y**2 * U * (4 + 6 * X * Y),
        ]
    )
    return (X, Y, Z), H


def certify_normalization():
    variables, H = normalized_map()
    X, Y, Z = variables
    assert sp.expand(H.jacobian(variables).det()) == 1
    assert H.jacobian(variables).subs({X: 0, Y: 0, Z: 0}) == sp.eye(3)
    points = [
        (0, 0, -sp.Rational(1, 4)),
        (sp.Rational(1, 2), -sp.Rational(3, 2), sp.Rational(13, 2)),
        (-sp.Rational(1, 2), sp.Rational(3, 2), sp.Rational(13, 2)),
    ]
    target = sp.Matrix([0, 0, -sp.Rational(1, 4)])
    for point in points:
        values = {X: point[0], Y: point[1], Z: point[2]}
        assert H.subs(values).applyfunc(sp.expand) == target


def certify_x_elimination():
    """Check a secondary resultant relation for the inverse x-coordinate.

    This is an elimination certificate only; its discriminant is not the
    nonproperness divisor because distinct marked roots can share x.
    """
    p, q, r, x, u = sp.symbols("p q r x u")
    equation_1 = p * x**3 + r * u**3 - x * u * (u + 1)
    equation_2 = q * x**2 + 3 * r * u**2 - x * (4 * u + 2)
    A = 27 * p**2 * r**2 - 18 * p * q * r + 16 * p + q**3 * r - q**2
    B = 4 - 3 * q * r
    inverse_cubic = A * x**3 + B * x - 2 * r
    resultant = sp.resultant(equation_1, equation_2, u)
    assert sp.expand(resultant - r * x**3 * inverse_cubic) == 0
    assert sp.Poly(43 * x**3 + 4 * x - 2, x, domain=sp.QQ).is_irreducible


def certify_binary_cubic_geometry():
    (x, y, z), F = canonical_map()
    A, B, C = F
    aa, bb, cc, U, V, W = sp.symbols("aa bb cc U V W")
    Q = cc * U**3 - 2 * U**2 * V + bb * U * V**2 - 2 * aa * V**3
    marked = {aa: A, bb: B, cc: C, U: 1 + x * y, V: x}
    assert sp.expand(Q.subs(marked)) == 0
    assert sp.expand(sp.diff(Q, U).subs(marked) - 2 * x) == 0
    assert sp.expand(sp.diff(Q, V).subs(marked) + 2 * (1 + x * y)) == 0

    p = cc * W**3 - 2 * W**2 + bb * W - 2 * aa
    discriminant_factor = (
        bb**2 - cc * bb**3 - 16 * aa + 18 * aa * bb * cc - 27 * aa**2 * cc**2
    )
    assert sp.factor(sp.discriminant(p, W) - 4 * discriminant_factor) == 0

    triple_parameter = sp.symbols("rho", nonzero=True)
    triple = {
        aa: triple_parameter**2 / 3,
        bb: 2 * triple_parameter,
        cc: 2 / (3 * triple_parameter),
    }
    assert sp.factor(p.subs(triple)) == 2 * (W - triple_parameter) ** 3 / (
        3 * triple_parameter
    )

    omitted_ideal = sp.groebner(
        [A - sp.Rational(1, 3), B - 2, C - sp.Rational(2, 3)],
        x,
        y,
        z,
        order="grevlex",
        domain=sp.QQ,
    )
    assert omitted_ideal.reduce(sp.Integer(1))[1] == 0

    # Both regular inverse charts of the marked-simple-root incidence.
    h = sp.diff(p, W) / 2
    finite_inverse = {
        x: 1 / h,
        y: W - h,
        z: 5 * h**2 - 3 * W * h - cc * h**3,
    }
    finite_image = F.subs(finite_inverse, simultaneous=True)
    assert sp.factor(finite_image[0] - aa - p / 2) == 0
    assert sp.factor(finite_image[1] - bb) == 0
    assert sp.factor(finite_image[2] - cc) == 0

    chart_s = sp.symbols("chart_s")
    chart_k = 1 - bb * chart_s + 3 * aa * chart_s**2
    chart_y = bb - 3 * aa * chart_s
    infinity_inverse = {
        x: chart_s / chart_k,
        y: chart_y,
        z: aa * chart_k**3 - chart_y**2 * chart_k * (chart_k + 3),
    }
    infinity_image = F.subs(infinity_inverse, simultaneous=True)
    chart_Q = Q.subs({U: 1, V: chart_s})
    assert sp.factor(infinity_image[0] - aa) == 0
    assert sp.factor(infinity_image[1] - bb) == 0
    assert sp.factor(infinity_image[2] - cc + chart_Q) == 0

    assert sp.factor(sp.discriminant(discriminant_factor, aa)) == -4 * (
        3 * bb * cc - 4
    ) ** 3


def certify_pencil_bundle_geometry():
    """Certify the pencil description of the marked-root source."""
    x, beta, gamma, delta, epsilon = sp.symbols(
        "x beta gamma delta epsilon"
    )

    hyperplane = beta * gamma + x * delta
    limiting_line = -2 * beta * delta + x * epsilon
    resultant = beta**2 * gamma - x * beta * delta + x**2 * epsilon
    assert sp.expand(resultant - beta * hyperplane - x * limiting_line) == 0

    # This projective point is the common base point of the whole pencil.
    base_point = {
        gamma: x**2,
        delta: -x * beta,
        epsilon: -2 * beta**2,
    }
    assert sp.expand(hyperplane.subs(base_point)) == 0
    assert sp.expand(limiting_line.subs(base_point)) == 0
    assert sp.expand(resultant.subs(base_point)) == 0

    # The complement of the constant section and diagonal is A^2.  The
    # forward parametrization is ([s:1+st],[1:t]); its separating determinant
    # is one, so its rational-looking inverse has no pole on this open set.
    s, t = sp.symbols("s t")
    forward_x, forward_beta = s, 1 + s * t
    forward_m, forward_n = sp.Integer(1), t
    forward_determinant = (
        forward_beta * forward_m - forward_x * forward_n
    )
    assert sp.expand(forward_determinant) == 1
    assert sp.cancel(
        forward_x * forward_m / forward_determinant - s
    ) == 0
    assert sp.cancel(forward_n / forward_m - t) == 0

    # Conversely, for ([x:beta],[m:n]) in the open set, put
    # s=xm/(beta*m-x*n) and t=n/m.  The reconstructed pairs agree
    # projectively with the original pairs.
    m, n = sp.symbols("m n", nonzero=True)
    separating_determinant = beta * m - x * n
    inverse_s = x * m / separating_determinant
    inverse_t = n / m
    reconstructed_beta = 1 + inverse_s * inverse_t
    assert sp.cancel(
        reconstructed_beta - beta * m / separating_determinant
    ) == 0
    assert sp.cancel(inverse_s * beta - reconstructed_beta * x) == 0
    assert sp.cancel(n - inverse_t * m) == 0


def certify_escape_curve():
    (x, y, z), F = canonical_map()
    s = sp.symbols("s", nonzero=True)
    curve = {x: s, y: -1 / s, z: 5 / s**2}
    assert F.subs(curve).applyfunc(sp.factor) == sp.Matrix([0, 2 / s, 0])

    t, rho, c = sp.symbols("t rho c", nonzero=True)
    general_curve = {
        x: 1 / t,
        y: rho - t,
        z: 5 * t**2 - 3 * rho * t - c * t**3,
    }
    expected = sp.Matrix(
        [rho**2 + rho * t - c * rho**3, 4 * rho + 2 * t - 3 * c * rho**2, c]
    )
    assert (F.subs(general_curve) - expected).applyfunc(sp.factor) == sp.zeros(3, 1)


def certify_weyl_relations():
    """Certify the polynomial vector fields defining a Weyl A_3 endomorphism."""
    variables, H = normalized_map()
    J = H.jacobian(variables)
    J_inverse = J.adjugate()  # det(J)=1, so this is the exact inverse.
    assert (J * J_inverse).applyfunc(sp.expand) == sp.eye(3)

    # delta_i = sum_k (J^{-1})_{k,i} d/dx_k is dual to dH_i.
    for i in range(3):
        for j in range(3):
            dual_value = sum(
                J_inverse[k, i] * sp.diff(H[j], variables[k]) for k in range(3)
            )
            assert sp.expand(dual_value) == (1 if i == j else 0)

    # The dual derivations commute, giving all defining Weyl relations.
    for i in range(3):
        for j in range(i + 1, 3):
            for ell in range(3):
                bracket_coefficient = sum(
                    J_inverse[k, i] * sp.diff(J_inverse[ell, j], variables[k])
                    - J_inverse[k, j] * sp.diff(J_inverse[ell, i], variables[k])
                    for k in range(3)
                )
                assert sp.expand(bracket_coefficient) == 0


def run_all():
    certify_direct()
    certify_structural_determinant()
    certify_fiber_ideal()
    certify_normalization()
    certify_x_elimination()
    certify_binary_cubic_geometry()
    certify_pencil_bundle_geometry()
    certify_escape_curve()
    certify_weyl_relations()


if __name__ == "__main__":
    run_all()
    print("PASS: all SymPy certificates verified exactly over Q.")
