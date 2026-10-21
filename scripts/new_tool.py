#!/usr/bin/env python3
"""Copy the bundled bead helper to a new project without overwriting files."""
import argparse
import html
from pathlib import Path
import shutil


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--title', default='拼豆配色小助手')
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1] / 'assets' / 'bead-helper'
    output = args.output.expanduser().resolve()
    if output.exists():
        parser.error('Output already exists; choose a new project directory.')
    if source == output or source in output.parents:
        parser.error('Output must be outside the template directory.')
    shutil.copytree(source, output)
    index = output / 'index.html'
    text = index.read_text(encoding='utf-8')
    text = text.replace('<title>拼豆配色小助手</title>', '<title>' + html.escape(args.title) + '</title>')
    index.write_text(text, encoding='utf-8')
    print(str(output))


if __name__ == '__main__':
    main()
