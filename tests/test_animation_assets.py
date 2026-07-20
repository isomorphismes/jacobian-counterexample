"""Manim-free certificates for the narrated and browser visualization assets."""

from fractions import Fraction
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from animations.math_core import (
    BRANCHES,
    curve_payload,
    elementary_source,
    elementary_target,
    exact_demo_parameters,
    export_curve_data,
    jacobian_map,
    sheet_point,
    target_family,
)
from animations.srt_to_vtt import convert_srt_text, parse_srt
from animations.story_data import (
    CREDITS,
    SEGMENTS,
    STORY_LICENSE,
    TARGET_DURATION_SECONDS,
    estimated_duration_seconds,
    export_story_json,
    render_transcript_markdown,
    spoken_word_count,
)


class _VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

def test_three_point_fiber_exactly_matches_the_announced_map():
    points = (
        (Fraction(0), Fraction(0), Fraction(-1, 4)),
        (Fraction(1), Fraction(-3, 2), Fraction(13, 2)),
        (Fraction(-1), Fraction(3, 2), Fraction(13, 2)),
    )
    expected = (Fraction(-1, 4), Fraction(0), Fraction(0))
    assert len(set(points)) == 3
    assert all(jacobian_map(point) == expected for point in points)


@pytest.mark.parametrize("curve_id", ("x_axis", "y_axis", "z_axis"))
@pytest.mark.parametrize(
    "parameter",
    (Fraction(-3, 5), Fraction(0), Fraction(7, 10)),
)
def test_elementary_curve_images_are_exact(curve_id, parameter):
    source = elementary_source(curve_id, parameter)
    assert jacobian_map(source) == elementary_target(curve_id, parameter)


@pytest.mark.parametrize("parameter", exact_demo_parameters())
@pytest.mark.parametrize("branch", BRANCHES)
def test_each_marked_root_sheet_maps_to_the_same_target(parameter, branch):
    source = sheet_point(parameter, branch)
    assert jacobian_map(source) == target_family(parameter)


def test_two_colliding_branches_escape_while_the_third_stays_bounded():
    near = Fraction(1, 100)
    farther = Fraction(1, 10)
    for branch in ("zero", "moving"):
        assert abs(sheet_point(near, branch)[0]) > abs(sheet_point(farther, branch)[0])
    assert abs(sheet_point(near, "remaining")[0]) < 2


def test_repeated_marked_root_is_the_only_sheet_singularity():
    with pytest.raises(ZeroDivisionError):
        sheet_point(Fraction(0), "zero")
    with pytest.raises(ZeroDivisionError):
        sheet_point(Fraction(1, 2), "moving")


def test_shared_fixture_is_the_deterministic_export():
    fixture = json.loads((ROOT / "shared" / "curve-fixtures.json").read_text())
    assert fixture == curve_payload(samples=61)
    assert "six real dimensions" in fixture["space_note"]
    assert "real slice" in fixture["space_note"]
    assert set(fixture["sheet_family"]["branches"]) == set(BRANCHES)


def test_curve_export_round_trip(tmp_path):
    output = export_curve_data(tmp_path / "curves.json", samples=7)
    payload = json.loads(output.read_text())
    assert payload == curve_payload(samples=7)
    assert all(
        len(curve["source"]) == len(curve["target"]) == 7
        for curve in payload["elementary_curves"]
    )


def test_story_metadata_has_unique_complete_segments_and_precise_credit_links():
    ids = [segment.id for segment in SEGMENTS]
    assert len(ids) == len(set(ids)) == 14
    assert all(spoken_word_count(segment.narration) >= 25 for segment in SEGMENTS)
    assert STORY_LICENSE == "CC-BY-4.0"
    credit_by_name = {credit.name: credit for credit in CREDITS}
    assert credit_by_name["Levent Alpöge"].url == (
        "https://x.com/__alpoge__/status/2079028340955197566"
    )
    assert credit_by_name["Andy Jiang (@davikrehalt)"].url == (
        "https://x.com/davikrehalt/status/2079175065695035442"
    )
    assert "Fable" in credit_by_name["Levent Alpöge"].role
    assert "GPT output" in credit_by_name["Andy Jiang (@davikrehalt)"].role
    assert "no claim" in credit_by_name["Repository contributors"].role


def test_planned_narration_is_short_and_close_to_target_duration():
    estimate = estimated_duration_seconds()
    assert 320 <= estimate <= 370
    assert abs(estimate - TARGET_DURATION_SECONDS) <= 10


def test_committed_transcript_is_generated_from_canonical_story_data():
    committed = (ROOT / "animations" / "transcript.md").read_text(encoding="utf-8")
    assert committed == render_transcript_markdown()


