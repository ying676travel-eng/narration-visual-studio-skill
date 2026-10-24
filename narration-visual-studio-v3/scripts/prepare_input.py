#!/usr/bin/env python3
"""Normalize SRT/VTT subtitles into a provenance-preserving V3 JSON document.

Plain text is accepted for planning only: it never receives invented timestamps.
This module intentionally uses only the Python standard library.
"""
from __future__ import annotations

import argparse
import html
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


TIMESTAMP_RE = re.compile(
    r"^(?:(?P<h>\d+):)?(?P<m>\d{2}):(?P<s>\d{2})(?:[,.](?P<f>\d{1,3}))?$"
)
TIMING_LINE_RE = re.compile(
    r"^\s*(?P<start>\S+)\s+-->\s+(?P<end>\S+)(?:\s+.*)?$"
)
TAG_RE = re.compile(r"<[^>]*>")


class InputError(ValueError):
    """Raised when a timed subtitle document has invalid or ambiguous timing."""


def parse_timestamp(value: str) -> float:
    """Parse SRT/VTT timestamp forms: HH:MM:SS,mmm or MM:SS.mmm."""
    match = TIMESTAMP_RE.fullmatch(value.strip())
    if not match:
        raise InputError(f"invalid timestamp: {value!r}")
    hours = int(match.group("h") or 0)
    minutes = int(match.group("m"))
    seconds = int(match.group("s"))
    if minutes > 59 or seconds > 59:
        raise InputError(f"minutes and seconds must be below 60: {value!r}")
    fraction = (match.group("f") or "").ljust(3, "0")
    millis = int(fraction or 0)
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def parse_range_time(value: str) -> float:
    """CLI range times accept subtitle timecodes or plain seconds."""
    raw = value.strip()
    if ":" in raw:
        return parse_timestamp(raw)
    try:
        seconds = float(raw)
    except ValueError as exc:
        raise InputError(f"invalid range time: {value!r}") from exc
    if not math.isfinite(seconds) or seconds < 0:
        raise InputError(f"range times must be finite and non-negative: {value!r}")
    return seconds


def _clean_subtitle_text(lines: Iterable[str]) -> tuple[str, str]:
    original = "\n".join(line.rstrip() for line in lines).strip()
    # VTT formatting tags carry no visual meaning in the normalized transcript.
    # Their text remains intact and entities are decoded exactly once.
    normalized = html.unescape(TAG_RE.sub("", original)).strip()
    return normalized, original


def _split_blocks(text: str) -> list[list[str]]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").lstrip("\ufeff").split("\n")
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines:
        if not line.strip():
            if current:
                blocks.append(current)
                current = []
        else:
            current.append(line)
    if current:
        blocks.append(current)
    return blocks


def _parse_timed_blocks(text: str, source_format: str, source_path: str | None) -> tuple[list[dict[str, Any]], list[str]]:
    cues: list[dict[str, Any]] = []
    warnings: list[str] = []
    blocks = _split_blocks(text)
    vtt_header_seen = False

    for block_no, block in enumerate(blocks, start=1):
        first = block[0].strip()
        if source_format == "vtt" and first.startswith("WEBVTT"):
            vtt_header_seen = True
            continue
        if source_format == "vtt" and first.upper().startswith(("NOTE", "STYLE", "REGION")):
            continue

        timing_indices = [i for i, line in enumerate(block) if "-->" in line]
        if not timing_indices:
            if source_format == "vtt" and not vtt_header_seen:
                warnings.append(f"Block {block_no}: content before WEBVTT header was ignored.")
            elif any(line.strip() for line in block):
                warnings.append(f"Block {block_no}: no cue timing line; block was ignored.")
            continue
        if len(timing_indices) > 1:
            raise InputError(f"block {block_no} contains more than one timing line")

        timing_index = timing_indices[0]
        match = TIMING_LINE_RE.fullmatch(block[timing_index])
        if not match:
            raise InputError(f"block {block_no} has a malformed timing line: {block[timing_index]!r}")
        start_raw, end_raw = match.group("start"), match.group("end")
        try:
            start = parse_timestamp(start_raw)
            end = parse_timestamp(end_raw)
        except InputError as exc:
            raise InputError(f"block {block_no}: {exc}") from exc
        if end <= start:
            raise InputError(f"block {block_no} end must be after start ({start_raw} --> {end_raw})")

        identifier = None
        preceding = [line.strip() for line in block[:timing_index] if line.strip()]
        if preceding:
            identifier = preceding[-1]
        body = block[timing_index + 1 :]
        normalized_text, original_text = _clean_subtitle_text(body)
        cue_id = identifier or str(len(cues) + 1)
        cues.append(
            {
                "id": cue_id,
                "start": start,
                "end": end,
                "original_start": start,
                "original_end": end,
                "text": normalized_text,
                "original_text": original_text,
                "source_path": source_path,
                "source_block": block_no,
                "timecode": {"start": start_raw, "end": end_raw},
            }
        )

    return cues, warnings


