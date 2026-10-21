#!/usr/bin/env python3
"""Static preflight and ZIP packer; not an official platform compatibility audit."""
import argparse
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import zipfile

ALLOWED = {'.html', '.css', '.js', '.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg', '.woff', '.woff2', '.json'}
LIMIT = 10 * 1024 * 1024


def preflight(source):
    source = Path(source).resolve()
    if not source.is_dir():
        raise ValueError('Source is not a directory')
    entries = sorted(source.rglob('*'))
    files = []
    for entry in entries:
        if entry.is_symlink():
            raise ValueError('Symlinks cannot be packaged: ' + str(entry))
        if entry.is_file():
            name = entry.relative_to(source)
            if any(part.startswith('.') or part == 'node_modules' for part in name.parts):
                raise ValueError('Development or hidden file: ' + str(name))
            if entry.suffix.lower() not in ALLOWED:
                raise ValueError('Unsupported runtime file: ' + str(name))
            files.append(entry)
    if [p.relative_to(source).as_posix() for p in files if p.suffix.lower() == '.html'] != ['index.html']:
        raise ValueError('Exactly one HTML entry is required at source/index.html')
    warnings = []
    total_text = 0
    for file in files:
        if file.suffix.lower() not in {'.html', '.js', '.css', '.json', '.svg'}:
            continue
        text = file.read_text(encoding='utf-8-sig')
        label = file.relative_to(source).as_posix()
        size = file.stat().st_size
        total_text += size
        if size > 2 * 1024 * 1024:
            warnings.append(label + ': text file exceeds 2 MiB; inspect manually')
        if re.search(r'https?://', text) and file.suffix.lower() != '.svg':
            raise ValueError(label + ': external URL found; inspect and remove runtime dependencies')
        if file.suffix.lower() == '.js':
            forbidden = r'\bfetch\s*\(|\bXMLHttpRequest\b|\bnew\s+(?:Worker|SharedWorker|WebSocket|EventSource|RTCPeerConnection)\b|\beval\s*\(|\bnew\s+Function\b|\bWebAssembly\b|navigator\.(?:clipboard|geolocation|serviceWorker)|window\.(?:open|prompt)\s*\(|^\s*(?:import|export)\s'
            if re.search(forbidden, text, re.M):
                raise ValueError(label + ': prohibited or unsupported runtime pattern')
        if file.suffix.lower() == '.html':
            if not re.search(r'<!doctype\s+html>', text, re.I) or 'viewport-fit=cover' not in text:
                raise ValueError(label + ': doctype or viewport-fit=cover missing')
            if re.search(r'\son[a-z]+\s*=|javascript:|<(?:iframe|object|base)\b|\bdownload\s*[=>]|target\s*=\s*[\"\x27]_blank', text, re.I):
                raise ValueError(label + ': inline event, download, embedded page or external navigation')
            for attrs, body in re.findall(r'<script\b([^>]*)>(.*?)</script\s*>', text, re.I | re.S):
                if not re.search(r'\bsrc\s*=', attrs, re.I) or body.strip() or re.search(r'\btype\s*=', attrs, re.I):
                    raise ValueError(label + ': use only external classic scripts')
            refs = re.findall(r'(?:src|href)\s*=\s*[\"\x27]([^\"\x27]+)', text, re.I)
        elif file.suffix.lower() == '.css':
            refs = re.findall(r'url\(\s*[\"\x27]?([^\"\x27)\s]+)', text, re.I)
            if re.search(r'@import\b', text, re.I):
                raise ValueError(label + ': CSS imports require manual bundling')
        else:
            refs = []
        for ref in refs:
            if ref.startswith('#'):
                continue
            parsed = urlsplit(ref)
            if parsed.scheme or parsed.netloc or ref.startswith('/'):
                raise ValueError(label + ': static resources must be package-relative: ' + ref)
            target = (file.parent / unquote(parsed.path)).resolve()
            if source not in target.parents or not target.is_file():
                raise ValueError(label + ': missing or out-of-package resource: ' + ref)
    if total_text > 5 * 1024 * 1024:
        warnings.append('Combined text exceeds 5 MiB; inspect data and source size')
    return files, warnings, total_text


def package(source, output, report=None):
    source = Path(source).resolve()
    output = Path(output).resolve()
    report = Path(report).resolve() if report else None
    if output.suffix.lower() != '.zip':
        raise ValueError('Output must have a .zip extension')
    for target in [output, report]:
        if target and (target == source or source in target.parents):
            raise ValueError('Output ZIP and report must be outside the runtime source directory')
        if target and target.exists():
            raise ValueError('Refusing to overwrite existing output: ' + str(target))
    if report == output:
        raise ValueError('Report and ZIP paths must be different')
    files, warnings, total_text = preflight(source)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        with zipfile.ZipFile(output, 'x', compression=zipfile.ZIP_DEFLATED) as archive:
            for file in files:
                archive.write(file, file.relative_to(source).as_posix())
        size = output.stat().st_size
        if size > LIMIT:
            raise ValueError('ZIP exceeds 10 MiB; reduce assets before packaging')
    except Exception:
        output.unlink(missing_ok=True)
        raise
    if size > 2 * 1024 * 1024:
        warnings.append('ZIP exceeds recommended 2 MiB')
    result = {'status': 'static-preflight-passed', 'zip': str(output), 'bytes': size,
              'file_count': len(files), 'text_bytes': total_text, 'warnings': warnings,
              'platform_acceptance': 'not-tested',
              'next': ['Run the current official skill audit', 'Test creator-platform simulator', 'Test Android QR preview', 'Test iOS QR preview']}
    if report:
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    try:
        result = package(args.source, args.output, args.report)
    except (ValueError, OSError, UnicodeError, zipfile.BadZipFile) as error:
        print(json.dumps({'status': 'failed', 'error': str(error)}, ensure_ascii=False))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
