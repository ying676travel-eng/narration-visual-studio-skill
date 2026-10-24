#!/usr/bin/env python3
"""Statically inspect a local HTML/CSS reference and create a safe style draft.

The source is parsed as data only. No JavaScript runs, network requests are made,
or source assets are copied into the generated style directory.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


class ImportErrorSafe(ValueError):
    """Raised for unsafe or invalid inputs and destination paths."""


@dataclass
class Declaration:
    name: str
    value: str
    important: bool
    order: int
    origin: str


@dataclass
class Rule:
    selectors: list[str]
    declarations: list[Declaration]
    order: int
    origin: str
    media: tuple[str, ...] = ()


@dataclass
class ElementInfo:
    tag: str
    attrs: dict[str, str]
    inline: list[Declaration]
    order: int


class ReferenceHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.css_sources: list[tuple[str, str]] = []
        self.elements: list[ElementInfo] = []
        self.assets: list[dict[str, Any]] = []
        self.script_tags = 0
        self.inline_scripts = 0
        self.event_handlers = 0
        self._style_chunks: list[str] | None = None
        self._script_has_src = False
        self._order = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._order += 1
        normalized = {str(key).lower(): (value or "") for key, value in attrs}
        inline = parse_declarations(normalized.get("style", ""), f"inline style on <{tag}>", 10**9 + self._order)
        self.elements.append(ElementInfo(tag.lower(), normalized, inline, self._order))
        self.event_handlers += sum(1 for name in normalized if name.startswith("on"))
        if tag.lower() == "style":
            self._style_chunks = []
        elif tag.lower() == "script":
            self.script_tags += 1
            self._script_has_src = bool(normalized.get("src"))
            if self._script_has_src:
                self.assets.append({"raw": normalized["src"], "kind": "script", "origin": "html"})
        if tag.lower() == "link":
            href = normalized.get("href", "")
            rel = set(normalized.get("rel", "").lower().split())
            if href and "stylesheet" in rel:
                self.css_sources.append(("link", href))
            elif href:
                self.assets.append({"raw": href, "kind": "link", "origin": "html"})
        for attr in ("src", "poster", "data", "srcset"):
            raw = normalized.get(attr, "")
            if raw and not (tag.lower() == "script" and attr == "src"):
                values = [item.strip().split()[0] for item in raw.split(",")] if attr == "srcset" else [raw.strip()]
                for value in values:
                    if value:
                        self.assets.append({"raw": value, "kind": attr, "origin": "html"})

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "style" and self._style_chunks is not None:
            self.css_sources.append(("inline", "\n".join(self._style_chunks)))
            self._style_chunks = None
        elif tag == "script":
            if not self._script_has_src:
                self.inline_scripts += 1
            self._script_has_src = False

    def handle_data(self, data: str) -> None:
        if self._style_chunks is not None:
            self._style_chunks.append(data)


def _strip_css_comments(text: str) -> str:
    result: list[str] = []
    i = 0
    quote: str | None = None
    while i < len(text):
        ch = text[i]
        if quote:
            result.append(ch)
            if ch == "\\" and i + 1 < len(text):
                i += 1
                result.append(text[i])
            elif ch == quote:
                quote = None
            i += 1
        elif ch in "\"'":
            quote = ch
            result.append(ch)
            i += 1
        elif text.startswith("/*", i):
            end = text.find("*/", i + 2)
            i = len(text) if end < 0 else end + 2
        else:
            result.append(ch)
            i += 1
    return "".join(result)


def _split_top_level(text: str, delimiter: str) -> list[str]:
    parts: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "(":
            depth += 1
        elif ch == ")":
            depth = max(0, depth - 1)
        elif ch == delimiter and depth == 0:
            parts.append(text[start:i].strip())
            start = i + 1
        i += 1
    parts.append(text[start:].strip())
    return [part for part in parts if part]


def _block_end(text: str, open_brace: int) -> int:
    depth = 1
    quote: str | None = None
    i = open_brace + 1
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\":
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return len(text)


def parse_declarations(body: str, origin: str, base_order: int = 0) -> list[Declaration]:
    declarations: list[Declaration] = []
    for index, item in enumerate(_split_top_level(body, ";")):
        colon_parts = _split_top_level(item, ":")
        if len(colon_parts) < 2:
            continue
        name = colon_parts[0].strip()
        if not name.startswith("--"):
            name = name.lower()
        value = item[item.find(":") + 1 :].strip()
        important = bool(re.search(r"!\s*important\s*$", value, re.I))
        if important:
            value = re.sub(r"!\s*important\s*$", "", value, flags=re.I).strip()
        if name:
            declarations.append(Declaration(name, value, important, base_order + index, origin))
    return declarations


def _parse_css_rules(css: str, origin: str, rules: list[Rule], media: tuple[str, ...] = ()) -> None:
    text = _strip_css_comments(css)
    cursor = 0
    while cursor < len(text):
        while cursor < len(text) and text[cursor].isspace():
            cursor += 1
        if cursor >= len(text):
            return
        quote: str | None = None
        parens = 0
        boundary = cursor
        while boundary < len(text):
            ch = text[boundary]
            if quote:
                if ch == "\\":
                    boundary += 2
                    continue
                if ch == quote:
                    quote = None
            elif ch in "\"'":
                quote = ch
            elif ch == "(":
                parens += 1
            elif ch == ")":
                parens = max(0, parens - 1)
            elif parens == 0 and ch in "{;}":
                break
            boundary += 1
        if boundary >= len(text):
            return
        head = text[cursor:boundary].strip()
        marker = text[boundary]
        if marker in ";}":
            cursor = boundary + 1
            continue
        end = _block_end(text, boundary)
        body = text[boundary + 1 : end]
        if head.lower().startswith(("@media", "@supports", "@container", "@layer")):
            _parse_css_rules(body, origin, rules, media + (head,))
        elif not head.startswith("@"):
            declarations = parse_declarations(body, origin, len(rules) * 1000)
            if declarations:
                rules.append(Rule(_split_top_level(head, ","), declarations, len(rules) + 1, origin, media))
        cursor = min(len(text), end + 1)


def _specificity(selector: str) -> tuple[int, int, int]:
    selector = re.sub(r"::[\w-]+", " ", selector)
    ids = len(re.findall(r"#[\w-]+", selector))
    classes = len(re.findall(r"\.[\w-]+|\[[^\]]+\]|:(?!:)[\w-]+", selector))
    remainder = re.sub(r"#[\w-]+|\.[\w-]+|:[\w-]+|\[[^\]]+\]", " ", selector)
    tags = len(re.findall(r"(?<![\w-])[A-Za-z][\w-]*", remainder))
    return ids, classes, tags


def _root_selector_matches(selector: str, element: ElementInfo) -> bool:
    selector = selector.strip()
    if not selector or any(token in selector for token in ("+", "~", ">")):
        return False
    parts = selector.split()
    target = parts[-1]
    tag_match = re.match(r"^([a-zA-Z][\w-]*|\*)", target)
    if tag_match and tag_match.group(1).lower() not in {"*", element.tag}:
        return False
    if ":root" in target and element.tag != "html":
        return False
    ids = re.findall(r"#([\w-]+)", target)
    classes = re.findall(r"\.([\w-]+)", target)
    if ids and element.attrs.get("id") not in ids:
        return False
    element_classes = set(element.attrs.get("class", "").split())
    if any(value not in element_classes for value in classes):
        return False
    pseudos = [p for p in re.findall(r":([\w-]+)", target) if p != "root"]
    if pseudos:
        return False
    if len(parts) > 1 and not all(part in {":root", "html", "*"} for part in parts[:-1]):
        return False
    return True


def _element_styles(element: ElementInfo, rules: list[Rule]) -> dict[str, str]:
    winners: dict[str, tuple[tuple[int, ...], Declaration]] = {}
    for rule in rules:
        if rule.media:
            continue
        for selector in rule.selectors:
            if not _root_selector_matches(selector, element):
                continue
            specificity = _specificity(selector)
            for declaration in rule.declarations:
                priority = (int(declaration.important), 0, *specificity, declaration.order + rule.order * 100000)
                current = winners.get(declaration.name)
                if current is None or priority >= current[0]:
                    winners[declaration.name] = (priority, declaration)
    for declaration in element.inline:
        priority = (int(declaration.important), 1, 0, 0, 0, declaration.order)
        current = winners.get(declaration.name)
        if current is None or priority >= current[0]:
            winners[declaration.name] = (priority, declaration)
    return {name: declaration.value for name, (_, declaration) in winners.items()}


def _resolve_vars(value: str, variables: dict[str, str], seen: set[str] | None = None) -> str:
    seen = set(seen or ())
    pattern = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,\s*([^()]*(?:\([^()]*\)[^()]*)*))?\)")
    result = value
    for _ in range(20):
        match = pattern.search(result)
        if not match:
            break
        key, fallback = match.group(1), match.group(2)
        if key in seen:
            replacement = fallback or ""
        elif key in variables:
            replacement = _resolve_vars(variables[key], variables, seen | {key})
        else:
            replacement = fallback or ""
        result = result[: match.start()] + replacement + result[match.end() :]
    return result.strip()


def _effective_styles(element: ElementInfo, rules: list[Rule], inherited: dict[str, str] | None = None) -> dict[str, str]:
    styles = dict(inherited or {})
    styles.update(_element_styles(element, rules))
    variables = {key: value for key, value in styles.items() if key.startswith("--")}
    for key, value in list(styles.items()):
        if not key.startswith("--"):
            styles[key] = _resolve_vars(value, variables)
    return styles


TOKEN_ALIASES: dict[str, tuple[str, ...]] = {
    "bg": ("--bg", "--background", "--surface", "--color-bg", "--primary"),
    "ink": ("--ink", "--foreground", "--text", "--color-text", "--secondary"),
    "accent": ("--accent", "--highlight", "--color-accent", "--tertiary"),
    "muted": ("--muted", "--gray", "--text-muted", "--secondary-text"),
    "line": ("--line", "--border", "--rule"),
    "display_font": ("--f-disp", "--display-font", "--font-display", "--serif"),
    "body_font": ("--f-body", "--body-font", "--font-body", "--sans"),
    "mono_font": ("--f-mono", "--mono-font", "--font-mono", "--mono"),
}
DEFAULT_TOKENS = {
    "bg": "#f5f1e9", "ink": "#252321", "accent": "#b96a42", "muted": "#746f68", "line": "#c9c1b6",
    "display_font": "Georgia, serif", "body_font": "Arial, sans-serif", "mono_font": "ui-monospace, SFMono-Regular, Menlo, monospace",
}


def _safe_color(raw: str, fallback: str) -> tuple[str, bool]:
    value = raw.strip().strip("\"'")
    safe = (re.fullmatch(r"#[0-9a-fA-F]{3,8}", value)
            or re.fullmatch(r"(?:rgb|rgba|hsl|hsla)\([\d.%\s,/+-]+\)", value, re.I)
            or re.fullmatch(r"[a-zA-Z]{1,24}", value))
    return (value, False) if safe else (fallback, bool(raw))


def _safe_font(raw: str, fallback: str) -> tuple[str, bool]:
    value = raw.strip()
    if len(value) <= 160 and re.fullmatch(r"[\w\s,'\"-]+", value, re.UNICODE) and not re.search(r"url|var\s*\(|expression|[;{}<>\\]", value, re.I):
        return value, False
    return fallback, bool(raw)


def _redacted_url(value: str) -> str:
    parts = urlsplit(value)
    if parts.scheme in {"http", "https"}:
        host = parts.hostname or "remote"
        port = f":{parts.port}" if parts.port else ""
        return f"{parts.scheme}://{host}{port}{parts.path}"
    return parts.path or value.split("?", 1)[0].split("#", 1)[0]


def _safe_local_file(root: Path, source_file: Path, raw: str) -> tuple[Path | None, str]:
    value = html.unescape(raw.strip().strip("\"'"))
    parts = urlsplit(value)
    if parts.scheme or parts.netloc or value.startswith("//"):
        return None, "remote"
    if value.startswith("data:") or value.startswith("#") or not value:
        return None, "inline_or_fragment"
    candidate = Path(parts.path) if parts.path.startswith("/") else source_file.parent / parts.path
    try:
        resolved = candidate.resolve(strict=False)
        resolved.relative_to(root.resolve())
    except (OSError, ValueError):
        return None, "outside_source_directory"
    return resolved, "local"


def _read_reference(source: Path) -> tuple[str, ReferenceHTMLParser]:
    if not source.exists() or not source.is_file():
        raise ImportErrorSafe(f"reference file not found: {source}")
    try:
        text = source.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ImportErrorSafe("reference must be UTF-8 HTML") from exc
    parser = ReferenceHTMLParser()
    parser.feed(text)
    parser.close()
    return text, parser


def inspect_reference(source: str | Path) -> dict[str, Any]:
    source_file = Path(source).resolve()
    _, parsed = _read_reference(source_file)
    root = source_file.parent.resolve()
    rules: list[Rule] = []
    assets: list[dict[str, Any]] = []
    remote_refs: list[dict[str, str]] = []
    missing_assets: list[str] = []
    blocked_assets: list[str] = []
    css_sources: list[str] = []
    css_imports: list[str] = []

    for source_kind, value in parsed.css_sources:
        if source_kind == "inline":
            css_sources.append("<style> in HTML")
            _parse_css_rules(value, "<style> in HTML", rules)
            for url in re.findall(r"url\(\s*(['\"]?)(.*?)\1\s*\)", value, re.I):
                assets.append({"raw": url[1], "kind": "css-url", "origin": "<style> in HTML"})
            for imported in re.findall(r"@import\s+(?:url\()?\s*['\"]?([^\s'\")]+)", value, re.I):
                css_imports.append(_redacted_url(imported))
            continue
        linked_path, classification = _safe_local_file(root, source_file, value)
        if classification == "remote":
            redacted = _redacted_url(value)
            remote_refs.append({"url": redacted, "kind": "stylesheet"})
            assets.append({"path": redacted, "kind": "stylesheet", "status": "remote_skipped", "origin": "html"})
            continue
        if classification != "local" or linked_path is None:
            blocked_assets.append(value)
            continue
        if not linked_path.is_file():
            relative_missing = str(linked_path.relative_to(root))
            missing_assets.append(relative_missing)
            assets.append({"path": relative_missing, "kind": "stylesheet", "status": "missing", "origin": "html"})
            continue
        try:
            css_text = linked_path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeDecodeError):
            missing_assets.append(str(linked_path.relative_to(root)))
            continue
        relative = str(linked_path.relative_to(root))
        css_sources.append(relative)
        assets.append({"path": relative, "kind": "stylesheet", "status": "read_only_local", "origin": "html"})
        _parse_css_rules(css_text, relative, rules)
        for url in re.findall(r"url\(\s*(['\"]?)(.*?)\1\s*\)", css_text, re.I):
            assets.append({"raw": url[1], "kind": "css-url", "origin": relative})
        for imported in re.findall(r"@import\s+(?:url\()?\s*['\"]?([^\s'\")]+)", css_text, re.I):
            css_imports.append(_redacted_url(imported))

    root_element = next((element for element in parsed.elements if element.tag == "html"), ElementInfo("html", {}, [], 0))
    body_element = next((element for element in parsed.elements if element.tag == "body"), ElementInfo("body", {}, [], 0))
    root_styles = _effective_styles(root_element, rules)
    body_styles = _effective_styles(body_element, rules, root_styles)
    variables = {key: value for key, value in body_styles.items() if key.startswith("--")}

    conflicts: dict[str, list[dict[str, str]]] = {}
    seen_values: dict[str, list[str]] = {}
    for rule in rules:
        for declaration in rule.declarations:
            if declaration.name.startswith("--"):
                raw = _resolve_vars(declaration.value, variables)
                previous = seen_values.setdefault(declaration.name, [])
                if raw not in previous:
                    previous.append(raw)
                if len(previous) > 1:
                    conflicts[declaration.name] = [{"value": item} for item in previous]

    raw_tokens: dict[str, str] = {}
    token_sources: dict[str, str] = {}
    for token, aliases in TOKEN_ALIASES.items():
        chosen = next((name for name in aliases if name in variables), None)
        if chosen:
            raw_tokens[token] = _resolve_vars(variables[chosen], variables)
            token_sources[token] = chosen
            continue
        if token in {"bg", "ink", "accent", "muted", "line"}:
            fallback_property = {"bg": "background-color", "ink": "color", "accent": "border-color", "muted": "color", "line": "border-color"}[token]
            fallback_styles = body_styles
            if fallback_styles.get(fallback_property):
                raw_tokens[token] = fallback_styles[fallback_property]
                token_sources[token] = f"static effective {fallback_property}"
        elif token == "body_font" and body_styles.get("font-family"):
            raw_tokens[token] = body_styles["font-family"]
            token_sources[token] = "static effective body font-family"
        elif token in {"display_font", "mono_font"}:
            selector_hint = re.compile(r"(?:h[1-6]|title|display)" if token == "display_font" else r"(?:code|pre|kbd|mono)", re.I)
            chosen_font = next((declaration.value for rule in rules if any(selector_hint.search(sel) for sel in rule.selectors)
                                for declaration in rule.declarations if declaration.name == "font-family"), None)
            if chosen_font:
                raw_tokens[token] = _resolve_vars(chosen_font, variables)
                token_sources[token] = "matching heading/code font-family rule"

    tokens: dict[str, str] = {}
    unsafe_values: list[str] = []
    for key in ("bg", "ink", "accent", "muted", "line"):
        value, unsafe = _safe_color(raw_tokens.get(key, ""), DEFAULT_TOKENS[key])
        tokens[key] = value
        if unsafe:
            unsafe_values.append(key)
        if key not in raw_tokens:
            token_sources[key] = "safe fallback; no unambiguous source token"
    for key in ("display_font", "body_font", "mono_font"):
        value, unsafe = _safe_font(raw_tokens.get(key, ""), DEFAULT_TOKENS[key])
        tokens[key] = value
        if unsafe:
            unsafe_values.append(key)
        if key not in raw_tokens:
            token_sources[key] = "safe fallback; no unambiguous source token"

    font_families: list[str] = []
    for rule in rules:
        for declaration in rule.declarations:
            if declaration.name == "font-family":
                family = _resolve_vars(declaration.value, variables)
                if family and family not in font_families:
                    font_families.append(family)

    for asset in parsed.assets + [item for item in assets if "raw" in item]:
        raw = asset["raw"]
        origin_file = source_file
        origin = str(asset.get("origin", ""))
        if origin and not origin.startswith("<") and origin != "html":
            candidate_origin = (root / origin).resolve()
            try:
                candidate_origin.relative_to(root)
                origin_file = candidate_origin
            except ValueError:
                pass
        local_path, classification = _safe_local_file(root, origin_file, raw)
        if classification == "remote":
            redacted = _redacted_url(raw)
            remote_refs.append({"url": redacted, "kind": asset["kind"]})
            assets.append({"path": redacted, "kind": asset["kind"], "status": "remote_skipped", "origin": asset["origin"]})
        elif classification == "inline_or_fragment":
            continue
        elif classification != "local" or local_path is None:
            blocked_assets.append(raw)
            assets.append({"path": raw.split("?", 1)[0], "kind": asset["kind"], "status": "blocked_outside_source_directory", "origin": asset["origin"]})
        else:
            relative = str(local_path.relative_to(root))
            exists = local_path.is_file()
            if not exists:
                missing_assets.append(relative)
            assets.append({"path": relative, "kind": asset["kind"], "status": "available_locally" if exists else "missing", "origin": asset["origin"]})

    media_queries = sorted({context for rule in rules for context in rule.media})
    script_risk = parsed.script_tags > 0 or parsed.event_handlers > 0
    uncertainties = [
        "Static analysis does not execute JavaScript or calculate browser layout.",
        "Media queries are listed but not evaluated because viewport and device settings are unknown.",
        "Complex selectors and inherited/runtime styles may differ from the generated token draft.",
        "No remote stylesheets, fonts, images, or other resources were downloaded.",
    ]
    if script_risk:
        uncertainties.append("The source includes scripts or event handlers; they were inspected only as text and were not executed.")
    if remote_refs:
        uncertainties.append("External references were recorded with query strings removed and skipped without network access.")
    risks = {
        "scripts_detected": parsed.script_tags,
        "inline_scripts_detected": parsed.inline_scripts,
        "event_handlers_detected": parsed.event_handlers,
        "scripts_executed": False,
        "remote_references_skipped": sorted({item["url"] for item in remote_refs}),
        "missing_local_assets": sorted(set(missing_assets)),
        "blocked_path_references": sorted(set(blocked_assets)),
        "css_conflicts": conflicts,
        "media_queries_not_evaluated": media_queries,
        "css_imports_not_loaded": sorted(set(css_imports)),
        "unsafe_token_values_replaced": unsafe_values,
        "font_availability": "Not checked; font names are extracted as references and should be visually verified on the target machine.",
        "uncertainty": uncertainties,
    }
    return {"source": str(source_file), "source_directory": str(root), "tokens": tokens,
            "token_sources": token_sources, "variables": variables, "conflicts": conflicts,
            "font_families": font_families, "css_sources": css_sources, "rules": rules,
            "assets": [item for item in assets if "raw" not in item], "risks": risks}


def _build_frame_md(result: dict[str, Any], name: str) -> str:
    token_block = json.dumps(result["tokens"], ensure_ascii=False, indent=2)
    return f"""# {name} — Imported style draft

