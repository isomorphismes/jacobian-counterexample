#!/usr/bin/env python3
"""Exact certificates for the factorization/resultant plane attack.

The identities in this file extract the reusable mechanism from the 2026-07-20
derivation of Aaron Lou (@aaron_lou).  They do *not* solve the two-dimensional
Jacobian conjecture.  In particular, the final quartic construction is a
noninjective map to a coefficient surface; finding two functions on that
surface with constant Poisson bracket remains open.
"""

from __future__ import annotations

import sympy as sp


def bracket(f: sp.Expr, g: sp.Expr, x: sp.Symbol, y: sp.Symbol) -> sp.Expr:
    """The standard plane Poisson bracket."""
    return sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x))


def coefficient_resultant_data(r: int, s: int):
    """Return factors, product coefficients, resultant, and augmented determinant."""
    t = sp.symbols("t")
    aa = sp.symbols(f"a0:{r + 1}")
    bb = sp.symbols(f"b0:{s + 1}")
    p = sum(aa[i] * t ** (r - i) for i in range(r + 1))
    q = sum(bb[i] * t ** (s - i) for i in range(s + 1))
    product_coefficients = sp.Poly(p * q, t).all_coeffs()
    resultant = sp.resultant(p, q, t)
    augmented = product_coefficients + [resultant]
    determinant = sp.factor(sp.Matrix(augmented).jacobian(aa + bb).det())
    return p, q, product_coefficients, resultant, determinant


def certify_lou_left_right_equivalence_and_chart():
    """Lou's displayed map is left--right equivalent to the canonical map."""
    x, y, z, t = sp.symbols("x y z t")
    u = 1 + x * y
    canonical = sp.Matrix(
        [
            u**3 * z + y**2 * u * (4 + 3 * x * y),
            y + 3 * x * u**2 * z + 3 * x * y**2 * (4 + 3 * x * y),
            2 * x - 3 * x**2 * y - x**3 * z,
        ]
    )
    lou = sp.Matrix(
        [
            x**3 * z - 3 * x**2 * y + 2 * x,
            -3 * x**3 * y**2 * z
            + 9 * x**2 * y**3
            - 6 * x**2 * y * z
            + 12 * x * y**2
            - 3 * x * z
            + y,
            -x**3 * y**3 * z
            + 3 * x**2 * y**4
            - 3 * x**2 * y**2 * z
            + 7 * x * y**3
            - 3 * x * y * z
            + 4 * y**2
            - z,
        ]
    )
    assert all(
        sp.expand(lou[i] - canonical[2 - i].subs(z, -z)) == 0 for i in range(3)
    )

    beta = 1 + x * y
    gamma = (2 - 3 * x * y + x**2 * z) / 2
    delta = -(x * z - y + x**2 * y * z - 3 * x * y**2) / 2
    epsilon = -z * (1 + x * y) ** 2 + 4 * y**2 + 3 * x * y**3
    c3 = sp.expand(x * gamma)
    c2 = sp.expand(x * delta + beta * gamma)
    c1 = sp.expand(x * epsilon + beta * delta)
    c0 = sp.expand(beta * epsilon)
    rho = sp.expand(x**2 * epsilon - x * beta * delta + beta**2 * gamma)
    assert c2 == 1
    assert rho == 1
    assert all(sp.expand(a - b) == 0 for a, b in zip((2 * c3, 2 * c1, c0), lou))
    assert sp.expand(2 * beta * delta - x * epsilon - y) == 0
    assert sp.expand(4 * y * delta + 2 * gamma * y**2 - epsilon - z) == 0

    # Lou's cubic is the canonical marked binary cubic after t -> -t.
    A, B, C = (component.subs(z, -z) for component in canonical)
    canonical_cubic = C * t**3 - 2 * t**2 + B * t - 2 * A
    lou_cubic = lou[0] * t**3 / 2 + t**2 + lou[1] * t / 2 + lou[2]
    assert sp.expand(lou_cubic + canonical_cubic.subs(t, -t) / 2) == 0


