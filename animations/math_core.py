"""Exact formulas and deterministic curve exports for the visualizations.

No Manim or NumPy import is required.  Operations work with ``Fraction`` for
exact tests and with ``float`` for rendering.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
from typing import Callable, Sequence, TypeVar


Number = TypeVar("Number")
Point3 = tuple[Number, Number, Number]
BRANCHES = ("zero", "moving", "remaining")


def jacobian_map(point: Sequence[Number]) -> Point3[Number]:
    """Evaluate Alpöge's displayed map ``F`` at a three-vector."""

    x, y, z = point
    one = 1 + x * y
    f1 = one**3 * z + y**2 * one * (4 + 3 * x * y)
    f2 = y + 3 * x * one**2 * z + 3 * x * y**2 * (4 + 3 * x * y)
    f3 = 2 * x - 3 * x**2 * y - x**3 * z
    return f1, f2, f3


def elementary_source(curve_id: str, parameter: Number) -> Point3[Number]:
    """Return a point on one of the three elementary source curves."""

    zero = parameter * 0
    if curve_id == "x_axis":
        return parameter, zero, zero
    if curve_id == "y_axis":
        return zero, parameter, zero
    if curve_id == "z_axis":
        return zero, zero, parameter
    raise KeyError(f"unknown elementary curve: {curve_id}")


def elementary_target(curve_id: str, parameter: Number) -> Point3[Number]:
    """Return the simplified exact image of an elementary curve."""

    zero = parameter * 0
    if curve_id == "x_axis":
        return zero, zero, 2 * parameter
    if curve_id == "y_axis":
        return 4 * parameter**2, parameter, zero
    if curve_id == "z_axis":
        return parameter, zero, zero
    raise KeyError(f"unknown elementary curve: {curve_id}")


def target_family(parameter: Number) -> Point3[Number]:
    """Target curve for ``2 T (T-s) (T-(1-s))`` in ``(a,b,c)`` coordinates."""

    zero = parameter * 0
    return zero, 2 * parameter * (1 - parameter), zero + 2


def branch_root(parameter: Number, branch: str) -> Number:
    """Return the marked root belonging to a named inverse branch."""

    if branch == "zero":
        return parameter * 0
    if branch == "moving":
        return parameter
    if branch == "remaining":
        return 1 - parameter
    raise KeyError(f"unknown marked-root branch: {branch}")


def target_polynomial_derivative(parameter: Number, root: Number) -> Number:
    """Evaluate the derivative of ``2T(T-s)(T-(1-s))`` at ``root``."""

    s = parameter
    t = root
    return 6 * t**2 - 4 * t + 2 * s * (1 - s)


def sheet_point(parameter: Number, branch: str) -> Point3[Number]:
    """Lift the target family using one selected simple root.

    The formula is the normalized-root inverse from the paper.  It is undefined
    exactly when the selected root ceases to be simple.
    """

    root = branch_root(parameter, branch)
    rho = target_polynomial_derivative(parameter, root)
    if rho == 0:
        raise ZeroDivisionError("the selected root is repeated")
    x = 2 / rho
    y = root - rho / 2
    z = 5 * rho**2 / 4 - 3 * root * rho / 2 - rho**3 / 4
    return x, y, z


def _linspace(start: float, stop: float, samples: int) -> list[float]:
    if samples < 2:
        raise ValueError("samples must be at least two")
    step = (stop - start) / (samples - 1)
    return [start + index * step for index in range(samples)]


def _clean_float(value: object) -> float:
    return round(float(value), 12)


def _sample(
    function: Callable[[float], Sequence[object]],
    start: float,
    stop: float,
    samples: int,
) -> list[dict[str, object]]:
    return [
        {
            "parameter": _clean_float(parameter),
            "point": [_clean_float(value) for value in function(parameter)],
        }
        for parameter in _linspace(start, stop, samples)
    ]


def curve_payload(samples: int = 61) -> dict[str, object]:
    """Return sampled, web-ready curve data generated from the exact formulas."""

    elementary_domains = {
        "x_axis": (-1.2, 1.2),
        "y_axis": (-0.7, 0.7),
        "z_axis": (-1.2, 1.2),
    }
    elementary = []
    for curve_id, domain in elementary_domains.items():
        start, stop = domain
        elementary.append(
            {
                "id": curve_id,
                "domain": [start, stop],
                "source": _sample(
                    lambda value, selected=curve_id: elementary_source(selected, value),
                    start,
                    stop,
                    samples,
                ),
                "target": _sample(
                    lambda value, selected=curve_id: elementary_target(selected, value),
                    start,
                    stop,
                    samples,
                ),
            }
        )
    sheet_start, sheet_stop = 0.08, 0.30
    return {
        "schema_version": 1,
        "space_note": (
            "Because C^3 has six real dimensions, these samples show only its R^3 "
            "real slice."
        ),
        "coordinate_order": ["x", "y", "z"],
        "target_coordinate_order": ["a", "b", "c"],
        "map_formula": [
            "(1+x*y)^3*z + y^2*(1+x*y)*(4+3*x*y)",
            "y + 3*x*(1+x*y)^2*z + 3*x*y^2*(4+3*x*y)",
            "2*x - 3*x^2*y - x^3*z",
        ],
        "elementary_curves": elementary,
        "sheet_family": {
            "polynomial": "2*T*(T-s)*(T-(1-s))",
            "domain": [sheet_start, sheet_stop],
            "target": _sample(target_family, sheet_start, sheet_stop, samples),
            "branches": {
                branch: _sample(
                    lambda value, selected=branch: sheet_point(value, selected),
                    sheet_start,
                    sheet_stop,
                    samples,
                )
                for branch in BRANCHES
            },
        },
        "three_point_fiber": {
            "source": [
                [0.0, 0.0, -0.25],
                [1.0, -1.5, 6.5],
                [-1.0, 1.5, 6.5],
            ],
            "target": [-0.25, 0.0, 0.0],
        },
    }


def export_curve_data(path: str | Path, samples: int = 61) -> Path:
    """Write deterministic sampled curves for a browser or another renderer."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(curve_payload(samples=samples), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def exact_demo_parameters() -> tuple[Fraction, ...]:
    """Convenient nondegenerate rational parameters for certificate tests."""

    return Fraction(1, 10), Fraction(1, 5), Fraction(3, 10)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export exact Jacobian story curves")
    parser.add_argument("output", type=Path)
    parser.add_argument("--samples", type=int, default=61)
    arguments = parser.parse_args()
    export_curve_data(arguments.output, samples=arguments.samples)
