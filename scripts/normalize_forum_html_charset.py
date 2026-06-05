#!/usr/bin/env python3
"""Normalize saved forum HTML files to UTF-8.

The forum advertises GBK in its original pages, but browser/CDP DOM dumps are
written as UTF-8.  If the old ``charset=gbk`` declaration is kept, opening the
saved HTML locally makes Chinese text look garbled.  This helper rewrites saved
HTML to UTF-8 bytes and updates/inserts the charset declaration.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


CHARSET_PATTERN = re.compile(r"charset\s*=\s*([\"']?)(?P<value>[^\"'\s;>]+)\1", flags=re.IGNORECASE)
HEAD_PATTERN = re.compile(r"<head([^>]*)>", flags=re.IGNORECASE)


def decode_html(raw: bytes) -> str:
    """Decode saved HTML as UTF-8 first, then GB18030 for raw forum bytes."""

    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gb18030")


def normalize_html_text(text: str) -> str:
    """Return HTML text with an explicit UTF-8 charset declaration."""

    charset_match = CHARSET_PATTERN.search(text)
    if charset_match and charset_match.group("value").lower() == "utf-8":
        return text
    if charset_match:
        return CHARSET_PATTERN.sub("charset=utf-8", text, count=1)
    if HEAD_PATTERN.search(text):
        return HEAD_PATTERN.sub(r'<head\1>\n<meta charset="utf-8">', text, count=1)
    return '<meta charset="utf-8">\n' + text


def normalize_file(path: Path) -> bool:
    """Normalize one HTML file and return whether its content changed."""

    original = path.read_bytes()
    normalized = normalize_html_text(decode_html(original)).encode("utf-8")
    if normalized == original:
        return False
    path.write_bytes(normalized)
    return True


def iter_html_paths(paths: list[Path]) -> list[Path]:
    """Expand file or directory arguments into sorted HTML file paths."""

    html_paths: list[Path] = []
    for path in paths:
        if path.is_dir():
            html_paths.extend(sorted(path.rglob("*.html")))
        elif path.suffix.lower() == ".html":
            html_paths.append(path)
    return html_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize saved forum HTML charset declarations to UTF-8.")
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("data_sources/sobko_sources/forum_threads")],
        help="HTML files or directories to normalize.",
    )
    args = parser.parse_args()

    changed_count = 0
    for html_path in iter_html_paths(args.paths):
        if normalize_file(html_path):
            changed_count += 1
            print(f"updated {html_path}")
    print(f"normalized_html={changed_count}")


if __name__ == "__main__":
    main()
