#!/usr/bin/env python3
"""Prepare a V3 authoring folder; Codex authors the semantic scenes and artwork."""
import argparse
import json
import re
import shutil
from pathlib import Path
from audit_project import load_tokens
from prepare_input import prepare_input

SKILL = Path(__file__).resolve().parent.parent
UPSTREAM_COMMIT = '934c88bac8cf6dc37db07cecf3bd0b58314c9921'
OFFICIAL_STYLES = frozenset(('cartesian', 'code-editorial', 'blockframe',
                             'broadside', 'cobalt-grid', 'daisy-days', 'editorial-forest'))


def resolve_style(name):
    """Return (frame.md path, style directory) for a built-in name or imported style dir."""
    path = Path(name)
    frame = path / 'frame.md' if path.is_dir() else path if path.is_file() else SKILL / 'styles' / name / 'frame.md'
    if not frame.is_file():
        raise ValueError('Unknown style or missing frame.md: ' + name)
    load_tokens(frame)
    return frame, frame.parent


def pack_style_assets(style_dir, out):
    """Copy the style pack's licensed assets (e.g. fonts) into the new project.

    Works only reference their own project-relative paths, so a project stays
    portable and never borrows a sibling project's font files.
    """
    packed = []
    fonts = style_dir / 'fonts'
    if fonts.is_dir():
        target = out / 'assets' / 'fonts'
        target.mkdir(parents=True, exist_ok=True)
        for item in sorted(fonts.iterdir()):
            if item.is_file():
                shutil.copyfile(item, target / item.name)
                packed.append('assets/fonts/' + item.name)
    return packed


def pack_style_guidance(style_dir, out):
    """Keep a project's design authority beside its machine-readable tokens."""
    frame_text = (style_dir / 'frame.md').read_text(encoding='utf-8')
    upstream = style_dir / 'upstream'
    official = (style_dir.name in OFFICIAL_STYLES
                and style_dir.resolve().parent == (SKILL / 'styles').resolve())
    showcase_url = ('https://github.com/heygen-com/hyperframes/blob/'
                    + UPSTREAM_COMMIT + '/skills/hyperframes/assets/frame-presets/'
                    + style_dir.name + '/frame-showcase.html') if official else None
    if (upstream / 'FRAME.md').is_file():
        target = out / 'upstream'
        target.mkdir()
        for name in ('FRAME.md', 'SOURCE.md'):
            if (upstream / name).is_file():
                text = (upstream / name).read_text(encoding='utf-8')
                if name == 'SOURCE.md':
                    text = text.replace('../fonts/', '../assets/fonts/')
                    text = text.replace('(../../../references/', '(../references/')
                    if official:
                        for link in ('./frame-showcase.html', 'frame-showcase.html'):
                            text = text.replace('(' + link + ')', '(' + showcase_url + ')')
                (target / name).write_text(text, encoding='utf-8')
        if official:
            for link in ('upstream/frame-showcase.html', './upstream/frame-showcase.html',
                         'frame-showcase.html', './frame-showcase.html'):
                frame_text = frame_text.replace('(' + link + ')', '(' + showcase_url + ')')
        elif (upstream / 'frame-showcase.html').is_file():
            shutil.copyfile(upstream / 'frame-showcase.html', target / 'frame-showcase.html')
    frame_text = frame_text.replace('(fonts/)', '(assets/fonts/)')
    # Code Editorial's additional local execution notes are part of its reading path.
    ref_name = 'code-editorial-execution.md'
    if '(../../references/' + ref_name + ')' in frame_text:
        target = out / 'references'
        target.mkdir()
        guide = (SKILL / 'references' / ref_name).read_text(encoding='utf-8')
        guide = guide.replace('../styles/code-editorial/upstream/FRAME.md', '../upstream/FRAME.md')
        if showcase_url:
            guide = guide.replace('`upstream/frame-showcase.html`', '[官方 showcase](' + showcase_url + ')')
        (target / ref_name).write_text(guide, encoding='utf-8')
        frame_text = frame_text.replace('(../../references/' + ref_name + ')', '(references/' + ref_name + ')')
    (out / 'frame.md').write_text(frame_text, encoding='utf-8')


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('source', type=Path)
    cli.add_argument('--out', required=True, type=Path)
    cli.add_argument('--style', default='cartesian', help='Built-in name or imported style directory')
    cli.add_argument('--start', type=float)
    cli.add_argument('--end', type=float)
    args = cli.parse_args()
    try:
        _, style_dir = resolve_style(args.style)
        if args.out.exists():
            raise ValueError('Output already exists; choose a new project directory')
        # Input function contract is shared with the standalone prepare_input tool.
        data = prepare_input(args.source, start=args.start, end=args.end)
        args.out.mkdir(parents=True)
        (args.out / 'assets').mkdir()
        (args.out / 'review').mkdir()
        (args.out / 'input.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        pack_style_guidance(style_dir, args.out)
        packed = pack_style_assets(style_dir, args.out)
        shutil.copyfile(args.source, args.out / ('source' + args.source.suffix))
        (args.out / 'source-map.md').write_text('# 字幕来源\n\n源文件：`' + args.source.name + '`；原文完整保存在 source 文件。\n\n时间映射及选段见 input.json。不得把纯文本估时称为精确同步。\n', encoding='utf-8')
        (args.out / 'scene-plan.md').write_text('# 内容分镜 · 待 Codex 编写\n\n先阅读完整字幕；逐场记录 scene_id、start/end、cue_ids、观众收获、关系、屏幕短文案与素材状态。\n', encoding='utf-8')
        (args.out / 'visual-storyboard.md').write_text('# 视觉分镜 · 待 Codex 编写\n\n遵循 frame.md；逐场说明构图、阅读路径、自绘图形、解释性变化、相对动效时间和素材真实性。\n', encoding='utf-8')
        (args.out / 'meta.json').write_text(json.dumps({'id': args.out.name, 'name': args.out.name}, ensure_ascii=False, indent=2), encoding='utf-8')
        print('Prepared', args.out, '— planning scaffold, not a generated composition')
        if packed:
            print('Packed style assets:', ', '.join(packed))
    except (ValueError, OSError) as exc:
        cli.error(str(exc))

if __name__ == '__main__':
    main()