def certify_resultant_jacobians():
    """Representative exact cases of det D(coeff(PQ), Res)=+/- (s-r) Res^2."""
    expected = {
        (1, 1): 0,
        (1, 2): -1,
        (1, 3): 2,
        (2, 3): 1,
    }
    for degrees, multiplier in expected.items():
        _, _, _, resultant, determinant = coefficient_resultant_data(*degrees)
        assert sp.expand(determinant - multiplier * resultant**2) == 0


def certify_literal_quadratic_collapse():
    """The degree-two factor analogue is an open chart of a quadric, not a cover."""
    beta, gamma = sp.symbols("beta gamma")
    delta = 1 + beta * gamma
    c2 = gamma
    c1 = sp.expand(delta + beta * gamma)
    c0 = sp.expand(beta * delta)
    assert sp.expand(c1**2 - 4 * c2 * c0) == 1

    # The map is an immersion.  It covers the c1=+1 line when c2=0 and omits
    # the other ruling line {c2=0,c1=-1}; hence it is one affine chart, not a
    # two-sheeted Keller construction.
    minors = (
        bracket(c2, c1, beta, gamma),
        bracket(c2, c0, beta, gamma),
        bracket(c1, c0, beta, gamma),
    )
    assert sp.groebner(minors, beta, gamma).contains(sp.Integer(1))
    assert c2.subs(gamma, 0) == 0
    assert c1.subs(gamma, 0) == 1
    assert c0.subs(gamma, 0) == beta
    assert sp.factor((c1 - 1) / (2 * c2) - beta) == 0
    assert sp.factor(2 * c0 / (c1 + 1) - beta) == 0


def certify_weighted_plane_core():
    """The weighted-lift quotient has one missing log-symplectic factor."""
    w, gamma, c, pprime = sp.symbols("w gamma c pprime", nonzero=True)
    # If q'(w)=w*p'(w)/c, this is the Jacobian in (w,gamma).
    matrix = sp.Matrix([[pprime, c], [gamma + w * pprime / c, w]])
    assert sp.factor(matrix.det()) == -c * gamma

    # gamma=x and w=y/x cancel the factor, but introduce poles into every
    # nonlinear p(w), q(w).  This is the two-dimensional bottleneck that the
    # extra weighted scale in the threefold construction removes.
    x, y = sp.symbols("x y", nonzero=True)
    chart_w = y / x
    chart_gamma = x
    assert sp.factor(bracket(chart_w, chart_gamma, x, y)) == -1 / chart_gamma
    example_p = 2 * chart_w - 3 * chart_w**2
    example_q = chart_w**2 - 2 * chart_w**3
    plane_P = sp.cancel(chart_gamma + example_p)
    plane_Q = sp.cancel(chart_w * chart_gamma + example_q)
    assert sp.denom(plane_P) != 1
    assert sp.denom(plane_Q) != 1
    assert sp.factor(bracket(plane_P, plane_Q, x, y)) == 1


