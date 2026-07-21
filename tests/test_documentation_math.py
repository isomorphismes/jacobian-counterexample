"""Regression checks for math markup in the README and Jupyter Book."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
FENCE = re.compile(r"(?ms)^```.*?^```\s*$")
SINGLE_DOLLAR = re.compile(r"(?<!\\)(?<!\$)\$(?!\$)")
INLINE_CODE = re.compile(r"(?<!`)`([^`\n]+)`(?!`)")


def markdown_sources() -> list[tuple[Path, str]]:
    sources = [(ROOT / "README.md", (ROOT / "README.md").read_text(encoding="utf-8"))]
    sources.extend(
        (path, path.read_text(encoding="utf-8"))
        for path in sorted((ROOT / "knowledge").glob("*.md"))
    )
    for path in sorted((ROOT / "knowledge" / "notebooks").glob("*.ipynb")):
        notebook = json.loads(path.read_text(encoding="utf-8"))
        markdown = "\n".join(
            "".join(cell.get("source", []))
            for cell in notebook.get("cells", [])
            if cell.get("cell_type") == "markdown"
        )
        sources.append((path, markdown))
    return sources


def prose(markdown: str) -> str:
    return FENCE.sub("", markdown)


def test_docs_use_myst_and_github_math_delimiters() -> None:
    """LaTeX parentheses/brackets render literally in this MyST setup."""

    forbidden = (r"\(", r"\)", r"\[", r"\]")
    for path, source in markdown_sources():
        body = prose(source)
        for delimiter in forbidden:
            assert delimiter not in body, f"{path}: unsupported delimiter {delimiter!r}"
        assert not re.search(r"(?m)^\s*\[\s*$", body), path
        assert not re.search(r"(?m)^\s*\]\s*$", body), path
        assert not re.search(r"(?<!\\)\b(?:qquad|quad)\b", body), (
            f"{path}: TeX spacing command is missing its backslash"
        )


def test_dollar_math_delimiters_are_balanced() -> None:
    for path, source in markdown_sources():
        body = prose(source)
        assert body.count("$$") % 2 == 0, f"{path}: unbalanced display math"
        for display in re.findall(r"\$\$(.*?)\$\$", body, flags=re.DOTALL):
            assert not SINGLE_DOLLAR.search(display), (
                f"{path}: inline dollar delimiter nested inside display math"
            )
        without_displays = re.sub(r"\$\$.*?\$\$", "", body, flags=re.DOTALL)
        for line_number, line in enumerate(without_displays.splitlines(), 1):
            assert len(SINGLE_DOLLAR.findall(line)) % 2 == 0, (
                f"{path}:{line_number}: unbalanced inline math"
            )


def test_prose_code_spans_are_not_being_used_for_mathematics() -> None:
    """Backticks remain for commands, paths, filenames, and environment names."""

    for path, source in markdown_sources():
        if path.suffix == ".ipynb":
            # Notebook prose legitimately names Python objects such as ``Integer``.
            continue
        body = prose(source)
        for match in INLINE_CODE.finditer(body):
            value = match.group(1)
            if body[: match.start()].endswith("{cite}"):
                continue
            is_command = value.startswith("make ")
            is_path = "/" in value or value.startswith(".")
            is_filename = value.endswith((".py", ".m", ".sage", ".tex", ".pdf", ".html"))
            is_environment_name = re.fullmatch(r"[A-Z][A-Z0-9_]+", value) is not None
            assert is_command or is_path or is_filename or is_environment_name, (
                f"{path}: mathematical or unexplained literal code span `{value}`"
            )


def test_book_enables_mathjax_compatible_myst_extensions() -> None:
    config = (ROOT / "knowledge" / "_config.yml").read_text(encoding="utf-8")
    assert "- dollarmath" in config
    assert "- amsmath" in config
    assert "navigation_with_keys: false" in config

    bibliography = (ROOT / "knowledge" / "references.bib").read_text(
        encoding="utf-8"
    )
    assert "$" not in bibliography, (
        "sphinxcontrib-bibtex emits dollar-delimited title math literally"
    )
