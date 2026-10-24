#!/usr/bin/env python3
"""Audit V3 provenance, coverage, style and local media without executing HTML."""
import argparse
import json
import math
import re
from html.parser import HTMLParser
from pathlib import Path


def load_tokens(path):
    text = Path(path).read_text(encoding='utf-8')
    block = re.search(r'```json\s*(.*?)\s*```', text, re.S)
    if not block:
        raise ValueError('frame.md needs a JSON token block')
    data = json.loads(block.group(1))
    tokens = data.get('tokens', data)
    required = {'bg', 'ink', 'accent', 'muted', 'line', 'display_font', 'body_font', 'mono_font'}
    if required - tokens.keys():
        raise ValueError('Missing style tokens: ' + ', '.join(sorted(required - tokens.keys())))
    for key in ['bg', 'ink', 'accent', 'muted', 'line']:
        if not isinstance(tokens[key], str) or not re.fullmatch(r'(?:#[0-9a-fA-F]{3,8}|(?:rgb|rgba|hsl|hsla)\([0-9.%\s,/+-]+\)|[a-zA-Z]{1,24})', tokens[key]):
            raise ValueError('Expected a safe CSS color: ' + key)
    return tokens


class Composition(HTMLParser):
    def __init__(self):
        super().__init__()
        self.roots, self.clips, self.assets = [], [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'data-composition-id' in a:
            self.roots.append(a)
        if 'clip' in a.get('class', '').split():
            self.clips.append(a)
        if tag in ('script', 'img', 'video', 'audio', 'source') and a.get('src'):
            self.assets.append(a['src'])


def audit(project):
    project = Path(project)
    errors, warnings = [], []
    required = ['source-map.md', 'input.json', 'scenes.json', 'scene-plan.md', 'visual-storyboard.md', 'frame.md', 'index.html']
    missing = [name for name in required if not (project / name).is_file()]
    if missing:
        return {'status': 'BLOCKED', 'errors': ['Missing files: ' + ', '.join(missing)], 'warnings': []}
    try:
        tokens = load_tokens(project / 'frame.md')
        inputs = json.loads((project / 'input.json').read_text())
        data = json.loads((project / 'scenes.json').read_text())
        scenes = data.get('scenes', []) if isinstance(data, dict) else data
        duration = float(inputs['duration'])
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError('Invalid timed input duration')
        cues = inputs['cues']
        ids = {str(cue['id']) for cue in cues}
        covered, seen = set(), set()
        last = 0
        samples = {0.0, max(0, duration - .04)}
        for scene in scenes:
            sid = scene['scene_id']
            start, end = float(scene['start']), float(scene['end'])
            if sid in seen or not all(math.isfinite(x) for x in [start, end]) or end <= start or abs(start-last) > .002:
                errors.append('Invalid/non-contiguous scene: ' + sid)
            seen.add(sid)
            last = end
            cue_ids = set(map(str, scene.get('cue_ids', [])))
            if not cue_ids or cue_ids - ids:
                errors.append('Missing or unknown cue IDs: ' + sid)
            covered |= cue_ids
            for cue in cues:
                if str(cue['id']) in cue_ids and (cue['end'] <= start - .002 or cue['start'] >= end + .002):
                    errors.append('Cue outside assigned scene: ' + sid + '/' + str(cue['id']))
            samples.update([start, min(end-.04, start+.8), max(start, end-.04)])
            if start > 0:
                samples.add(max(0, start-.04))
            for relative in scene.get('reveal_times', []):
                t = float(relative)
                if t < 0 or t >= end-start:
                    errors.append('Reveal outside scene: ' + sid)
                else:
                    samples.add(min(end-.04, start+t+.7))
        if not scenes or abs(last-duration) > .002:
            errors.append('Scenes do not cover full input duration')
        if ids != covered:
            errors.append('Cue coverage mismatch: ' + str(sorted(ids ^ covered)))
        source = (project / 'index.html').read_text()
        doc = Composition(); doc.feed(source)
        if len(doc.roots) != 1:
            errors.append('Expected exactly one composition root')
        else:
            root = doc.roots[0]
            if abs(float(root.get('data-duration', 0))-duration) > .002:
                errors.append('HTML/input duration mismatch')
            if (root.get('data-width'), root.get('data-height')) != ('1920', '1080'):
                errors.append('Expected 1920x1080 canvas')
        if len(doc.clips) != len(scenes):
            errors.append('HTML/plan scene count mismatch')
        for clip, scene in zip(doc.clips, scenes):
            if abs(float(clip.get('data-start', -1))-scene['start']) > .002 or abs(float(clip.get('data-duration', -1))-(scene['end']-scene['start'])) > .002:
                errors.append('HTML/plan timing mismatch: ' + scene['scene_id'])
        for src in doc.assets:
            if re.match(r'(https?:)?//', src):
                errors.append('Render dependency must be local: ' + src)
            elif not src.startswith('data:') and not (project / src.split('?')[0]).is_file():
                errors.append('Missing asset: ' + src)
        if 'data-at=' in source:
            errors.append('V2 data-at is not a V3 timeline API')
        return {'status': 'BLOCKED' if errors else 'NEEDS_VISUAL_REVIEW', 'errors': errors, 'warnings': warnings,
                'duration': duration, 'scenes': len(scenes), 'cues': len(cues), 'tokens': tokens,
                'sample_times': sorted(round(t, 4) for t in samples)}
    except (ValueError, KeyError, TypeError, OSError) as exc:
        return {'status': 'BLOCKED', 'errors': [str(exc)], 'warnings': warnings}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = audit(args.project)
    encoded = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(encoded, encoding='utf-8')
    print(encoded)
    raise SystemExit(bool(result['errors']))

if __name__ == '__main__':
    main()