def certify_quintic_slice_obstructions():
    """Exact identities behind two natural quadratic--cubic slice failures."""
    t = sp.symbols("t")
    p, q, m, n, rr, ss = sp.symbols("p q m n rr ss")
    quadratic = t**2 + p * t + q
    cubic = sp.expand((m * t + n) * quadratic + (rr * t + ss))
    product_polynomial = sp.Poly(sp.expand(quadratic * cubic), t)
    coefficients = product_polynomial.all_coeffs()
    expected = [
        m,
        2 * m * p + n,
        m * p**2 + 2 * m * q + 2 * n * p + rr,
        2 * m * p * q + n * p**2 + 2 * n * q + p * rr + ss,
        m * q**2 + 2 * n * p * q + p * ss + q * rr,
        q * (n * q + ss),
    ]
    assert all(sp.expand(a - b) == 0 for a, b in zip(coefficients, expected))
    resultant = sp.factor(sp.resultant(quadratic, cubic, t))
    assert resultant == ss**2 - p * rr * ss + q * rr**2

    # Fixing the top four product coefficients (M,A,B,C) solves successively
    # for n,rr,ss.  If the normalized inverse surface were A^2 in this monic
    # chart, its resultant N would be a nonzero constant.  Three coefficients
    # force the leading quintic data to degenerate.
    M, A, B, C = sp.symbols("M A B C")
    substitutions = {
        m: M,
        n: A - 2 * M * p,
        rr: B - 2 * A * p + 3 * M * p**2 - 2 * M * q,
        ss: C + A * p**2 - 2 * A * q - B * p - M * p**3 + 4 * M * p * q,
    }
    normalized_resultant = sp.Poly(sp.expand(resultant.subs(substitutions)), p, q)
    assert normalized_resultant.coeff_monomial(q**3) == 4 * M**2
    after_m = sp.Poly(normalized_resultant.as_expr().subs(M, 0), p, q)
    assert after_m.coeff_monomial(q**2) == 4 * A**2
    after_ma = sp.Poly(after_m.as_expr().subs(A, 0), p, q)
    assert after_ma.coeff_monomial(p**2) == 2 * B**2
    assert sp.expand(after_ma.as_expr().subs(B, 0) - C**2) == 0

    # The Bring--Jerrard coefficient plane has a single (4,5) cusp as its
    # discriminant.  The written Euler-characteristic calculation stratifies
    # its factor surface into fibers of sizes 10, 4, and 0.
    aa, bb, parameter = sp.symbols("aa bb parameter")
    bring_jerrard = t**5 + aa * t + bb
    discriminant = sp.factor(sp.discriminant(bring_jerrard, t))
    assert discriminant == 256 * aa**5 + 3125 * bb**4
    cusp_parametrization = {aa: -5 * parameter**4, bb: 4 * parameter**5}
    assert sp.expand(discriminant.subs(cusp_parametrization)) == 0

    # Two sparse cusp near-misses used in the construction search.
    lead, next_lead = sp.symbols("lead next_lead")
    assert sp.factor(sp.discriminant(lead * t**5 + next_lead * t**4 + 1, t)) == (
        3125 * lead**4 + 256 * next_lead**5
    )
    assert sp.factor(sp.discriminant(t * (lead * t**4 + next_lead * t**3 + 1), t)) == (
        256 * lead**3 - 27 * next_lead**4
    )