Status: **Draft**. This is a static, editable interpretation of a local reference.

## Machine-readable tokens

The first JSON fenced block is the token map consumed by V3 tools.

```json
{token_block}
```

## Visual direction

- Treat the extracted background, ink, accent, muted, and line colors as a palette with a clear reading hierarchy; use the accent sparingly for labels, key numbers, or one focal state.
- Use the display font for short titles and the body font for supporting text. Keep each supplied family stack so browsers can fall back when a face is unavailable.
- Use the mono font for compact technical labels only. Its local availability has not been verified.
- The source page's composition is evidence about its own use case, not a fixed layout for every narration scene. Choose a different composition for a quote, comparison, sequence, or relationship diagram when content calls for it.

## Composition and drawing notes

- Preserve the observed color and typography hierarchy; static analysis cannot reliably infer spacing, responsive behavior, or runtime states.
- Prefer thin rules and restrained geometry when they appear in the source. Do not copy a full webpage or repeat one source layout across every scene.
- Draw scene-specific SVG/CSS only when it makes the narrated relationship easier to understand.

## Motion language

Use short, deliberate reveals that explain a relationship or state change. Favor line drawing, focus changes, and assembly when they match the source's visual language. Avoid continuous decorative motion. Test all motion at arbitrary seek times.

## Do / Don't

