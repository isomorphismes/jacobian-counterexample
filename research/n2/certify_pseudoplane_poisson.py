#!/usr/bin/env python3
"""Exact certificates for the exceptional pseudo-plane Poisson attack.

Let

    R = Q[a,b,c] / (b^2 - a - a^2*c)

with Poisson brackets

    {a,b}=2*a^2,  {a,c}=4*b,  {b,c}=2+4*a*c.

This script proves finite polynomial identities and the ambient-quadratic
Groebner no-go used in ``knowledge/pseudoplane-poisson-obstructions.md``.
Valuation and residue arguments in that note are mathematical proofs rather
than bounded computer searches.
"""

from __future__ import annotations

import sympy as sp


a, b, c = sp.symbols("a b c")
RELATION = b**2 - a - a**2 * c
POISSON = sp.Matrix(
    [
        [0, 2 * a**2, 4 * b],
        [-2 * a**2, 0, 2 + 4 * a * c],
        [-4 * b, -2 - 4 * a * c, 0],
    ]
)


def bracket(f: sp.Expr, g: sp.Expr) -> sp.Expr:
    """Poisson bracket in the ambient polynomial ring."""
    variables = (a, b, c)
    df = sp.Matrix([sp.diff(f, variable) for variable in variables])
    dg = sp.Matrix([sp.diff(g, variable) for variable in variables])
    return sp.expand((df.T * POISSON * dg)[0])


def normal_form(f: sp.Expr) -> sp.Expr:
    """The unique representative f0(a,c)+b*f1(a,c) modulo RELATION."""
    return sp.Poly(sp.expand(f), b).rem(sp.Poly(RELATION, b)).as_expr().expand()


def certify_poisson_and_darboux_charts() -> None:
    """Check the hypersurface bracket and the two rational Darboux charts."""
    defining = b**2 - a - a**2 * c
    assert normal_form(bracket(defining, a)) == 0
    assert normal_form(bracket(defining, b)) == 0
    assert normal_form(bracket(defining, c)) == 0

    # Chart D(a): p=-1/(2a), q=b.
    p = -sp.Rational(1, 2) / a
    q = b
    assert sp.factor(bracket(p, q)) == 1
    assert sp.factor(c - (2 * p + 4 * p**2 * q**2)).subs(b**2, a + a**2 * c) == 0

    # Chart D(1+ac): P=b/2, Q=c/(1+ac).
    pp = b / 2
    qq = c / (1 + a * c)
    assert sp.factor(normal_form(sp.together(bracket(pp, qq) - 1).as_numer_denom()[0])) == 0

    # The overlap transition is P=q/2, Q=-2p-q^{-2} and is symplectic.
    p_symbol, q_symbol = sp.symbols("p q", nonzero=True)
    pp_transition = q_symbol / 2
    qq_transition = -2 * p_symbol - q_symbol ** -2
    canonical = sp.diff(pp_transition, p_symbol) * sp.diff(qq_transition, q_symbol) - sp.diff(
        pp_transition, q_symbol
    ) * sp.diff(qq_transition, p_symbol)
    assert sp.factor(canonical) == 1

    # The rational mates forced by fixing a or b really have bracket one.
    assert sp.factor(bracket(a, b / (2 * a**2))) == 1
    assert sp.factor(bracket(b, 1 / (2 * a))) == 1

    # For fixed c the generic fiber diagonalizes after adjoining ell^2=c.
    ell = sp.symbols("ell", nonzero=True)
    z = 1 + 2 * a * c + 2 * ell * b
    assert sp.factor(bracket(c, z).subs(c, ell**2) + 4 * ell * z.subs(c, ell**2)) == 0


def certify_homogeneous_formulas() -> None:
    """Verify the two all-weight formulas with symbolic integer exponents."""
    t = sp.symbols("t", nonzero=True)
    k = sp.symbols("k", integer=True, nonnegative=True)
    h = sp.symbols("h", integer=True, positive=True)
    pfun = sp.Function("P")
    qfun = sp.Function("Q")
    ac = a * c

    positive_u = a**k * pfun(ac)
    positive_v = b * c ** (k + 1) * qfun(ac)
    positive_actual = bracket(positive_u, positive_v)
    positive_actual = sp.collect(positive_actual, b**2).subs(b**2, a * (1 + a * c))
    positive_actual = sp.simplify(positive_actual.subs(c, t / a))
    positive_expected = 2 * t**k * (
        k * (2 * (k + 1) + (2 * k + 3) * t) * pfun(t) * qfun(t)
        + (2 * k + 1) * t * (1 + t) * sp.diff(pfun(t), t) * qfun(t)
        + 2 * k * t * (1 + t) * pfun(t) * sp.diff(qfun(t), t)
    )
    assert sp.simplify(positive_actual - positive_expected) == 0

    negative_u = c**h * pfun(ac)
    negative_v = b * a ** (h - 1) * qfun(ac)
    negative_actual = bracket(negative_u, negative_v)
    negative_actual = sp.collect(negative_actual, b**2).subs(b**2, a * (1 + a * c))
    negative_actual = sp.simplify(negative_actual.subs(c, t / a))
    negative_expected = -2 * t ** (h - 1) * (
        h * ((2 * h - 1) + 2 * h * t) * pfun(t) * qfun(t)
        + (2 * h - 1) * t * (1 + t) * sp.diff(pfun(t), t) * qfun(t)
        + 2 * h * t * (1 + t) * pfun(t) * sp.diff(qfun(t), t)
    )
    assert sp.simplify(negative_actual - negative_expected) == 0

    # The only negative-weight case not killed by a visible power of t is h=1.
    # Its bracket is -(2/Q)*(t(1+t)P Q^2)', the degree obstruction in the note.
    h_one = sp.simplify(negative_expected.subs(h, 1))
    derivative_form = -2 * sp.diff(t * (1 + t) * pfun(t) * qfun(t) ** 2, t) / qfun(t)
    assert sp.simplify(h_one - derivative_form) == 0


