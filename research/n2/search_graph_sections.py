#!/usr/bin/env python3
"""Exact searches for plane restrictions of the explicit threefold map.

This is a research script: it asks whether a polynomial graph z=phi(x,y)
through the known colliding points admits a constant-Jacobian linear
projection of the three output coordinates.
"""

from __future__ import annotations

import argparse

import sympy as sp


x, y, z = sp.symbols("x y z")
U = 1 + x * y
F = (
    U**3 * z + y**2 * U * (4 + 3 * x * y),
    y + 3 * x * U**2 * z + 3 * x * y**2 * (4 + 3 * x * y),
    2 * x - 3 * x**2 * y - x**3 * z,
)


def jacobian_minors(phi: sp.Expr) -> tuple[sp.Expr, sp.Expr, sp.Expr]:
    """Return the 2x2 minors after restricting F to z=phi."""
    restricted = tuple(sp.expand(f.subs(z, phi)) for f in F)
    answer = []
    for i, j in ((0, 1), (0, 2), (1, 2)):
        answer.append(
            sp.expand(
                sp.diff(restricted[i], x) * sp.diff(restricted[j], y)
                - sp.diff(restricted[i], y) * sp.diff(restricted[j], x)
            )
        )
    return tuple(answer)


def quadratic_collision_family() -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    """All quadratics taking the prescribed values at P0,P+,P-."""
    r, s, t = sp.symbols("r s t")
    # Linear odd part is r*(y+3*x/2).  The final x^2 coefficient makes
    # c20 - 3*c11/2 + 9*c02/4 = 27/4.
    phi = (
        -sp.Rational(1, 4)
        + r * (y + sp.Rational(3, 2) * x)
        + (sp.Rational(27, 4) + sp.Rational(3, 2) * s - sp.Rational(9, 4) * t)
        * x**2
        + s * x * y
        + t * y**2
    )
    return sp.expand(phi), (r, s, t)


def quadratic_equations() -> tuple[sp.Expr, tuple[sp.Symbol, ...], list[sp.Expr]]:
    """Coefficient system for a constant linear combination of the minors."""
    phi, parameters = quadratic_collision_family()
    a, b, c, k = sp.symbols("a b c k")
    minors = jacobian_minors(phi)
    obstruction = sp.Poly(a * minors[0] + b * minors[1] + c * minors[2] - k, x, y)
    equations = [sp.factor(coefficient) for _, coefficient in obstruction.terms()]
    return phi, parameters + (a, b, c, k), equations


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--groebner",
        action="store_true",
        help="compute a Groebner basis (potentially expensive)",
    )
    args = parser.parse_args()

    phi, unknowns, equations = quadratic_equations()
    print(f"phi = {phi}")
    print(f"unknowns = {unknowns}")
    print(f"coefficient equations = {len(equations)}")
    print(f"nonzero equations = {sum(eq != 0 for eq in equations)}")

    if args.groebner:
        # Constant nonzero projection can be normalized in three affine charts.
        for projection_variable in unknowns[-4:-1]:
            chart_unknowns = tuple(u for u in unknowns if u != projection_variable)
            chart_equations = [
                sp.expand(eq.subs(projection_variable, 1)) for eq in equations
            ]
            print(f"chart {projection_variable}=1")
            basis = sp.groebner(chart_equations, *chart_unknowns, order="grevlex")
            print(tuple(basis.polys))


if __name__ == "__main__":
    main()
