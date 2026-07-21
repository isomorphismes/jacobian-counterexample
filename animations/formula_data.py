"""Canonical TeX strings for mathematical displays in the Manim film.

This module has no Manim dependency so regression tests can verify the visual
formula contract without importing the rendering stack.
"""

from __future__ import annotations


DISPLAY_FORMULAS: dict[str, str] = {
    "complex_space": r"\mathbb C^3",
    "real_space": r"\mathbb R^3",
    "jacobian": r"\det DF=-2",
    "f1": r"F_1=(1+xy)^3z+y^2(1+xy)(4+3xy)",
    "f2": r"F_2=y+3x(1+xy)^2z+3xy^2(4+3xy)",
    "f3": r"F_3=2x-3x^2y-x^3z",
    "p0": r"P_0=\left(0,0,-\frac14\right)",
    "p1": r"P_1=\left(1,-\frac32,\frac{13}{2}\right)",
    "p2": r"P_2=\left(-1,\frac32,\frac{13}{2}\right)",
    "fiber_equality": r"F(P_0)=F(P_1)=F(P_2)",
    "fiber_target": r"\left(-\frac14,0,0\right)",
    "unordered_roots": r"\{p,q,r\}",
    "projective_map": (
        r"\mathbb P^1\times\operatorname{Sym}^2(\mathbb P^1)"
        r"\longrightarrow\operatorname{Sym}^3(\mathbb P^1)"
    ),
    "projective_point_map": r"(p,\{q,r\})\longmapsto\{p,q,r\}",
    "target_affine": r"\mathbb P^3\setminus H\simeq\mathbb A^3",
    "source_affine": r"X_{\mathrm{aff}}\simeq\mathbb A^3",
    "linear_factor": r"\ell",
    "quadratic_factor": r"q",
    "factor_product": r"C=\ell q",
    "factor_scale": r"(\ell,q)\sim(s\ell,s^{-1}q)",
    "resultant_nonzero": r"\operatorname{Res}(\ell,q)\ne0",
    "resultant_scale": (
        r"\operatorname{Res}(s\ell,s^{-1}q)"
        r"=s\operatorname{Res}(\ell,q)"
    ),
    "resultant_one": r"\operatorname{Res}(\ell,q)=1",
    "common_morphism": (
        r"(\text{cubic},\text{ marked simple root})"
        r"\longmapsto\text{cubic}"
    ),
    "explicit_map": r"F\colon\mathbb A^3\longrightarrow\mathbb A^3",
    "left_right": r"G=R_0\circ F\circ S_0",
    "source_a3": r"\text{source}\simeq\mathbb A^3",
    "target_a3": r"\text{target}\simeq\mathbb A^3",
    "sheet_polynomial": r"P_s(T)=2T(T-s)\bigl(T-(1-s)\bigr)",
    "proof_conclusion": (
        r"\text{local invertibility}+\text{escape at infinity}"
        r"=\text{global noninjectivity}"
    ),
}


# These are the formulas whose semantic presence is essential to the film.
# Tests require each one to pass through a MathTex-backed display helper.
KEY_DISPLAY_FORMULAS: tuple[str, ...] = (
    "jacobian",
    "f1",
    "f2",
    "f3",
    "fiber_equality",
    "projective_map",
    "projective_point_map",
    "factor_scale",
    "resultant_nonzero",
    "resultant_scale",
    "resultant_one",
    "left_right",
    "sheet_polynomial",
)
