#!/usr/bin/env python3
"""Run the cheap audit/lint or a browser check, saving complete JSON reports."""
import argparse
import json
import os
import subprocess
from pathlib import Path
try:
    import fcntl
except ImportError:  # Windows agents can still use the single-Skill package.
    import msvcrt

from audit_project import audit


SKILL = Path(__file__).resolve().parent.parent
CLI = SKILL / 'node_modules' / '.bin' / 'hyperframes'


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def lock_project(lock):
    if 'fcntl' in globals():
        fcntl.flock(lock, fcntl.LOCK_EX)
    else:
        lock.write('0')
        lock.flush()
        lock.seek(0)
        msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)


def findings(report):
    if 'findings' in report:
        return report['findings']
    return [item for section in ('lint', 'runtime', 'layout', 'motion', 'contrast', 'craft')
            for item in report.get(section, {}).get('findings', [])]


def run_cli(project, mode, output):
    command = [str(CLI), 'lint' if mode == 'quick' else 'check', str(project), '--json']
    if mode == 'full':
        command.append('--snapshots')
    env = {**os.environ, 'HYPERFRAMES_NO_TELEMETRY': '1', 'DO_NOT_TRACK': '1'}
    result = subprocess.run(command, cwd=SKILL, env=env, text=True, capture_output=True)
    name = 'lint' if mode == 'quick' else 'check'
    (output / f'{name}.stderr.log').write_text(result.stderr, encoding='utf-8')
    (output / f'{name}.stdout.log').write_text(result.stdout, encoding='utf-8')
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError:
        detail = result.stderr.strip()[-700:]
        raise RuntimeError(f'{name} did not return JSON (exit {result.returncode}): {detail}; full output saved in {output}')
    save_json(output / f'{name}.json', report)
    if mode != 'quick' and 'lint' in report:
        save_json(output / 'lint.json', report['lint'])
    return result.returncode, report, result.stderr


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('project', type=Path)
    parser.add_argument('--mode', choices=('quick', 'check', 'full'), default='quick',
                        help='quick=audit+lint; check=browser check; full=browser check with snapshots')
    args = parser.parse_args()
    project = args.project.resolve()
    output = project / 'review' / 'checks'
    output.mkdir(parents=True, exist_ok=True)
    if not CLI.is_file():
        parser.error(f'Pinned HyperFrames CLI is missing: run npm ci in {SKILL}')
    # A per-project lock prevents two agents from writing the same check output simultaneously.
    with (output / '.lock').open('w') as lock:
        lock_project(lock)
        result = audit(project)
        save_json(output / 'audit.json', result)
        if result['errors']:
            print(f"audit: {len(result['errors'])} errors; HyperFrames skipped")
            for issue in result['errors']:
                print('  ' + issue)
            return 1
        try:
            code, report, stderr = run_cli(project, args.mode, output)
        except RuntimeError as exc:
            print(f'check failed: {exc}')
            return 1
        issues = findings(report)
        errors = [x for x in issues if x.get('severity') == 'error']
        warnings = [x for x in issues if x.get('severity') == 'warning']
        print(f'{args.mode}: {len(errors)} errors, {len(warnings)} warnings; report: {output / ("lint.json" if args.mode == "quick" else "check.json")}')
        for issue in errors + warnings[:10]:
            location = issue.get('file') or issue.get('sourceFile') or issue.get('selector') or 'project'
            line = issue.get('line')
            print(f"  {issue.get('severity')}: {location}{':' + str(line) if line else ''} {issue.get('code', '')}: {issue.get('message', '')}")
        if len(warnings)>10:
            print(f'  {len(warnings)-10} more warnings in saved JSON')
        if args.mode != 'quick':
            print(f"  browserSkipped={report.get('browserSkipped')}; snapshots={len(report.get('snapshots', {}).get('files', []))}")
        if 'EEXIST' in stderr or 'EEXIST' in str(report.get('error', '')):
            print('  EEXIST: HyperFrames could not create an existing path. Check the saved stderr and concurrent runs; .hyperframes was preserved.')
        if code or not report.get('ok', False) or (args.mode != 'quick' and report.get('browserSkipped') is not False):
            if not errors:
                print(f'  Check failed (exit {code}); inspect saved JSON and stderr for the exact cause.')
            return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
