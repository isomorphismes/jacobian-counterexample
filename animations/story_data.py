"""Canonical narration, provenance, and transcript metadata.

This module deliberately has no Manim dependency.  The animation, tests, and
future landing page exports all read the same records.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Iterable


STORY_TITLE = "One map, three descriptions"
STORY_SUBTITLE = "The marked-root map behind a noninjective Keller map"
STORY_LICENSE = "CC-BY-4.0"
TARGET_DURATION_SECONDS = 345
DEFAULT_WORDS_PER_MINUTE = 128


@dataclass(frozen=True)
class Credit:
    name: str
    role: str
    url: str | None = None


@dataclass(frozen=True)
class StorySegment:
    id: str
    chapter: str
    title: str
    narration: str
    on_screen: tuple[str, ...]


CREDITS: tuple[Credit, ...] = (
    Credit(
        "Levent Alpöge",
        "Public announcement of the explicit polynomial map; the post credits "
        "Akhil for the question and Fable for the work.",
        "https://x.com/__alpoge__/status/2079028340955197566",
    ),
    Credit(
        "Fable",
        "Credited in Alpöge's announcement for work on the explicit construction.",
    ),
    Credit(
        "Andy Jiang (@davikrehalt)",
        "Posted the projective symmetric-product marked-root description, "
        "explicitly presenting it in the post as GPT output.",
        "https://x.com/davikrehalt/status/2079175065695035442",
    ),
    Credit(
        "GPT",
        "Credited by Jiang's post for the projective marked-root formulation.",
    ),
    Credit(
        "Aaron Lou",
        "Gave the factorization-resultant derivation and a global affine chart.",
        "https://aaronlou.com/jacobian_counterexample_derivation.pdf",
    ),
    Credit(
        "Repository contributors",
        "Compilation, independent checking, exposition, animation, and landing page; "
        "no claim to the discoveries above.",
    ),
)


SEGMENTS: tuple[StorySegment, ...] = (
    StorySegment(
        "credits",
        "Provenance",
        "Three public descriptions",
        "This map reached the public in three distinct forms. Levent Alpöge posted "
        "the explicit polynomial formula, crediting Akhil for the question and "
        "Fable for the work. Later, Andy Jiang, at davikrehalt, posted the "
        "projective marked-root description and explicitly presented it as GPT "
        "output. Aaron Lou then gave a resultant-based derivation and global "
        "affine chart. This repository compiles, explains, visualizes, and checks "
        "those contributions.",
        (
            "Levent Alpöge + credited Fable — explicit formula",
            "Andy Jiang (@davikrehalt) + credited GPT — projective model",
            "Aaron Lou — resultant derivation and affine chart",
        ),
    ),
    StorySegment(
        "local_global",
        "The puzzle",
        "Local invertibility can fail globally",
        "The Jacobian condition is local: at every finite point, the derivative is "
        "invertible. Imagine a tiny neighborhood being moved without being pinched "
        "flat. The surprise is global. Different distant points can still acquire "
        "the same image if inverse branches disappear through infinity. That is the "
        "mechanism we will see.",
        (
            "det DF = -2 everywhere",
            "No finite critical point",
            "Global branches can escape at infinity",
        ),
    ),
    StorySegment(
        "formula",
        "Levent and Fable",
        "The explicit polynomial certificate",
        "Alpöge's presentation begins with three explicit polynomials in x, y, "
        "and z. Exact symbolic expansion gives determinant minus two everywhere. "
        "The formula is the fastest certificate that the map is locally invertible, "
        "but by itself it gives little clue why these particular terms fit together.",
        (
            "Explicit F: affine three-space to affine three-space",
            "Exact identity: det DF = -2",
        ),
    ),
    StorySegment(
        "three_points",
        "Levent and Fable",
        "Three points, one value",
        "Now substitute these three source points. They are distinct, yet every one "
        "maps to negative one quarter, zero, zero. This already proves "
        "noninjectivity. The remaining descriptions explain the hidden object that "
        "each point is recording.",
        (
            "(0, 0, -1/4)",
            "(1, -3/2, 13/2)",
            "(-1, 3/2, 13/2)",
            "all map to (-1/4, 0, 0)",
        ),
    ),
    StorySegment(
        "mark_roots",
        "The common idea",
        "Mark one root, then forget the mark",
        "A cubic has three projective roots when multiplicity is counted. "
        "Temporarily mark one root and leave the other two unordered. For a cubic "
        "with three distinct roots, there are exactly three possible markings. If "
        "we now forget the mark, those three choices become one cubic. Generic "
        "degree three is therefore built into the construction.",
        (
            "cubic + one marked simple root",
            "forget the mark",
            "three generic choices become one cubic",
        ),
    ),
    StorySegment(
        "projective_map",
        "Jiang and GPT",
        "The projective marked-root map",
        "Jiang's post packages this as a projective map. A point p and an unordered "
        "pair q, r are sent to the unordered triple p, q, r. In symbols, projective "
        "one-space times its second symmetric power maps to its third symmetric "
        "power. This is simply the operation: forget which root was distinguished.",
        (
            "P¹ × Sym²(P¹) → Sym³(P¹)",
            "(p, {q,r}) ↦ {p,q,r}",
        ),
    ),
    StorySegment(
        "delete_ramification",
        "Jiang and GPT",
        "Delete only bad marked roots",
        "The forgetful map ramifies only when the marked root collides with one of "
        "the two residual roots. Delete exactly that ramification divisor. The "
        "unmarked roots may still collide with each other. After deletion, the "
        "differential is invertible everywhere that remains, so the restricted map "
        "is étale.",
        (
            "delete: marked root = residual root",
            "keep: the two unmarked roots may coincide",
            "remaining map is étale",
        ),
    ),
    StorySegment(
        "affine_slice",
        "Jiang and GPT",
        "The affine-space miracle",
        "Next choose a hyperplane tangent, but not osculating, to the small diagonal "
        "of triple roots. Its complement in projective three-space is affine "
        "three-space. Remarkably, the corresponding source complement is also "
        "affine three-space. Choosing coordinates on these two spaces turns the "
        "geometric forgetful map into Alpöge's polynomial map.",
        (
            "H tangent, not osculating, to the triple-root curve",
            "target complement ≅ A³",
            "source complement ≅ A³",
        ),
    ),
    StorySegment(
        "factorization",
        "Lou",
        "A marked root is a factor",
        "Lou's description replaces a marked root by a factorization of the binary "
        "cubic: a linear factor ell for the marked root, times a quadratic factor q "
        "for the other two. But the factorization has a redundant scale. "
        "Multiplying ell by s and q by s inverse leaves the cubic unchanged.",
        (
            "C = ell · q",
            "(ell, q) ~ (s ell, s⁻¹ q)",
        ),
    ),
    StorySegment(
        "resultant",
        "Lou",
        "The resultant fixes the scale",
        "The linear-quadratic resultant detects whether the marked root is simple. "
        "It is nonzero exactly when ell and q have no common root. Under the "
        "redundant scaling, the resultant is multiplied by s. Requiring resultant "
        "one therefore chooses one and only one representative on every simple-root "
        "scaling orbit. This is the resultant gauge.",
        (
            "Res(ell, q) ≠ 0 means a simple marked root",
            "Res(s ell, s⁻¹ q) = s Res(ell, q)",
            "set Res = 1",
        ),
    ),
    StorySegment(
        "unified",
        "Equivalence",
        "Three languages for one arrow",
        "These are not competing maps. They are three coordinate systems for one "
        "arrow. Alpöge gives the direct formula and collision certificate. Jiang "
        "and GPT expose the marked-root geometry. Lou supplies the normalized "
        "factor space and global affine chart. Lou's coordinate map G equals an "
        "output reversal after F and a sign change in the source. That is left-right "
        "equivalence, not dynamical conjugacy.",
        (
            "formula = marked-root map = normalized multiplication",
            "G = R₀ ∘ F ∘ S₀",
            "left-right equivalent; not strict conjugacy",
        ),
    ),
    StorySegment(
        "real_curves",
        "Visualization",
        "Exact curves on the real slice",
        "Complex three-space has six real dimensions, so here we visualize only "
        "its real slice. Three elementary "
        "source curves are mapped exactly: the x-axis becomes a target line, the "
        "y-axis becomes a parabola, and the z-axis becomes another target line. "
        "The same formulas drive both this animation and the browser artifact.",
        (
            "visualization: R³ inside C³",
            "x-axis → line; y-axis → parabola; z-axis → line",
        ),
    ),
    StorySegment(
        "escaping_sheets",
        "Visualization",
        "Two inverse branches escape",
        "A more revealing target curve represents cubics with roots zero, s, and "
        "one minus s. Each possible marked root defines a different source curve, "
        "but all three map to the same target curve. As s approaches zero, two "
        "marked roots collide. Their two source branches run toward infinity, while "
        "the branch marking the remaining simple root stays finite. No finite "
        "critical point appears.",
        (
            "P_s(T) = 2T(T-s)(T-(1-s))",
            "three marked-root branches → one target curve",
            "two branches escape as s → 0",
        ),
    ),
    StorySegment(
        "proof_scope",
        "Conclusion",
        "The proof spine and its scope",
        "The proof now has a short spine. Both chosen complements are affine "
        "three-space. Removing marked-root ramification makes the forgetful map "
        "étale. A general cubic has three simple roots, so the map has generic "
        "degree three and cannot be injective. Constant Jacobian, three-point "
        "fibers, and escape at infinity are three views of the same geometry. "
        "Adding identity coordinates extends the construction to higher dimensions, "
        "while dimension two remains a separate problem.",
        (
            "A³ → A³",
            "étale + generic degree 3 + nonproper",
            "dimension two is separate",
        ),
    ),
)


def segment_by_id(segment_id: str) -> StorySegment:
    """Return one canonical story segment."""

    for segment in SEGMENTS:
        if segment.id == segment_id:
            return segment
    raise KeyError(f"unknown story segment: {segment_id}")


def spoken_word_count(text: str) -> int:
    """Count narration words using a deterministic, punctuation-agnostic rule."""

    return len(re.findall(r"[A-Za-zÀ-ž0-9]+(?:[-'][A-Za-zÀ-ž0-9]+)*", text))


def estimated_duration_seconds(
    segments: Iterable[StorySegment] = SEGMENTS,
    words_per_minute: int = DEFAULT_WORDS_PER_MINUTE,
    pause_per_segment: float = 0.35,
) -> float:
    """Estimate spoken duration for planning and deterministic silent audio."""

    selected = tuple(segments)
    words = sum(spoken_word_count(segment.narration) for segment in selected)
    return words * 60.0 / words_per_minute + pause_per_segment * len(selected)


def story_payload() -> dict[str, object]:
    """Return JSON-serializable metadata for the animation and landing page."""

    return {
        "schema_version": 1,
        "title": STORY_TITLE,
        "subtitle": STORY_SUBTITLE,
        "license": STORY_LICENSE,
        "target_duration_seconds": TARGET_DURATION_SECONDS,
        "estimated_duration_seconds": round(estimated_duration_seconds(), 3),
        "credits": [asdict(credit) for credit in CREDITS],
        "segments": [asdict(segment) for segment in SEGMENTS],
    }


def export_story_json(path: str | Path) -> Path:
    """Export canonical story metadata for a web client."""

    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(story_payload(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return output


def render_transcript_markdown() -> str:
    """Render the public, text-first transcript from the canonical records."""

    lines = [
        f"# {STORY_TITLE}",
        "",
        STORY_SUBTITLE,
        "",
        "This is the canonical narration transcript. The three-dimensional scenes "
        "show the real slice `R^3` inside the complex map on `C^3`.",
        "",
        "## Provenance",
        "",
    ]
    for credit in CREDITS:
        name = f"[{credit.name}]({credit.url})" if credit.url else credit.name
        lines.append(f"- **{name}:** {credit.role}")
    lines.extend(["", "## Narration", ""])
    previous_chapter: str | None = None
    for segment in SEGMENTS:
        if segment.chapter != previous_chapter:
            lines.extend([f"### {segment.chapter}", ""])
            previous_chapter = segment.chapter
        lines.extend([f"#### {segment.title}", "", segment.narration, ""])
    lines.extend(
        [
            "## Accessibility note",
            "",
            "The narration states all mathematically essential motion. Root branches "
            "are distinguished by labels as well as color. The video captions are "
            "generated from this text and published as WebVTT.",
            "",
            "## License",
            "",
            "Narration text and original visual composition are CC BY 4.0; animation "
            "source code is MIT-licensed. Third-party materials retain their own terms.",
            "",
        ]
    )
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Export Jacobian story metadata")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    export_story_json(args.output)
