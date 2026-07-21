"""Build the two repository-unique static film faces from pinned Inter."""

from __future__ import annotations

import hashlib
from io import BytesIO
from pathlib import Path

import fontTools
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


ROOT = Path(__file__).resolve().parent / "assets" / "fonts"
SOURCE = ROOT / "Inter-VariableFont_opsz-wght.ttf"
FONTTOOLS_VERSION = "4.51.0"
SOURCE_SHA256 = "29160a80ff49ddcab2c97711247e08b1fab27a484a329ce8b813d820dc559031"

FAMILY = "Jacobian Counterexample Film Text"
POSTSCRIPT_PREFIX = "JacobianCounterexampleFilmText"
VERSION = "Version 4.001-jcfilm.2;git-66647c0bb"
INSTANCE_LOCATION = {"opsz": 14.0}
FACES = {
    "Regular": {
        "weight": 400.0,
        "file": ROOT / "JacobianCounterexampleFilmText-Regular.ttf",
        "size": 341_712,
        "sha256": "2282daa5748d02c1ac3703811c778a5e4775d13f4563fc9957db7ab8402d664d",
    },
    "Bold": {
        "weight": 700.0,
        "file": ROOT / "JacobianCounterexampleFilmText-Bold.ttf",
        "size": 343_388,
        "sha256": "11ca1dd863323d2ab533be2e4094266b838f56040d18f9fbaa633b360585cb28",
    },
}
VARIABLE_TABLES = {"avar", "cvar", "fvar", "gvar", "HVAR", "MVAR", "VVAR"}


def sha256(path: Path) -> str:
    """Return a streaming SHA-256 digest."""

    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def names_for(style: str) -> dict[int, str]:
    """Return the exact public OpenType names for one static face."""

    postscript_name = f"{POSTSCRIPT_PREFIX}-{style}"
    return {
        1: FAMILY,
        2: style,
        3: f"4.001-jcfilm.2;git-66647c0bb;RSMS;{postscript_name}",
        4: f"{FAMILY} {style}",
        5: VERSION,
        6: postscript_name,
        16: FAMILY,
        17: style,
        25: POSTSCRIPT_PREFIX,
    }


def build_face(style: str, weight: float, output: Path) -> None:
    """Instantiate and rename one face without changing its static design."""

    source = TTFont(SOURCE, recalcTimestamp=False)
    location = {**INSTANCE_LOCATION, "wght": weight}
    font = instantiateVariableFont(
        source,
        location,
        inplace=False,
        optimize=True,
        updateFontNames=True,
    )
    # A first serialization lets FontTools finalize dependent static tables
    # such as ``loca`` before we capture the reference design.  Name changes
    # below must leave every other compiled table (apart from ``head``'s file
    # checksum) identical to this direct upstream instance.
    reference_buffer = BytesIO()
    font.save(reference_buffer, reorderTables=True)
    reference = TTFont(BytesIO(reference_buffer.getvalue()), recalcTimestamp=False)
    reference_tables = {
        tag: reference.getTableData(tag)
        for tag in reference.keys()
        if tag != "GlyphOrder"
    }

    expected_names = names_for(style)
    rewritten_ids = set(expected_names) - {16, 17}
    changed: set[int] = set()
    for record in font["name"].names:
        if record.nameID not in rewritten_ids:
            continue
        record.string = expected_names[record.nameID].encode(record.getEncoding())
        changed.add(record.nameID)
    if changed != rewritten_ids:
        raise RuntimeError(f"missing expected source names: {rewritten_ids - changed}")

    # Inter 4.001 omits these typographic names.  Pango on macOS can list a
    # renamed family while silently falling back for its Bold face unless the
    # family/subfamily pair is explicit in name IDs 16 and 17.
    font["name"].setName(FAMILY, 16, 3, 1, 0x0409)
    font["name"].setName(style, 17, 3, 1, 0x0409)
    font.save(output, reorderTables=True)

    derived = TTFont(output, recalcTimestamp=False)
    unexpected_variable_tables = VARIABLE_TABLES & set(derived.keys())
    if unexpected_variable_tables:
        raise RuntimeError(
            f"static {style} face retained variable tables: "
            f"{sorted(unexpected_variable_tables)}"
        )
    if derived["OS/2"].usWeightClass != int(weight):
        raise RuntimeError(f"static {style} face has the wrong weight class")
    expected_bold_bit = 1 if style == "Bold" else 0
    if derived["head"].macStyle & 1 != expected_bold_bit:
        raise RuntimeError(f"static {style} face has the wrong bold style bit")

    for tag, raw_table in reference_tables.items():
        if tag not in {"head", "name"} and derived.getTableData(tag) != raw_table:
            raise RuntimeError(f"unexpected modification to {style} table {tag}")
    for name_id, expected in expected_names.items():
        values = {
            record.toUnicode()
            for record in derived["name"].names
            if record.nameID == name_id
        }
        if values != {expected}:
            raise RuntimeError(
                f"derived {style} name {name_id} is not exact: {values}"
            )


def main() -> None:
    """Build both faces and verify their exact reproducible bytes."""

    if fontTools.__version__ != FONTTOOLS_VERSION:
        raise RuntimeError(
            f"FontTools {FONTTOOLS_VERSION} is required, found {fontTools.__version__}"
        )
    if sha256(SOURCE) != SOURCE_SHA256:
        raise RuntimeError("upstream Inter source hash does not match the pinned input")

    for style, specification in FACES.items():
        output = specification["file"]
        assert isinstance(output, Path)
        build_face(style, float(specification["weight"]), output)
        if output.stat().st_size != specification["size"]:
            raise RuntimeError(f"derived {style} size does not match the pinned output")
        if sha256(output) != specification["sha256"]:
            raise RuntimeError(f"derived {style} hash does not match the pinned output")
        print(f"wrote {output.relative_to(Path.cwd())}: {specification['sha256']}")


if __name__ == "__main__":
    main()