def certify_no_ambient_quadratic_pair() -> None:
    """Prove exactly that no two ambient quadratics have bracket one in R.

    Constants do not affect a bracket.  The constant coefficient of a putative
    bracket-one pair makes its linear (b,c)-coefficient matrix invertible with
    determinant 1/2.  An SL(2) target change therefore normalizes those terms
    to U=b/2+..., V=c+....  The remaining coefficient ideal is the unit ideal.
    """
    names = "A D E F G H I Ap Dp Ep Fp Gp Hp Ip"
    A, D, E, F, G, H, I, Ap, Dp, Ep, Fp, Gp, Hp, Ip = sp.symbols(names)
    variables = (A, D, E, F, G, H, I, Ap, Dp, Ep, Fp, Gp, Hp, Ip)

    # The last basis vector is the normal form of b^2-a.  Thus these are
    # precisely the images of all ambient polynomials of total degree <=2.
    u = b / 2 + A * a + D * a**2 + E * a * b + F * a * c + G * b * c + H * c**2 + I * a**2 * c
    v = c + Ap * a + Dp * a**2 + Ep * a * b + Fp * a * c + Gp * b * c + Hp * c**2 + Ip * a**2 * c
    remainder = sp.Poly(normal_form(bracket(u, v) - 1), a, b, c)
    equations = [coefficient for _, coefficient in remainder.terms()]
    basis = sp.groebner(equations, *variables, order="grevlex")
    assert list(basis) == [sp.Integer(1)]

    # Independent human-readable contradiction used in the proof note.
    delta = lambda x, xp, y, yp: x * yp - xp * y
    delta_eh = delta(E, Ep, H, Hp)
    delta_fg = delta(F, Fp, G, Gp)
    assert sp.expand(2 * (8 * delta_eh + delta_fg)) in equations
    assert sp.expand(2 * (6 * delta_eh + delta_fg + 1)) in equations


def certify_lnd_and_self_map_identities() -> None:
    """Check the natural LND and the conformally Poisson etale self-map."""
    # delta=(1/2){a,-}: delta(a)=0, delta(b)=a^2, delta(c)=2b.
    assert bracket(a, a) / 2 == 0
    assert bracket(a, b) / 2 == a**2
    assert bracket(a, c) / 2 == 2 * b
    parameter = sp.symbols("parameter")
    moved = {a: a, b: b + parameter * a**2, c: c + 2 * parameter * b + parameter**2 * a**2}
    assert sp.expand(RELATION.subs(moved, simultaneous=True) - RELATION) == 0

    eta_a = b**2
    eta_b = b * (1 + 2 * a * c)
    eta_c = 4 * c
    eta = (eta_a, eta_b, eta_c)
    assert normal_form(eta_b**2 - eta_a - eta_a**2 * eta_c) == 0
    target_brackets = (2 * eta_a**2, 4 * eta_b, 2 + 4 * eta_a * eta_c)
    actual_brackets = (
        normal_form(bracket(eta_a, eta_b)),
        normal_form(bracket(eta_a, eta_c)),
        normal_form(bracket(eta_b, eta_c)),
    )
    assert all(normal_form(actual - 4 * target) == 0 for actual, target in zip(actual_brackets, target_brackets))

    t = a * c
    s = 1 + 2 * t
    eta_t = normal_form(eta_a * eta_c)
    assert normal_form(eta_t - 4 * t * (1 + t)) == 0
    assert normal_form((1 + 2 * eta_t) - (2 * s**2 - 1)) == 0


def main() -> None:
    certify_poisson_and_darboux_charts()
    certify_homogeneous_formulas()
    certify_no_ambient_quadratic_pair()
    certify_lnd_and_self_map_identities()
    print("PASS: pseudo-plane Poisson identities and quadratic no-go certified over Q.")


if __name__ == "__main__":
    main()
