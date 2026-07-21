"""Compile every canonical film formula with the scene's exact TeX template.

This is a targeted renderer preflight.  DVI mode checks LaTeX syntax and the
base TeX dependency; ``--svg`` additionally exercises the native ``dvisvgm``
converter required by Manim.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from manim import config
from manim.utils.tex_file_writing import (
    compile_tex,
    convert_to_svg,
    generate_tex_file,
)

try:
    from animations.formula_data import DISPLAY_FORMULAS
    from animations.jacobian_story import MATH_TEX_TEMPLATE
except ModuleNotFoundError:  # Allow invocation from animations/.
    from formula_data import DISPLAY_FORMULAS  # type: ignore[no-redef]
    from jacobian_story import MATH_TEX_TEMPLATE  # type: ignore[no-redef]


def verify_formulas(output_dir: Path, convert_svg: bool = False) -> list[Path]:
    """Compile all registered displays and return the generated artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    config.media_dir = output_dir
    config.no_latex_cleanup = True
    generated: list[Path] = []
    for formula in DISPLAY_FORMULAS.values():
        tex_file = generate_tex_file(
            formula,
            environment="align*",
            tex_template=MATH_TEX_TEMPLATE,
        )
        dvi_file = compile_tex(
            tex_file,
            MATH_TEX_TEMPLATE.tex_compiler,
            MATH_TEX_TEMPLATE.output_format,
        )
        generated.append(
            convert_to_svg(dvi_file, MATH_TEX_TEMPLATE.output_format)
            if convert_svg
            else dvi_file
        )
    return generated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument(
        "--svg",
        action="store_true",
        help="also require dvisvgm and convert every DVI artifact to SVG",
    )
    args = parser.parse_args()
    artifacts = verify_formulas(args.output_dir, convert_svg=args.svg)
    kind = "SVG" if args.svg else "DVI"
    print(f"compiled {len(artifacts)} canonical formulas to {kind}")
    print(artifacts[0].parent)


if __name__ == "__main__":
    main()