def _analyze_cues(cues: list[dict[str, Any]], warnings: list[str]) -> tuple[list[dict[str, float]], list[dict[str, Any]]]:
    seen_exact: dict[tuple[float, float, str], str] = {}
    seen_ids: dict[str, str] = {}
    previous_start: float | None = None
    max_end: float | None = None
    gaps: list[dict[str, float]] = []

    for cue in cues:
        cue_id = str(cue["id"])
        cue_text = str(cue["text"])
        start, end = float(cue["start"]), float(cue["end"])
        if not cue_text:
            warnings.append(f"Cue {cue_id}: subtitle text is blank.")
        if cue_id in seen_ids:
            warnings.append(f"Cue {cue_id}: duplicate cue identifier also used by cue {seen_ids[cue_id]}.")
        else:
            seen_ids[cue_id] = cue_id
        exact_key = (start, end, cue_text.casefold())
        if cue_text and exact_key in seen_exact:
            warnings.append(f"Cue {cue_id}: duplicate text and time range also used by cue {seen_exact[exact_key]}.")
        elif cue_text:
            seen_exact[exact_key] = cue_id

        if previous_start is not None and start < previous_start:
            warnings.append(f"Cue {cue_id}: starts before the preceding cue; source order is not chronological.")
        if max_end is not None:
            if start < max_end:
                warnings.append(f"Cue {cue_id}: overlaps the preceding timed content by {max_end - start:.3f}s.")
            elif start > max_end:
                gaps.append({"start": max_end, "end": start, "duration": start - max_end})
        previous_start = start
        max_end = max(max_end or end, end)

    return gaps, [{"code": "input_warning", "message": item} for item in warnings]