- Do use these colors and font stacks consistently across a work.
- Do use the accent for a small number of meaningful focal points.
- Do choose composition from the narration's meaning rather than reusing a reference frame.
- Do keep enough contrast between text and surface colors.
- Do check local font fallback and long Chinese text before export.
- Don't claim browser-computed fidelity from this static import.
- Don't depend on external fonts or images being available offline.
- Don't reproduce source scripts, hidden behaviors, or remote embeds in generated projects.
- Don't use decorative motion that competes with narration.
- Don't treat this draft as user-approved visual acceptance.

## Source and limits

- Source file: {result['source']}
- Import method: local static analysis; no scripts executed and no remote requests made.
- Extracted token sources: {json.dumps(result['token_sources'], ensure_ascii=False)}
- CSS override conflicts: {json.dumps(result['conflicts'], ensure_ascii=False) if result['conflicts'] else 'none detected in parsed custom properties'}
- Review the accompanying import-report.md and assets-manifest.json; edit this draft after visually checking it in a browser.
"""


def _build_preview(tokens: dict[str, str], name: str) -> str:
    safe_name = html.escape(name)
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:; font-src 'none'; connect-src 'none';">
<title>{safe_name} style preview</title>
<style>
:root {{ color-scheme: light; --bg: {tokens['bg']}; --ink: {tokens['ink']}; --accent: {tokens['accent']}; --muted: {tokens['muted']}; --line: {tokens['line']}; --display: {tokens['display_font']}; --body: {tokens['body_font']}; --mono: {tokens['mono_font']}; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 32px; background: var(--bg); color: var(--ink); font-family: var(--body); }}
header {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 1px solid var(--line); padding-bottom: 16px; margin-bottom: 28px; }}
header h1 {{ margin: 0; font: 600 22px/1.15 var(--display); }}
header span, .eyebrow, .label {{ color: var(--accent); font: 600 11px/1.2 var(--mono); letter-spacing: .12em; text-transform: uppercase; }}
main {{ display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: 16px; max-width: 1100px; margin: auto; }}
article {{ min-height: 230px; border: 1px solid var(--line); padding: 26px; position: relative; overflow: hidden; }}
article h2 {{ margin: 12px 0; font: 500 clamp(24px,3vw,38px)/1.05 var(--display); }}
p {{ color: var(--muted); line-height: 1.55; margin: 0; max-width: 48ch; }}
.hero {{ display: flex; flex-direction: column; justify-content: center; }}
.hero:after {{ content: ''; position: absolute; width: 180px; height: 180px; right: -74px; top: -72px; border: 1px solid var(--line); border-radius: 50%; box-shadow: 0 0 0 19px var(--line), 0 0 0 37px var(--line); opacity: .25; }}
.compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: end; }}
.compare section + section {{ border-left: 1px solid var(--line); padding-left: 20px; }}
.compare strong {{ display: block; font: 500 27px/1 var(--display); margin: 12px 0; }}
.sequence ol {{ list-style: none; padding: 0; margin: 22px 0 0; display: flex; gap: 12px; }}
.sequence li {{ flex: 1; border-top: 2px solid var(--accent); padding-top: 10px; font-size: 14px; }}
.sequence b {{ display: block; color: var(--accent); font: 600 12px/1.2 var(--mono); margin-bottom: 8px; }}
.quote {{ display: flex; align-items: center; gap: 24px; }}
.quote .mark {{ color: var(--accent); font: 100px/.7 var(--display); }}
.quote blockquote {{ margin: 0; font: 500 clamp(24px,3vw,36px)/1.12 var(--display); }}
@media (max-width: 700px) {{ body {{ padding: 18px; }} main {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header><h1>{safe_name}</h1><span>Static token showcase</span></header>
<main>
<article class="hero"><span class="eyebrow">01 / Thesis</span><h2>One clear idea</h2><p>Use scale, alignment, and open space to give the key thought room to land.</p></article>
<article class="compare"><section><span class="label">Before</span><strong>Scattered</strong><p>Separate signals compete for attention.</p></section><section><span class="label">After</span><strong>Connected</strong><p>One visible relationship makes the change clear.</p></section></article>
<article class="sequence"><span class="eyebrow">03 / Sequence</span><h2>From signal to outcome</h2><ol><li><b>01</b>Observe</li><li><b>02</b>Connect</li><li><b>03</b>Resolve</li></ol></article>
<article class="quote"><span class="mark">“</span><div><span class="eyebrow">04 / Principle</span><blockquote>Make the important relationship visible.</blockquote></div></article>
</main>
</body>
</html>
'''


def _build_report(result: dict[str, Any], name: str) -> str:
    risks = result["risks"]
    def bullets(items: list[str]) -> str:
        return "\n".join(f"- {item}" for item in items) or "- None detected."
    conflict_lines = [f"{key}: " + " -> ".join(item["value"] for item in values) for key, values in result["conflicts"].items()]
    remote = risks["remote_references_skipped"]
    return f"""# Import report: {name}

