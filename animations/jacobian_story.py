"""Narrated Manim explainer for the marked-root Jacobian map.

Render in deterministic silent mode (the default) for CI, set
``JACOBIAN_VOICE_SERVICE=piper`` for reproducible offline draft narration, or
use ``recorder`` for the final human narration. Formula cards use Pango
``Text`` rather than ``MathTex``, so the scene does not depend on ``dvisvgm``.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
import wave

from manim import (
    Arrow,
    Circle,
    Create,
    DEGREES,
    DOWN,
    Dot,
    Dot3D,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    LEFT,
    Line,
    ParametricFunction,
    RIGHT,
    RoundedRectangle,
    Text,
    ThreeDAxes,
    ThreeDScene,
    Transform,
    UP,
    ValueTracker,
    VGroup,
    always_redraw,
    linear,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover.helper import remove_bookmarks
from manim_voiceover.services.base import SpeechService

try:
    from animations.math_core import (
        BRANCHES,
        elementary_source,
        elementary_target,
        sheet_point,
        target_family,
    )
    from animations.story_data import segment_by_id, spoken_word_count
except ModuleNotFoundError:  # Allow ``manim`` invocation from animations/.
    from math_core import (  # type: ignore[no-redef]
        BRANCHES,
        elementary_source,
        elementary_target,
        sheet_point,
        target_family,
    )
    from story_data import segment_by_id, spoken_word_count  # type: ignore[no-redef]


BACKGROUND = "#08111F"
PANEL = "#13243A"
INK = "#F2F7FF"
MUTED = "#A9B9CF"
BLUE = "#53C8E8"
GREEN = "#65D6A6"
GOLD = "#FFC857"
MAGENTA = "#EF7EB8"
RED = "#FF6B6B"
BRANCH_COLORS = {
    "zero": BLUE,
    "moving": MAGENTA,
    "remaining": GREEN,
}


class DeterministicSilenceService(SpeechService):
    """Offline voice service that emits deterministic silent WAV clips.

    It keeps the VoiceoverScene timing and SRT path exercised in CI without a
    microphone, network call, API key, or speech model.  It is not intended for
    the published narration.
    """

    def __init__(
        self,
        words_per_minute: int = 128,
        pause_seconds: float = 0.35,
        sample_rate: int = 16_000,
        **kwargs: object,
    ) -> None:
        super().__init__(transcription_model=None, **kwargs)
        self.words_per_minute = words_per_minute
        self.pause_seconds = pause_seconds
        self.sample_rate = sample_rate

    def generate_from_text(
        self,
        text: str,
        cache_dir: str | os.PathLike[str] | None = None,
        path: str | os.PathLike[str] | None = None,
        **kwargs: object,
    ) -> dict[str, object]:
        del kwargs
        clean_text = remove_bookmarks(text)
        duration = max(
            1.25,
            spoken_word_count(clean_text) * 60.0 / self.words_per_minute
            + self.pause_seconds,
        )
        input_data = {
            "input_text": clean_text,
            "service": "deterministic-silence",
            "words_per_minute": self.words_per_minute,
            "pause_seconds": self.pause_seconds,
            "sample_rate": self.sample_rate,
        }
        output_dir = Path(self.cache_dir if cache_dir is None else cache_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        cached = self.get_cached_result(input_data, output_dir)
        if cached is not None:
            cached_audio = output_dir / str(cached["original_audio"])
            if cached_audio.is_file():
                return cached

        filename = (
            Path(path).name
            if path is not None
            else f"{self.get_audio_basename(input_data)}.wav"
        )
        audio_path = output_dir / filename
        frame_count = round(duration * self.sample_rate)
        silent_chunk = b"\x00\x00" * 4096
        with wave.open(str(audio_path), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(self.sample_rate)
            remaining = frame_count
            while remaining:
                chunk_frames = min(remaining, 4096)
                audio.writeframesraw(silent_chunk[: chunk_frames * 2])
                remaining -= chunk_frames
            audio.writeframes(b"")
        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": filename,
        }


def build_speech_service() -> SpeechService:
    """Select the explicit CI, offline-draft, or final voice strategy."""

    mode = os.getenv("JACOBIAN_VOICE_SERVICE", "silent").strip().lower()
    if mode == "silent":
        return DeterministicSilenceService()
    if mode == "piper":
        try:
            from animations.piper_service import PiperSpeechService
        except ModuleNotFoundError:  # Allow invocation from animations/.
            from piper_service import PiperSpeechService  # type: ignore[no-redef]

        return PiperSpeechService()
    if mode == "recorder":
        from manim_voiceover.services.recorder import RecorderService

        # Sentence-level captions do not need Whisper word boundaries.
        return RecorderService(transcription_model=None)
    raise ValueError(
        "JACOBIAN_VOICE_SERVICE must be 'silent', 'piper', or 'recorder', "
        f"not {mode!r}"
    )


class JacobianStory(ThreeDScene, VoiceoverScene):
    """Approximately six-minute, attribution-first visual proof guide."""

    def construct(self) -> None:
        self.camera.background_color = BACKGROUND
        self.set_speech_service(build_speech_service(), create_subcaption=True)
        self._provenance()
        self._explicit_certificate()
        self._marked_roots()
        self._resultant_route()
        self._unification()
        self._curve_visualization()
        self._proof_and_credits()

    def _voice(self, segment_id: str):
        segment = segment_by_id(segment_id)
        return self.voiceover(
            text=segment.narration,
            max_subcaption_len=48,
            subcaption_buff=0.08,
        )

    @staticmethod
    def _run_time(tracker: object, fraction: float, minimum: float = 0.6) -> float:
        duration = float(getattr(tracker, "duration"))
        return max(minimum, duration * fraction)

    @staticmethod
    def _heading(title: str, subtitle: str | None = None) -> VGroup:
        heading = Text(title, color=INK, font_size=42, weight="BOLD")
        if subtitle is None:
            return VGroup(heading).to_edge(UP, buff=0.35)
        subheading = Text(subtitle, color=MUTED, font_size=24)
        return VGroup(heading, subheading).arrange(DOWN, buff=0.13).to_edge(UP, buff=0.3)

    @staticmethod
    def _card(
        title: str,
        lines: tuple[str, ...],
        color: str = BLUE,
        width: float = 4.0,
        font_size: int = 22,
    ) -> VGroup:
        title_text = Text(title, color=color, font_size=27, weight="BOLD")
        body_lines = [Text(line, color=INK, font_size=font_size) for line in lines]
        body = VGroup(*body_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        content = VGroup(title_text, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        content.scale_to_fit_width(min(content.width, width - 0.45))
        height = max(1.35, content.height + 0.48)
        panel = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.16,
            stroke_color=color,
            stroke_width=2,
            fill_color=PANEL,
            fill_opacity=0.92,
        )
        content.move_to(panel)
        return VGroup(panel, content)

    def _clear(self, run_time: float = 0.45) -> None:
        visible = list(self.mobjects)
        if visible:
            self.play(*(FadeOut(item) for item in visible), run_time=run_time)

    def _provenance(self) -> None:
        self.next_section("01-provenance")
        heading = self._heading("One map, three descriptions", "Provenance before proof")
        cards = VGroup(
            self._card(
                "Levent Alpöge + credited Fable",
                ("explicit formula", "Jacobian and collision certificate"),
                BLUE,
                width=4.15,
                font_size=19,
            ),
            self._card(
                "Andy Jiang + credited GPT",
                ("projective marked-root model", "posted by @davikrehalt"),
                MAGENTA,
                width=4.15,
                font_size=19,
            ),
            self._card(
                "Aaron Lou",
                ("resultant normalization", "global affine chart"),
                GREEN,
                width=4.15,
                font_size=19,
            ),
        ).arrange(RIGHT, buff=0.25).shift(DOWN * 0.25)
        footer = Text(
            "Repository role: compile · explain · visualize · check",
            color=MUTED,
            font_size=24,
        ).to_edge(DOWN, buff=0.45)
        with self._voice("credits") as tracker:
            self.play(FadeIn(heading), run_time=self._run_time(tracker, 0.12))
            self.play(
                LaggedStart(*(FadeIn(card, shift=UP * 0.15) for card in cards), lag_ratio=0.22),
                run_time=self._run_time(tracker, 0.52),
            )
            self.play(FadeIn(footer), run_time=self._run_time(tracker, 0.12))
        self._clear()

    def _explicit_certificate(self) -> None:
        self.next_section("02-local-versus-global")
        heading = self._heading("Locally invertible. Globally surprising.")
        source = self._card("SOURCE  C³", ("three distant points",), BLUE, width=4.2)
        target = self._card("TARGET  C³", ("one shared value",), GREEN, width=4.2)
        source.shift(LEFT * 3.5 + DOWN * 0.2)
        target.shift(RIGHT * 3.5 + DOWN * 0.2)
        arrow = Arrow(source.get_right(), target.get_left(), color=GOLD, buff=0.2)
        jacobian = Text("det DF = -2  everywhere", color=GOLD, font_size=34).shift(DOWN * 2.25)
        infinity = Text(
            "inverse branches can leave through infinity",
            color=MUTED,
            font_size=23,
        ).next_to(jacobian, DOWN, buff=0.23)
        with self._voice("local_global") as tracker:
            self.play(FadeIn(heading), FadeIn(source), run_time=self._run_time(tracker, 0.22))
            self.play(Create(arrow), FadeIn(target), run_time=self._run_time(tracker, 0.25))
            self.play(FadeIn(jacobian), run_time=self._run_time(tracker, 0.2))
            self.play(FadeIn(infinity), run_time=self._run_time(tracker, 0.12))
        self._clear()

        self.next_section("03-explicit-formula")
        heading = self._heading("Levent's explicit formula", "The quickest exact certificate")
        formula_lines = VGroup(
            Text("F₁ = (1+xy)³z + y²(1+xy)(4+3xy)", color=BLUE, font_size=27),
            Text("F₂ = y + 3x(1+xy)²z + 3xy²(4+3xy)", color=GREEN, font_size=27),
            Text("F₃ = 2x - 3x²y - x³z", color=MAGENTA, font_size=27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).shift(DOWN * 0.15)
        determinant = self._card(
            "Exact symbolic identity",
            ("det DF = -2", "no pointwise approximation"),
            GOLD,
            width=4.2,
        ).to_edge(DOWN, buff=0.45)
        with self._voice("formula") as tracker:
            self.play(FadeIn(heading), run_time=self._run_time(tracker, 0.12))
            self.play(
                LaggedStart(*(FadeIn(line, shift=RIGHT * 0.15) for line in formula_lines), lag_ratio=0.18),
                run_time=self._run_time(tracker, 0.48),
            )
            self.play(FadeIn(determinant), run_time=self._run_time(tracker, 0.18))
        self._clear()

        self.next_section("04-three-point-fiber")
        heading = self._heading("Three points, one image", "An exact noninjectivity certificate")
        colors = (BLUE, MAGENTA, GREEN)
        point_text = (
            "(0, 0, -1/4)",
            "(1, -3/2, 13/2)",
            "(-1, 3/2, 13/2)",
        )
        points = VGroup(
            *[
                self._card(f"P{index}", (label,), color, width=3.2, font_size=21)
                for index, (label, color) in enumerate(zip(point_text, colors))
            ]
        ).arrange(DOWN, buff=0.2).shift(LEFT * 3.5 + DOWN * 0.2)
        target = self._card("F(P₀) = F(P₁) = F(P₂)", ("(-1/4, 0, 0)",), GOLD, width=4.3)
        target.shift(RIGHT * 3.3 + DOWN * 0.2)
        arrows = VGroup(
            *[
                Arrow(point.get_right(), target.get_left(), buff=0.15, color=color, stroke_width=3)
                for point, color in zip(points, colors)
            ]
        )
        with self._voice("three_points") as tracker:
            self.play(FadeIn(heading), FadeIn(points), run_time=self._run_time(tracker, 0.28))
            self.play(
                LaggedStart(*(Create(arrow) for arrow in arrows), lag_ratio=0.18),
                FadeIn(target),
                run_time=self._run_time(tracker, 0.42),
            )
            self.play(Indicate(target, color=GOLD), run_time=self._run_time(tracker, 0.13))
        self._clear()

    def _marked_roots(self) -> None:
        self.next_section("05-mark-one-root")
        heading = self._heading("A cubic with one marked root", "The shared hidden object")
        root_circle = Circle(radius=2.0, color=MUTED, stroke_width=3).shift(LEFT * 2.7 + DOWN * 0.2)
        angles = (math.pi / 2, math.pi + 0.3, -0.25)
        colors = (BLUE, MAGENTA, GREEN)
        root_names = ("p", "q", "r")
        roots = VGroup(
            *[
                Dot(root_circle.point_at_angle(angle), radius=0.12, color=color)
                for angle, color in zip(angles, colors)
            ]
        )
        labels = VGroup(
            *[
                Text(name, color=color, font_size=27).next_to(dot, UP, buff=0.12)
                for name, color, dot in zip(root_names, colors, roots)
            ]
        )
        mark = Circle(radius=0.24, color=GOLD, stroke_width=5).move_to(roots[0])
        cubic = self._card(
            "one cubic",
            ("unordered roots {p, q, r}", "the mark is forgotten"),
            GOLD,
            width=4.5,
        ).shift(RIGHT * 3.2 + DOWN * 0.2)
        forget = Arrow(root_circle.get_right(), cubic.get_left(), color=GOLD, buff=0.35)
        with self._voice("mark_roots") as tracker:
            self.play(FadeIn(heading), Create(root_circle), FadeIn(roots), FadeIn(labels), run_time=self._run_time(tracker, 0.28))
            self.play(FadeIn(mark), run_time=self._run_time(tracker, 0.1))
            self.play(mark.animate.move_to(roots[1]), run_time=self._run_time(tracker, 0.12))
            self.play(mark.animate.move_to(roots[2]), run_time=self._run_time(tracker, 0.12))
            self.play(Create(forget), FadeIn(cubic), FadeOut(mark), run_time=self._run_time(tracker, 0.22))
        self._clear()

        self.next_section("06-projective-map")
        heading = self._heading("Jiang's projective formulation", "Posted as GPT output")
        map_text = Text("P¹ × Sym²(P¹)  →  Sym³(P¹)", color=INK, font_size=42)
        point_text = Text("(p, {q,r})  ↦  {p,q,r}", color=GOLD, font_size=38).next_to(map_text, DOWN, buff=0.5)
        explanation = self._card(
            "Plain language",
            ("remember a cubic and one chosen root", "then forget which root was chosen"),
            BLUE,
            width=6.4,
        ).next_to(point_text, DOWN, buff=0.6)
        with self._voice("projective_map") as tracker:
            self.play(FadeIn(heading), run_time=self._run_time(tracker, 0.12))
            self.play(FadeIn(map_text), FadeIn(point_text), run_time=self._run_time(tracker, 0.38))
            self.play(FadeIn(explanation), run_time=self._run_time(tracker, 0.2))
        self._clear()

        self.next_section("07-delete-ramification")
        heading = self._heading("Delete the bad marked choices", "Not every repeated root is removed")
        before = VGroup(
            Dot(LEFT * 2.2, color=BLUE, radius=0.14),
            Dot(RIGHT * 0.2, color=MAGENTA, radius=0.14),
            Dot(RIGHT * 2.2, color=GREEN, radius=0.14),
        ).shift(DOWN * 0.25)
        root_labels = VGroup(
            Text("marked p", color=BLUE, font_size=24).next_to(before[0], UP),
            Text("q", color=MAGENTA, font_size=24).next_to(before[1], UP),
            Text("r", color=GREEN, font_size=24).next_to(before[2], UP),
        )
        deleted = Text("deleted boundary  R", color=RED, font_size=30).to_edge(DOWN, buff=0.8)
        etale = self._card("After deletion", ("differential invertible everywhere", "restricted map is étale"), GREEN, width=5.2).to_edge(DOWN, buff=0.45)
        with self._voice("delete_ramification") as tracker:
            self.play(FadeIn(heading), FadeIn(before), FadeIn(root_labels), run_time=self._run_time(tracker, 0.2))
            self.play(before[0].animate.move_to(before[1]), run_time=self._run_time(tracker, 0.24))
            self.play(FadeOut(before[0], shift=UP), FadeIn(deleted), run_time=self._run_time(tracker, 0.16))
            self.play(FadeOut(deleted), FadeIn(etale), run_time=self._run_time(tracker, 0.18))
        self._clear()

        self.next_section("08-affine-slice")
        heading = self._heading("The affine-space miracle", "A special tangential slice")
        twisted = ParametricFunction(
            lambda value: [2.4 * value, 0.48 * value**3, 0],
            t_range=[-1.25, 1.25, 0.03],
            color=MAGENTA,
        ).shift(UP * 0.2)
        tangent = Line(LEFT * 3.2 + UP * 0.2, RIGHT * 3.2 + UP * 0.2, color=GOLD)
        geometry_label = Text("H: tangent, not osculating", color=GOLD, font_size=25).next_to(tangent, UP, buff=0.25)
        spaces = VGroup(
            self._card("target complement", ("P³ minus H  ≅  A³",), BLUE, width=4.8),
            self._card("source complement", ("marked simple roots  ≅  A³",), GREEN, width=4.8),
        ).arrange(RIGHT, buff=0.45).to_edge(DOWN, buff=0.38)
        with self._voice("affine_slice") as tracker:
            self.play(FadeIn(heading), Create(twisted), run_time=self._run_time(tracker, 0.24))
            self.play(Create(tangent), FadeIn(geometry_label), run_time=self._run_time(tracker, 0.2))
            self.play(
                LaggedStart(*(FadeIn(space, shift=UP * 0.12) for space in spaces), lag_ratio=0.25),
                run_time=self._run_time(tracker, 0.35),
            )
        self._clear()

    def _resultant_route(self) -> None:
        self.next_section("09-factorization")
        heading = self._heading("Lou's factorization route", "A marked root becomes a linear factor")
        ell = self._card("linear factor  ell", ("the marked root",), BLUE, width=3.6)
        times = Text("×", color=GOLD, font_size=48)
        quad = self._card("quadratic factor  q", ("the other two roots",), GREEN, width=3.6)
        equals = Text("=", color=GOLD, font_size=48)
        cubic = self._card("binary cubic  C", ("C = ell · q",), MAGENTA, width=3.6)
        factors = VGroup(ell, times, quad, equals, cubic).arrange(RIGHT, buff=0.25).shift(UP * 0.15)
        scale = Text("(ell, q)  ~  (s ell, s⁻¹ q)", color=INK, font_size=34).shift(DOWN * 2.05)
        with self._voice("factorization") as tracker:
            self.play(FadeIn(heading), run_time=self._run_time(tracker, 0.12))
            self.play(
                LaggedStart(*(FadeIn(item, shift=UP * 0.1) for item in factors), lag_ratio=0.12),
                run_time=self._run_time(tracker, 0.48),
            )
            self.play(FadeIn(scale), run_time=self._run_time(tracker, 0.18))
        self._clear()

        self.next_section("10-resultant-gauge")
        heading = self._heading("The resultant fixes the scale", "One representative on each simple-root orbit")
        orbit = Circle(radius=1.65, color=MUTED, stroke_width=4).shift(LEFT * 2.9 + DOWN * 0.1)
        orbit_label = Text("scaling orbit", color=MUTED, font_size=25).next_to(orbit, DOWN, buff=0.2)
        chosen = Dot(orbit.point_at_angle(0.45), color=GOLD, radius=0.14)
        chosen_label = Text("Res = 1", color=GOLD, font_size=27).next_to(chosen, RIGHT, buff=0.18)
        rules = self._card(
            "Resultant gauge",
            (
                "Res(ell,q) ≠ 0  ⇔  marked root simple",
                "Res(s ell,s⁻¹q) = s Res(ell,q)",
                "set Res(ell,q) = 1",
            ),
            GREEN,
            width=6.1,
            font_size=20,
        ).shift(RIGHT * 3.0 + DOWN * 0.1)
        with self._voice("resultant") as tracker:
            self.play(FadeIn(heading), Create(orbit), FadeIn(orbit_label), run_time=self._run_time(tracker, 0.22))
            self.play(FadeIn(rules), run_time=self._run_time(tracker, 0.32))
            self.play(FadeIn(chosen), FadeIn(chosen_label), run_time=self._run_time(tracker, 0.18))
            self.play(Indicate(chosen, color=GOLD), run_time=self._run_time(tracker, 0.12))
        self._clear()

    def _unification(self) -> None:
        self.next_section("11-unification")
        heading = self._heading("Three languages for one arrow", "Equivalent, but not literally identical formulas")
        cards = VGroup(
            self._card("Alpöge + Fable", ("explicit F", "collision certificate"), BLUE, width=3.7, font_size=19),
            self._card("Jiang + GPT", ("marked-root moduli", "forget the mark"), MAGENTA, width=3.7, font_size=19),
            self._card("Lou", ("Res = 1 factors", "global affine chart"), GREEN, width=3.7, font_size=19),
        ).arrange(RIGHT, buff=0.32).shift(UP * 0.4)
        common = self._card(
            "one morphism",
            ("cubic + normalized simple root  →  cubic",),
            GOLD,
            width=6.6,
        ).shift(DOWN * 1.55)
        arrows = VGroup(
            *[Arrow(card.get_bottom(), common.get_top(), color=card[0].get_stroke_color(), buff=0.12) for card in cards]
        )
        relation = Text("G = R₀ ∘ F ∘ S₀   ·   left-right equivalence", color=INK, font_size=26).to_edge(DOWN, buff=0.32)
        with self._voice("unified") as tracker:
            self.play(FadeIn(heading), run_time=self._run_time(tracker, 0.1))
            self.play(
                LaggedStart(*(FadeIn(card, shift=UP * 0.1) for card in cards), lag_ratio=0.18),
                run_time=self._run_time(tracker, 0.34),
            )
            self.play(*(Create(arrow) for arrow in arrows), FadeIn(common), run_time=self._run_time(tracker, 0.24))
            self.play(FadeIn(relation), run_time=self._run_time(tracker, 0.14))
        self._clear()

    def _curve_visualization(self) -> None:
        self.next_section("12-real-curves")
        self.set_camera_orientation(phi=67 * DEGREES, theta=-48 * DEGREES, zoom=0.72)
        source_axes = ThreeDAxes(
            x_range=[-2.2, 2.2, 1],
            y_range=[-2.2, 2.2, 1],
            z_range=[-2.2, 2.2, 1],
            x_length=4.2,
            y_length=4.2,
            z_length=3.2,
        ).scale(0.7).shift(LEFT * 3.7)
        target_axes = source_axes.copy().shift(RIGHT * 7.4)
        domains = {
            "x_axis": (-1.2, 1.2),
            "y_axis": (-0.7, 0.7),
            "z_axis": (-1.2, 1.2),
        }
        colors = {"x_axis": BLUE, "y_axis": MAGENTA, "z_axis": GREEN}
        source_curves = VGroup(
            *[
                ParametricFunction(
                    lambda value, selected=curve_id: source_axes.c2p(
                        *elementary_source(selected, value)
                    ),
                    t_range=[domain[0], domain[1], 0.03],
                    color=colors[curve_id],
                    stroke_width=6,
                )
                for curve_id, domain in domains.items()
            ]
        )
        target_curves = VGroup(
            *[
                ParametricFunction(
                    lambda value, selected=curve_id: target_axes.c2p(
                        *elementary_target(selected, value)
                    ),
                    t_range=[domain[0], domain[1], 0.03],
                    color=colors[curve_id],
                    stroke_width=6,
                )
                for curve_id, domain in domains.items()
            ]
        )
        source_label = Text("SOURCE  R³", color=INK, font_size=28).shift(LEFT * 3.55 + UP * 3.2)
        target_label = Text("TARGET  R³", color=INK, font_size=28).shift(RIGHT * 3.55 + UP * 3.2)
        caveat = Text(
            "Visualization only: R³ inside the map on C³",
            color=GOLD,
            font_size=23,
        ).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(source_label, target_label, caveat)
        with self._voice("real_curves") as tracker:
            self.play(FadeIn(source_label), FadeIn(target_label), FadeIn(caveat), run_time=self._run_time(tracker, 0.12))
            self.play(Create(source_axes), Create(target_axes), run_time=self._run_time(tracker, 0.2))
            self.play(
                LaggedStart(*(Create(curve) for curve in source_curves), lag_ratio=0.18),
                LaggedStart(*(Create(curve) for curve in target_curves), lag_ratio=0.18),
                run_time=self._run_time(tracker, 0.48),
            )
        self.play(
            FadeOut(source_axes),
            FadeOut(target_axes),
            FadeOut(source_curves),
            FadeOut(target_curves),
            FadeOut(source_label),
            FadeOut(target_label),
            run_time=0.5,
        )
        self.remove_fixed_in_frame_mobjects(source_label, target_label)

        self.next_section("13-escaping-sheets")
        source_sheet_axes = ThreeDAxes(
            x_range=[-16, 16, 8],
            y_range=[-0.6, 0.6, 0.3],
            z_range=[-0.4, 0.4, 0.2],
            x_length=5.0,
            y_length=2.2,
            z_length=2.2,
        ).shift(LEFT * 3.6)
        target_sheet_axes = ThreeDAxes(
            x_range=[-0.2, 0.2, 0.1],
            y_range=[0, 0.5, 0.25],
            z_range=[1.8, 2.2, 0.2],
            x_length=2.4,
            y_length=3.3,
            z_length=2.4,
        ).shift(RIGHT * 3.7)
        branch_curves = VGroup(
            *[
                ParametricFunction(
                    lambda value, selected=branch: source_sheet_axes.c2p(
                        *sheet_point(value, selected)
                    ),
                    t_range=[0.08, 0.30, 0.004],
                    color=BRANCH_COLORS[branch],
                    stroke_width=6,
                )
                for branch in BRANCHES
            ]
        )
        shared_target_curve = ParametricFunction(
            lambda value: target_sheet_axes.c2p(*target_family(value)),
            t_range=[0.08, 0.30, 0.004],
            color=GOLD,
            stroke_width=8,
        )
        parameter = ValueTracker(0.30)
        branch_dots = VGroup(
            *[
                always_redraw(
                    lambda selected=branch: Dot3D(
                        source_sheet_axes.c2p(
                            *sheet_point(parameter.get_value(), selected)
                        ),
                        radius=0.085,
                        color=BRANCH_COLORS[selected],
                    )
                )
                for branch in BRANCHES
            ]
        )
        target_dot = always_redraw(
            lambda: Dot3D(
                target_sheet_axes.c2p(*target_family(parameter.get_value())),
                radius=0.11,
                color=GOLD,
            )
        )
        sheet_title = Text("three marked-root branches", color=INK, font_size=27).shift(LEFT * 3.4 + UP * 3.2)
        target_title = Text("one target curve", color=INK, font_size=27).shift(RIGHT * 3.55 + UP * 3.2)
        polynomial = Text("P_s(T) = 2T(T-s)(T-(1-s))", color=GOLD, font_size=24).to_edge(DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(sheet_title, target_title)
        with self._voice("escaping_sheets") as tracker:
            self.play(
                FadeIn(sheet_title),
                FadeIn(target_title),
                Transform(caveat, polynomial),
                Create(source_sheet_axes),
                Create(target_sheet_axes),
                run_time=self._run_time(tracker, 0.2),
            )
            self.play(
                LaggedStart(*(Create(curve) for curve in branch_curves), lag_ratio=0.18),
                Create(shared_target_curve),
                run_time=self._run_time(tracker, 0.3),
            )
            self.add(branch_dots, target_dot)
            self.play(
                parameter.animate.set_value(0.08),
                run_time=self._run_time(tracker, 0.42),
                rate_func=linear,
            )
        self.play(
            FadeOut(source_sheet_axes),
            FadeOut(target_sheet_axes),
            FadeOut(branch_curves),
            FadeOut(shared_target_curve),
            FadeOut(branch_dots),
            FadeOut(target_dot),
            FadeOut(sheet_title),
            FadeOut(target_title),
            FadeOut(caveat),
            run_time=0.55,
        )
        self.remove_fixed_in_frame_mobjects(sheet_title, target_title, caveat)

    def _proof_and_credits(self) -> None:
        self.next_section("14-proof-and-scope")
        heading = self._heading("The proof spine", "Constant Jacobian, three roots, and infinity")
        cards = VGroup(
            self._card("1 · affine spaces", ("source ≅ A³", "target ≅ A³"), BLUE, width=3.7, font_size=20),
            self._card("2 · remove ramification", ("marked root stays simple", "map becomes étale"), GREEN, width=3.7, font_size=20),
            self._card("3 · count roots", ("three generic markings", "generic degree three"), MAGENTA, width=3.7, font_size=20),
        ).arrange(RIGHT, buff=0.32).shift(UP * 0.35)
        conclusion = Text(
            "local invertibility  +  escape at infinity  =  global noninjectivity",
            color=GOLD,
            font_size=29,
        ).shift(DOWN * 1.55)
        scope = Text(
            "Higher dimensions follow by adjoining identities · dimension two is separate",
            color=MUTED,
            font_size=23,
        ).shift(DOWN * 2.25)
        credits = VGroup(
            Text("Sources and exact links", color=GOLD, font_size=28, weight="BOLD"),
            Text("@__alpoge__ · @davikrehalt · Aaron Lou's derivation", color=INK, font_size=23),
            Text("Paper · code · transcript · checks: this repository", color=INK, font_size=23),
            Text("Original animation and text: CC BY 4.0", color=MUTED, font_size=21),
        ).arrange(DOWN, buff=0.16)
        self.add_fixed_in_frame_mobjects(heading)
        with self._voice("proof_scope") as tracker:
            self.play(FadeIn(heading), run_time=self._run_time(tracker, 0.1))
            self.add_fixed_in_frame_mobjects(cards)
            self.play(
                LaggedStart(*(FadeIn(card, shift=UP * 0.12) for card in cards), lag_ratio=0.2),
                run_time=self._run_time(tracker, 0.34),
            )
            self.add_fixed_in_frame_mobjects(conclusion, scope)
            self.play(FadeIn(conclusion), FadeIn(scope), run_time=self._run_time(tracker, 0.22))
            self.play(
                FadeOut(cards),
                FadeOut(conclusion),
                FadeOut(scope),
                FadeOut(heading),
                run_time=self._run_time(tracker, 0.1),
            )
            self.remove_fixed_in_frame_mobjects(heading, cards, conclusion, scope)
            self.add_fixed_in_frame_mobjects(credits)
            self.play(FadeIn(credits), run_time=self._run_time(tracker, 0.08))
        self.wait(1.0)
