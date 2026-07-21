"""Cross-artifact release checks for the public mathematical explainer."""

from __future__ import annotations

from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[1]
ALPOGE_POST = "https://x.com/__alpoge__/status/2079028340955197566"
JIANG_POST = "https://x.com/davikrehalt/status/2079175065695035442"
LOU_NOTE = "https://aaronlou.com/jacobian_counterexample_derivation.pdf"
LOU_PROFILE = "https://x.com/aaron_lou"
LITT_BUNDLE_POST = "https://x.com/littmath/status/2079347618417971212"
LITT_PENCIL_POST = "https://x.com/littmath/status/2079353531430289734"
LITT_ASSISTANCE_POST = "https://x.com/littmath/status/2079414119720165633"
LITT_COMPARISON_POST = "https://x.com/littmath/status/2079475742401003816"
KELLER_DOI = "https://doi.org/10.1007/BF01695502"
BCW_DOI = "https://doi.org/10.1090/S0273-0979-1982-15032-7"
DRUZKOWSKI_DOI = "https://doi.org/10.1007/BF01459126"


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_critical_primary_sources_are_present_across_public_exposition() -> None:
    public_sources = (
        "README.md",
        "src/distinguished_root_map.tex",
        "site/index.html",
        "animations/story_data.py",
    )
    for path in public_sources:
        contents = text(path)
        assert ALPOGE_POST in contents, path
        assert JIANG_POST in contents, path
        assert LOU_NOTE in contents, path
        assert "@aaron_lou" in contents.replace(r"\_", "_"), path

    linked_profile_sources = (
        "README.md",
        "src/distinguished_root_map.tex",
        "site/index.html",
        "knowledge/index.md",
        "knowledge/literature-audit.md",
        "knowledge/paper-comparison.md",
        "knowledge/resultant-factor-route.md",
    )
    for path in linked_profile_sources:
        assert LOU_PROFILE in text(path), path


def test_compiler_role_is_not_presented_as_discovery_authorship() -> None:
    readme = text("README.md")
    paper = text("src/distinguished_root_map.tex")
    site = text("site/index.html")
    assert "does **not** claim" in readme
    assert "does not claim discovery authorship" in paper
    assert "does not claim" in site.lower()
    assert "Bartosz Naskrecki" in readme
    assert "Bartosz Naskrecki" in paper
    assert "Bartosz Naskrecki" in site


def test_litt_pencil_bundle_explanation_is_credited_in_the_paper() -> None:
    paper = text("src/distinguished_root_map.tex")
    assert "@littmath" in paper
    assert LITT_BUNDLE_POST in paper
    assert LITT_PENCIL_POST in paper
    assert LITT_ASSISTANCE_POST in paper
    assert LITT_COMPARISON_POST in paper


def test_historical_literature_links_use_the_canonical_dois() -> None:
    site = text("site/index.html")
    bibliography = text("knowledge/references.bib")
    paper = text("src/distinguished_root_map.tex")
    assert KELLER_DOI in site and KELLER_DOI in paper
    assert BCW_DOI in site and BCW_DOI in paper
    assert DRUZKOWSKI_DOI in site
    assert DRUZKOWSKI_DOI.removeprefix("https://doi.org/") in bibliography
    assert "10.4064/ap-44-2-115-120" not in site


def test_real_slice_warning_is_visible_in_every_visual_explainer() -> None:
    site = text("site/index.html")
    animation = text("animations/story_data.py")
    assert "six real dimensions" in site
    assert "real slice" in site.lower()
    assert "six real dimensions" in animation
    assert "real slice" in animation.lower()


def test_dual_license_files_and_canonical_pdf_exist() -> None:
    assert "MIT License" in text("LICENSE-CODE")
    assert "CC BY 4.0" in text("LICENSE-CONTENT")
    transcript = text("animations/transcript.md")
    assert "Narration text and original visual composition are CC BY 4.0" in transcript
    assert "animation source code is MIT-licensed" in transcript
    pdf = ROOT / "output/pdf/one_map_three_descriptions.pdf"
    assert pdf.stat().st_size > 100_000
    assert pdf.read_bytes()[:5] == b"%PDF-"


def test_elementary_real_curves_match_the_map_exactly() -> None:
    t = sp.symbols("t")
    x, y, z = sp.symbols("x y z")
    mapping = sp.Matrix(
        [
            (1 + x * y) ** 3 * z
            + y**2 * (1 + x * y) * (4 + 3 * x * y),
            y
            + 3 * x * (1 + x * y) ** 2 * z
            + 3 * x * y**2 * (4 + 3 * x * y),
            2 * x - 3 * x**2 * y - x**3 * z,
        ]
    )
    cases = (
        ({x: t, y: 0, z: 0}, sp.Matrix([0, 0, 2 * t])),
        ({x: 0, y: t, z: 0}, sp.Matrix([4 * t**2, t, 0])),
        ({x: 0, y: 0, z: t}, sp.Matrix([t, 0, 0])),
    )
    for source, expected in cases:
        assert all(sp.expand(value) == 0 for value in mapping.subs(source) - expected)


def test_three_marked_root_sheets_have_one_target_curve() -> None:
    s, t = sp.symbols("s t")
    polynomial = 2 * t * (t - s) * (t - (1 - s))
    derivative = sp.diff(polynomial, t)
    target = sp.Matrix([0, 2 * s * (1 - s), 2])
    x, y, z = sp.symbols("x y z")
    mapping = sp.Matrix(
        [
            (1 + x * y) ** 3 * z
            + y**2 * (1 + x * y) * (4 + 3 * x * y),
            y
            + 3 * x * (1 + x * y) ** 2 * z
            + 3 * x * y**2 * (4 + 3 * x * y),
            2 * x - 3 * x**2 * y - x**3 * z,
        ]
    )

    for root in (sp.Integer(0), s, 1 - s):
        rho = sp.expand(derivative.subs(t, root))
        source = {
            x: 2 / rho,
            y: root - rho / 2,
            z: 5 * rho**2 / 4
            - 3 * root * rho / 2
            - rho**3 / 4,
        }
        difference = mapping.subs(source) - target
        assert all(sp.factor(value) == 0 for value in difference)