Status: **Draft generated from static analysis**.

Source: {result['source']}

No JavaScript was executed, no external request was made, and no source asset was copied. The preview is generated from extracted tokens and contains no source scripts or remote references.

## What was extracted

- CSS sources read: {', '.join(result['css_sources']) if result['css_sources'] else 'no local stylesheet rules found'}
- Token values and source variables are recorded in frame.md.
- Font families seen in CSS: {', '.join(result['font_families']) if result['font_families'] else 'none detected'}

## CSS overrides and uncertainty

{bullets(conflict_lines)}

{bullets(risks['uncertainty'])}

## Safety and missing resources

- Script elements detected: {risks['scripts_detected']}; inline scripts: {risks['inline_scripts_detected']}; event handlers: {risks['event_handlers_detected']}.
- Script execution: **disabled**.
- Remote references skipped: {', '.join(remote) if remote else 'none'}.
- Missing local assets: {', '.join(risks['missing_local_assets']) if risks['missing_local_assets'] else 'none detected'}.
- References outside the source directory were blocked: {', '.join(risks['blocked_path_references']) if risks['blocked_path_references'] else 'none detected'}.
- Font installation/availability was not checked. Use browser fallback and inspect Chinese text on the target machine.
- CSS media queries are listed but not evaluated; viewport-specific results may differ.