def certify_quartic_factor_scaffold():
    """Certify the explicit A^2 chart, collision, image, and linear no-go."""
    t, b, u, v = sp.symbols("t b u v")
    c = (v + u) / 2
    f = (v - u) / 2
    factor_a = t**2 + b * t + c
    factor_b = t**2 - b * t + f
    assert sp.factor(sp.resultant(factor_a, factor_b, t) - (u**2 + 2 * b**2 * v)) == 0
    product = sp.Poly(sp.expand(factor_a * factor_b), t)
    assert product.coeff_monomial(t**3) == 0
    p0 = sp.expand(v - b**2)
    q0 = sp.expand(-b * u)
    r0 = sp.expand((v**2 - u**2) / 4)
    assert sp.expand(product.as_expr() - (t**4 + p0 * t**2 + q0 * t + r0)) == 0

    x, y = sp.symbols("x y")
    chart = {b: x, u: 1 + x**2 * y, v: -y - x**2 * y**2 / 2}
    assert sp.expand((u**2 + 2 * b**2 * v - 1).subs(chart)) == 0
    assert sp.factor(((u - 1) / b**2).subs(chart) - y) == 0
    assert sp.factor((-2 * v / (u + 1)).subs(chart) - y) == 0
    p = sp.expand(p0.subs(chart))
    q = sp.expand(q0.subs(chart))
    r = sp.expand(r0.subs(chart))

    # A simpler intermediate surface retains the collision and is enough for
    # the plane attack.  It is the normalization of the product-coefficient
    # hypersurface in the marked-partition function field.
    aa = x**2
    bb = sp.expand(x * (1 + x**2 * y))
    cc = sp.expand(2 * y + x**2 * y**2)
    assert sp.expand(bb**2 - aa - aa**2 * cc) == 0

    # The factor surface is the universal cover of the exceptional affine
    # pseudo-plane S(2,2,1).  The source is the complement of one line in the
    # Danielewski cover X^2*Y=Z^2-1, and (aa,cc,bb) is the Z/2 quotient.
    cover_x = x
    cover_y = cc
    cover_z = 1 + x**2 * y
    assert sp.expand(cover_x**2 * cover_y - cover_z**2 + 1) == 0
    assert aa == cover_x**2
    assert cc == cover_y
    assert bb == sp.expand(cover_x * cover_z)
    assert sp.factor((cover_z - 1) / cover_x**2 - y) == 0
    assert sp.factor(cover_y / (cover_z + 1) - y) == 0

    # Dubouloz--Palka's basic open embedding T -> cover produces a rational
    # Darboux pair.  Its Jacobian is already constant, but its denominator is
    # the square of the missing-boundary equation and cannot be discarded.
    rational_v = sp.cancel(2 * cc / (1 + aa * cc))
    assert sp.factor(bracket(bb, rational_v, x, y)) == 4
    assert sp.factor(sp.denom(rational_v) - (1 + x**2 * y) ** 2) == 0
    shear0, shear1, shear2 = sp.symbols("shear0 shear1 shear2")
    shear = shear0 + shear1 * bb + shear2 * bb**2
    assert sp.factor(bracket(bb, rational_v + shear, x, y)) == 4

    # The C*-equivariant cover endomorphisms are Chebyshev maps.  Their
    # restrictions to the plane chart have constant Jacobian but a genuine
    # denominator for every tested nontrivial degree; the general obstruction
    # is the factorization of T_d(z)+1 recorded in the accompanying proof.
    lam = sp.symbols("lambda", nonzero=True)
    for degree in range(2, 7):
        cheb_t = sp.chebyshevt(degree, cover_z)
        cheb_u = sp.chebyshevu(degree - 1, cover_z)
        zeta = sp.symbols("zeta")
        assert sp.expand(
            sp.chebyshevt(degree, zeta) ** 2
            - 1
            - (zeta**2 - 1) * sp.chebyshevu(degree - 1, zeta) ** 2
        ) == 0
        assert sp.expand(
            sp.diff(sp.chebyshevt(degree, zeta), zeta)
            - degree * sp.chebyshevu(degree - 1, zeta)
        ) == 0
        cheb_plane_x = sp.cancel(x * cheb_u / lam)
        cheb_plane_y = sp.cancel(
            lam**2 * y * (cover_z + 1) / (cheb_t + 1)
        )
        assert sp.factor(bracket(cheb_plane_x, cheb_plane_y, x, y)) == (
            degree * lam
        )
        assert sp.denom(cheb_plane_y) != 1

    cover_X, cover_Y, cover_Z = sp.symbols("cover_X cover_Y cover_Z")
    cover_relation = cover_X**2 * cover_Y - cover_Z**2 + 1
    lifted = (cover_X * cover_Z, 4 * cover_Y, 2 * cover_Z**2 - 1)
    lifted_relation = sp.expand(
        lifted[0] ** 2 * lifted[1] - lifted[2] ** 2 + 1
    )
    assert sp.factor(lifted_relation - 4 * cover_Z**2 * cover_relation) == 0

    target_a, target_c, target_b = sp.symbols("target_a target_c target_b")
    target_relation = target_b**2 - target_a - target_a**2 * target_c
    embedded_cover_relation = sp.expand(
        target_b**2 * (4 * target_c) - (1 + 2 * target_a * target_c) ** 2 + 1
    )
    assert sp.factor(embedded_cover_relation - 4 * target_c * target_relation) == 0
    eta_a = target_b**2
    eta_b = target_b * (1 + 2 * target_a * target_c)
    eta_c = 4 * target_c
    eta_relation = sp.expand(eta_b**2 - eta_a - eta_a**2 * eta_c)
    assert sp.factor(eta_relation + 4 * target_c * target_b**2 * target_relation) == 0

    assert p == sp.expand(-aa - cc / 2)
    assert q == -bb
    assert r == sp.expand(cc**2 / 16 - aa * cc / 4 - sp.Rational(1, 4))
    normalization_minors = (
        bracket(aa, bb, x, y),
        bracket(aa, cc, x, y),
        bracket(bb, cc, x, y),
    )
    assert all(
        sp.expand(left - right) == 0
        for left, right in zip(
            normalization_minors, (2 * aa**2, 4 * bb, 2 + 4 * aa * cc)
        )
    )
    assert sp.groebner(normalization_minors, x, y).contains(sp.Integer(1))
    for point in ((1, 0), (-1, -2)):
        assert tuple(h.subs({x: point[0], y: point[1]}) for h in (aa, bb, cc)) == (
            1,
            1,
            0,
        )

    # The symplectic form is already an exact *sum* of target brackets at
    # target degree two.  This does not produce one Darboux pair, but it shows
    # why a purely cohomological obstruction is too weak.
    bracket_sum = (
        bracket(bb, cc, x, y) / 2
        + bracket(aa * bb, cc**2, x, y) / 2
        - 4 * bracket(aa * cc, bb * cc, x, y)
    )
    assert sp.expand(bracket_sum) == 1

    target = (-1, -1, -sp.Rational(1, 4))
    for point in ((1, 0), (-1, -2)):
        assert tuple(h.subs({x: point[0], y: point[1]}) for h in (p, q, r)) == target

    # The complementary-factor swap is symplectic and rational on this chart.
    tau_x = -x
    tau_y = -y - 2 / x**2
    for h in (p, q, r):
        assert sp.factor(h.subs({x: tau_x, y: tau_y}, simultaneous=True) - h) == 0
    assert sp.factor(bracket(tau_x, tau_y, x, y)) == 1

    P, Q, R = sp.symbols("P Q R")
    image_equation = (
        -16 * P**4 * R
        + 4 * P**3 * Q**2
        + 128 * P**2 * R**2
        + P**2
        - 144 * P * Q**2 * R
        + 27 * Q**4
        - 256 * R**3
        + 12 * R
        - 1
    )
    assert sp.expand(image_equation.subs({P: p, Q: q, R: r})) == 0

    # The singular locus of the coefficient surface is an elliptic cubic.
    singular_generators = [
        image_equation,
        sp.diff(image_equation, P),
        sp.diff(image_equation, Q),
        sp.diff(image_equation, R),
    ]
    singular_basis = sp.groebner(singular_generators, P, Q, R, order="grevlex")
    expected_singular = [2 * P**2 + 24 * R - 3, -32 * P * R + P + 9 * Q**2]
    assert all(singular_basis.reduce(h)[1] == 0 for h in expected_singular)
    expected_basis = sp.groebner(expected_singular, P, Q, R, order="grevlex")
    assert all(expected_basis.reduce(h)[1] == 0 for h in singular_generators)

    minors = (bracket(p, q, x, y), bracket(p, r, x, y), bracket(q, r, x, y))
    assert sp.groebner(minors, x, y).contains(sp.Integer(1))

    # No two linear forms in p,q,r have constant nonzero bracket.
    l1, l2, l3, kappa = sp.symbols("l1 l2 l3 kappa")
    candidate = sp.Poly(l1 * minors[0] + l2 * minors[1] + l3 * minors[2] - kappa, x, y)
    equations = [coefficient for _, coefficient in candidate.terms()]
    assert sp.linsolve(equations, (l1, l2, l3, kappa)) == {(0, 0, 0, 0)}

    # The displayed collision is the entire fiber in this A^2 chart, and the
    # two tangent bivectors agree.  This is why the earlier tangent obstruction
    # does not kill nonlinear target functions here.
    fiber_basis = sp.groebner([p + 1, q + 1, r + sp.Rational(1, 4)], y, x, order="lex")
    assert [sp.factor(h.as_expr()) for h in fiber_basis.polys] == [
        -x + y + 1,
        (x - 1) * (x + 1),
    ]
    rows = [tuple(h.subs({x: px, y: py}) for h in minors) for px, py in ((1, 0), (-1, -2))]
    assert rows[0] == rows[1] == (1, 1, sp.Rational(1, 2))


def run_all():
    certify_lou_left_right_equivalence_and_chart()
    certify_resultant_jacobians()
    certify_literal_quadratic_collapse()
    certify_weighted_plane_core()
    certify_quintic_slice_obstructions()
    certify_quartic_factor_scaffold()


if __name__ == "__main__":
    run_all()
    print("PASS: all exact factorization/resultant route certificates verified over Q.")