def test_landing_page_contains_every_canonical_narration_segment_as_html():
    source = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
    parser = _VisibleText()
    parser.feed(source)
    visible_text = re.sub(r"\s+", " ", " ".join(parser.parts)).strip()

    for segment in SEGMENTS:
        assert source.count(f'data-segment-id="{segment.id}"') == 1
        assert re.sub(r"\s+", " ", segment.narration).strip() in visible_text

    assert "Read the exact narration transcript" in visible_text
    assert "marked-root-explainer-transcript.md" in source


def _webvtt_timestamp_seconds(value: str) -> float:
    hours, minutes, seconds = value.split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def test_embedded_webvtt_is_complete_ordered_and_exactly_canonical():
    source = (
        ROOT / "site" / "public" / "media" / "marked-root-explainer.en.vtt"
    ).read_text(encoding="utf-8")
    assert source.startswith("WEBVTT\n\n")

    cues: list[tuple[int, float, float, str]] = []
    for block in re.split(r"\n\s*\n", source.strip())[1:]:
        lines = block.splitlines()
        if len(lines) < 3 or " --> " not in lines[1]:
            continue
        cue_id = int(lines[0])
        start_text, end_text = lines[1].split(" --> ")
        cues.append(
            (
                cue_id,
                _webvtt_timestamp_seconds(start_text),
                _webvtt_timestamp_seconds(end_text),
                " ".join(lines[2:]),
            )
        )

    assert len(cues) == 104
    assert [cue[0] for cue in cues] == list(range(1, 105))
    assert cues[0][1] == 0
    assert all(start < end for _, start, end, _ in cues)
    assert all(previous[2] <= current[1] for previous, current in zip(cues, cues[1:]))
    assert cues[-1][2] < 275.733

    caption_text = " ".join(cue[3] for cue in cues)
    canonical_text = " ".join(segment.narration for segment in SEGMENTS)
    assert caption_text == canonical_text


def test_embedded_release_media_matches_its_public_manifest():
    media = ROOT / "site" / "public" / "media"
    movie = media / "marked-root-explainer.mp4"
    captions = media / "marked-root-explainer.en.vtt"
    manifest = (media / "README.md").read_text(encoding="utf-8")

    assert movie.stat().st_size > 10_000_000
    movie_bytes = movie.read_bytes()
    assert b"ftyp" in movie_bytes[:32]
    assert movie_bytes.index(b"moov") < movie_bytes.index(b"mdat")
    assert hashlib.sha256(movie_bytes).hexdigest() in manifest
    assert hashlib.sha256(captions.read_bytes()).hexdigest() in manifest
    assert "1920 x 1080" in manifest
    assert "H.264/AAC" in manifest
    assert "synthetic" in manifest
    assert "not presented as a recording by any credited mathematician" in manifest


def test_story_json_export_round_trip(tmp_path):
    output = export_story_json(tmp_path / "story.json")
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["target_duration_seconds"] == TARGET_DURATION_SECONDS
    assert len(payload["segments"]) == len(SEGMENTS)
    assert payload["segments"][0]["id"] == "credits"


def test_srt_conversion_validates_timing_and_emits_webvtt():
    source = (
        "1\n00:00:00,000 --> 00:00:02,400\nOne map, three descriptions.\n\n"
        "2\n00:00:02,500 --> 00:00:05,000\nMark one root, then forget it.\n"
    )
    cues = parse_srt(source)
    assert len(cues) == 2
    converted = convert_srt_text(source)
    assert converted.startswith("WEBVTT\n\n1\n00:00:00.000")
    assert "00:00:02.500 --> 00:00:05.000" in converted


def test_srt_conversion_rejects_overlaps():
    source = (
        "1\n00:00:00,000 --> 00:00:03,000\nFirst.\n\n"
        "2\n00:00:02,900 --> 00:00:04,000\nSecond.\n"
    )
    with pytest.raises(ValueError, match="overlap"):
        parse_srt(source)


def test_scene_references_every_segment_and_avoids_latex_runtime():
    source = (ROOT / "animations" / "jacobian_story.py").read_text(encoding="utf-8")
    assert "class JacobianStory(ThreeDScene, VoiceoverScene)" in source
    assert "RecorderService(transcription_model=None)" in source
    assert "DeterministicSilenceService" in source
    assert 'mode == "piper"' in source
    assert "PiperSpeechService" in source
    assert "MathTex(" not in source
    assert " Tex(" not in source
    for segment in SEGMENTS:
        assert f'_voice("{segment.id}")' in source


def test_animation_environment_pins_verified_versions():
    environment = (ROOT / "environment-animation.yml").read_text(encoding="utf-8")
    assert "manim=0.20.1" in environment
    assert '"manim-voiceover[recorder]==0.4.0"' in environment
    assert '"piper-tts==1.4.2"' in environment
    assert "python=3.12" in environment
    assert "pip>=26.1.2" in environment
    assert "portaudio>=19,<20" in environment
    assert "sox>=14.4,<15" in environment