def normalize_input(
    text: str,
    *,
    source_path: str | None = None,
    source_format: str | None = None,
    range_start: float | None = None,
    range_end: float | None = None,
    zero_based: bool = False,
) -> dict[str, Any]:
    """Return V3 input JSON; timed cues keep their original source timecodes."""
    if any(value is not None and (not math.isfinite(value) or value < 0) for value in (range_start, range_end)):
        raise InputError("range boundaries must be finite and non-negative")
    if range_start is not None and range_end is not None and range_end <= range_start:
        raise InputError("range end must be after range start")
    if zero_based and range_start is None:
        raise InputError("--zero-based requires a range start")

    detected = (source_format or "").lower().lstrip(".")
    if detected not in {"srt", "vtt", "txt", "text"}:
        detected = "vtt" if text.lstrip("\ufeff \t\r\n").startswith("WEBVTT") else "srt"
        # A file extension, supplied by the caller, takes precedence over content.
        if source_format:
            detected = source_format.lower().lstrip(".")
    if detected not in {"srt", "vtt", "txt", "text"}:
        raise InputError(f"unsupported input format: {source_format}")

    is_timed = detected in {"srt", "vtt"}
    if is_timed:
        cues, warnings = _parse_timed_blocks(text, detected, source_path)
        if not cues:
            if "-->" in text:
                raise InputError("no valid subtitle cues found")
            # Files with no timestamps are useful for planning, but must say so.
            is_timed = False
            detected = "text"
            warnings.append("No timecodes found; this input supports content planning only, not precise playback.")
    else:
        cues, warnings = [], ["No timecodes found; this input supports content planning only, not precise playback."]

    if not is_timed:
        if range_start is not None or range_end is not None:
            raise InputError("cannot select a timed range from text without timecodes")
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text.replace("\r\n", "\n").replace("\r", "\n")) if part.strip()]
        if not paragraphs:
            raise InputError("input contains no subtitle text")
        cues = [
            {
                "id": str(index),
                "start": None,
                "end": None,
                "original_start": None,
                "original_end": None,
                "text": paragraph,
                "original_text": paragraph,
                "source_path": source_path,
                "source_block": index,
            }
            for index, paragraph in enumerate(paragraphs, start=1)
        ]
        return {
            "source": source_path,
            "source_format": detected,
            "planning_only": True,
            "timecode_status": "missing",
            "duration": None,
            "source_offset": None,
            "range": None,
            "cue_count": len(cues),
            "cues": cues,
            "gaps": [],
            "warnings": warnings,
        }

    if range_start is not None or range_end is not None:
        effective_start = range_start if range_start is not None else min(float(c["start"]) for c in cues)
        effective_end = range_end if range_end is not None else max(float(c["end"]) for c in cues)
        if effective_end <= effective_start:
            raise InputError("range end must be after range start")
        selected: list[dict[str, Any]] = []
        for cue in cues:
            original_start, original_end = float(cue["start"]), float(cue["end"])
            clipped_start, clipped_end = max(original_start, effective_start), min(original_end, effective_end)
            if clipped_end <= clipped_start:
                continue
            updated = dict(cue)
            updated["start"] = clipped_start
            updated["end"] = clipped_end
            selected.append(updated)
        if not selected:
            raise InputError("the requested range does not overlap any subtitle cue")
        cues = selected
        range_info = {"start": effective_start, "end": effective_end, "duration": effective_end - effective_start}
        warnings.append(f"Range selected: {effective_start:.3f}s to {effective_end:.3f}s; cues outside it were excluded and boundary cues clipped.")
    else:
        effective_start = min(float(c["start"]) for c in cues)
        effective_end = max(float(c["end"]) for c in cues)
        range_info = None

    offset = effective_start if zero_based else 0.0
    for cue in cues:
        cue["start"] = round(float(cue["start"]) - offset, 3)
        cue["end"] = round(float(cue["end"]) - offset, 3)
        cue["original_start"] = round(float(cue["original_start"]), 3)
        cue["original_end"] = round(float(cue["original_end"]), 3)

    gaps, structured_warnings = _analyze_cues(cues, warnings)
    duration = round(effective_end - offset, 3)
    return {
        "source": source_path,
        "source_format": detected,
        "planning_only": False,
        "timecode_status": "present",
        "duration": duration,
        "source_offset": round(offset, 3),
        "range": range_info,
        "cue_count": len(cues),
        "cues": cues,
        "gaps": gaps,
        "warnings": structured_warnings,
    }


def prepare_file(path: str | Path, **options: Any) -> dict[str, Any]:
    source = Path(path)
    try:
        content = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise InputError(f"input is not valid UTF-8: {source}") from exc
    except OSError as exc:
        raise InputError(f"cannot read input {source}: {exc}") from exc
    suffix = source.suffix.lower().lstrip(".")
    if suffix in {"srt", "vtt", "txt"}:
        options.setdefault("source_format", suffix)
    options.setdefault("source_path", str(source.resolve()))
    return normalize_input(content, **options)


def prepare_input(source: str | Path, start: float | str | None = None, end: float | str | None = None) -> dict[str, Any]:
    """Parent-pipeline API: read a file and optionally clip a range to zero."""
    options: dict[str, Any] = {}
    if start is not None:
        options["range_start"] = parse_range_time(str(start))
    if end is not None:
        options["range_end"] = parse_range_time(str(end))
    if start is not None or end is not None:
        options["zero_based"] = True
    return prepare_file(source, **options)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="subtitle or plain-text file")
    parser.add_argument("--out", "--output", dest="output", help="write JSON to this file (default: stdout)")
    parser.add_argument("--range", nargs=2, metavar=("START", "END"), help="keep the intersecting range; times may be seconds or HH:MM:SS.mmm")
    parser.add_argument("--zero-based", action="store_true", help="subtract the selected range start from cue times")
    args = parser.parse_args(argv)
    try:
        options: dict[str, Any] = {"zero_based": args.zero_based}
        if args.range:
            options["range_start"] = parse_range_time(args.range[0])
            options["range_end"] = parse_range_time(args.range[1])
        payload = prepare_file(args.input, **options)
        serialized = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            Path(args.output).write_text(serialized, encoding="utf-8")
        else:
            sys.stdout.write(serialized)
    except (InputError, OSError) as exc:
        print(f"prepare_input: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
