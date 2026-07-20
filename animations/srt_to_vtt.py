"""Validate Manim's external SRT captions and convert them to WebVTT."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import re


TIMESTAMP_RE = re.compile(
    r"^(?P<start>\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+"
    r"(?P<end>\d{2}:\d{2}:\d{2},\d{3})$"
)


@dataclass(frozen=True)
class Cue:
    identifier: str
    start: str
    end: str
    text: tuple[str, ...]


def _milliseconds(timestamp: str) -> int:
    hours, minutes, remainder = timestamp.split(":")
    seconds, millis = remainder.split(",")
    return (
        int(hours) * 3_600_000
        + int(minutes) * 60_000
        + int(seconds) * 1_000
        + int(millis)
    )


def parse_srt(content: str) -> tuple[Cue, ...]:
    """Parse the strict subset of SRT emitted by Manim."""

    normalized = content.lstrip("\ufeff").replace("\r\n", "\n").strip()
    if not normalized:
        raise ValueError("caption file is empty")
    cues: list[Cue] = []
    previous_end = -1
    for block in re.split(r"\n\s*\n", normalized):
        lines = block.splitlines()
        if len(lines) < 3:
            raise ValueError(f"invalid SRT cue: {block!r}")
        identifier = lines[0].strip()
        match = TIMESTAMP_RE.fullmatch(lines[1].strip())
        if match is None:
            raise ValueError(f"invalid SRT timestamp: {lines[1]!r}")
        start = match.group("start")
        end = match.group("end")
        start_ms = _milliseconds(start)
        end_ms = _milliseconds(end)
        if start_ms < previous_end:
            raise ValueError("caption cues overlap or are out of order")
        if end_ms <= start_ms:
            raise ValueError("caption cue has nonpositive duration")
        text = tuple(line.rstrip() for line in lines[2:] if line.strip())
        if not text:
            raise ValueError("caption cue has no text")
        cues.append(Cue(identifier, start, end, text))
        previous_end = end_ms
    return tuple(cues)


def convert_srt_text(content: str) -> str:
    """Convert validated SRT text into a browser-compatible WebVTT document."""

    lines = ["WEBVTT", ""]
    for cue in parse_srt(content):
        if cue.identifier:
            lines.append(cue.identifier)
        lines.append(f"{cue.start.replace(',', '.')} --> {cue.end.replace(',', '.')}")
        lines.extend(cue.text)
        lines.append("")
    return "\n".join(lines)


def convert_file(source: str | Path, destination: str | Path) -> Path:
    """Convert one UTF-8 SRT file to UTF-8 WebVTT."""

    source_path = Path(source)
    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    destination_path.write_text(
        convert_srt_text(source_path.read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    return destination_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    options = parser.parse_args()
    convert_file(options.source, options.destination)