## Files

- frame.md: editable style draft; its first JSON block contains machine-readable tokens.
- style-preview.html: standalone, offline preview with four distinct structures.
- assets-manifest.json: referenced local and remote assets, with availability status. Source assets are not copied.
"""


def _slug(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-_").lower()
    if not normalized:
        raise ImportErrorSafe("style name must contain letters or numbers")
    return normalized[:64]


def import_style(source: str | Path, destination: str | Path, name: str | None = None) -> Path:
    """Create a new style directory and refuse to overwrite any existing path."""
    source_file = Path(source).resolve()
    target = Path(destination).expanduser()
    if target.exists():
        raise ImportErrorSafe(f"destination already exists; refusing to overwrite: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target = target.parent.resolve() / target.name
    style_name = name or target.name
    result = inspect_reference(source_file)
    target.mkdir(parents=False, exist_ok=False)
    try:
        (target / "frame.md").write_text(_build_frame_md(result, style_name), encoding="utf-8")
        (target / "style-preview.html").write_text(_build_preview(result["tokens"], style_name), encoding="utf-8")
        (target / "import-report.md").write_text(_build_report(result, style_name), encoding="utf-8")
        (target / "assets-manifest.json").write_text(json.dumps(result["assets"], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except Exception:
        for child in target.iterdir():
            if child.is_file():
                child.unlink()
        target.rmdir()
        raise
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="local HTML reference file")
    parser.add_argument("--out-dir", "--out", dest="out_dir", required=True, help="new style directory; it must not already exist")
    parser.add_argument("--name", help="human-readable style name")
    args = parser.parse_args(argv)
    try:
        output = import_style(args.input, args.out_dir, args.name)
    except (ImportErrorSafe, OSError) as exc:
        print(f"inspect_reference: {exc}", file=sys.stderr)
        return 2
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
