#!/usr/bin/env python3
"""Render forum thread Markdown files as clean archival HTML.

Forum pages saved from Discuz contain navigation, login widgets, reply forms,
footer marketing text, and ad containers.  The knowledge base only needs the
verified thread content, so this renderer builds ``thread.html`` from
``index.md`` and keeps only source metadata plus the extracted floor text.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sobko_mcp.common import load_frontmatter_markdown


URL_PATTERN = re.compile(r"<(https?://[^>]+)>")
BOLD_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
IMAGE_LINE_PATTERN = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")


def render_inline(text: str) -> str:
    """Escape text and render the small Markdown subset used by forum files."""

    escaped = html.escape(text)
    escaped = re.sub(
        r"&lt;(https?://[^&<>]+(?:&amp;[^&<>]+)*)&gt;",
        lambda match: f'<a href="{match.group(1)}">{match.group(1)}</a>',
        escaped,
    )
    escaped = URL_PATTERN.sub(lambda match: f'<a href="{match.group(1)}">{match.group(1)}</a>', escaped)
    return BOLD_PATTERN.sub(lambda match: f"<strong>{match.group(1)}</strong>", escaped)


def flush_paragraph(buffer: list[str], parts: list[str]) -> None:
    """Flush accumulated paragraph lines to HTML."""

    if not buffer:
        return
    paragraph = "<br>\n".join(render_inline(line) for line in buffer)
    parts.append(f"<p>{paragraph}</p>")
    buffer.clear()


def render_markdown_body(body: str) -> str:
    """Render headings, bullet lists, and paragraphs from Markdown body."""

    parts: list[str] = []
    paragraph: list[str] = []
    in_list = False

    for raw_line in body.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            flush_paragraph(paragraph, parts)
            if in_list:
                parts.append("</ul>")
                in_list = False
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph(paragraph, parts)
            if in_list:
                parts.append("</ul>")
                in_list = False
            level = min(len(heading_match.group(1)) + 1, 6)
            parts.append(f"<h{level}>{render_inline(heading_match.group(2))}</h{level}>")
            continue

        image_match = IMAGE_LINE_PATTERN.fullmatch(stripped)
        if image_match:
            flush_paragraph(paragraph, parts)
            if in_list:
                parts.append("</ul>")
                in_list = False
            alt = html.escape(image_match.group("alt"))
            path = html.escape(image_match.group("path"))
            parts.append(f'<figure><img src="{path}" alt="{alt}" style="max-width:100%; height:auto;"><figcaption>{alt}</figcaption></figure>')
            continue

        if stripped.startswith("- "):
            flush_paragraph(paragraph, parts)
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{render_inline(stripped[2:])}</li>")
            continue

        if in_list:
            parts.append("</ul>")
            in_list = False
        paragraph.append(stripped)

    flush_paragraph(paragraph, parts)
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def render_clean_html(index_path: Path) -> str:
    """Render one ``index.md`` file into a clean standalone HTML document."""

    metadata, body = load_frontmatter_markdown(index_path.read_text(encoding="utf-8"))
    title = metadata.get("title") or index_path.parent.name
    canonical_url = metadata.get("url", "")
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
body {{ max-width: 920px; margin: 2rem auto; padding: 0 1rem; line-height: 1.72; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #1f2933; }}
a {{ color: #2563eb; }}
h1, h2, h3, h4 {{ line-height: 1.35; }}
.source-note {{ color: #667085; font-size: 0.92rem; border-bottom: 1px solid #e5e7eb; padding-bottom: 1rem; margin-bottom: 1.5rem; }}
strong {{ color: #111827; }}
</style>
</head>
<body>
<!-- Clean archival copy generated from browser-verified Markdown; site navigation, login widgets, reply forms, footers, and ad containers are intentionally omitted. -->
<h1>{html.escape(title)}</h1>
<div class="source-note">
<div>Source: {f'<a href="{html.escape(canonical_url)}">{html.escape(canonical_url)}</a>' if canonical_url else "local forum archive"}</div>
<div>Archive scope: 仅保留已抽取正文；站点导航、登录/回帖控件、页脚和非正文区已移除。</div>
</div>
{render_markdown_body(body)}
</body>
</html>
"""


def iter_index_paths(paths: list[Path]) -> list[Path]:
    """Expand file or directory arguments into forum ``index.md`` paths."""

    index_paths: list[Path] = []
    for path in paths:
        if path.is_dir():
            index_paths.extend(sorted(path.rglob("index.md")))
        elif path.name == "index.md":
            index_paths.append(path)
    return index_paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Render clean forum thread HTML from Markdown archives.")
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        default=[Path("data_sources/sobko_sources/forum_threads")],
        help="Forum thread directories or index.md files to render.",
    )
    args = parser.parse_args()

    rendered_count = 0
    for index_path in iter_index_paths(args.paths):
        output_path = index_path.parent / "thread.html"
        output_path.write_text(render_clean_html(index_path), encoding="utf-8")
        rendered_count += 1
        print(f"rendered {output_path}")
    print(f"rendered_html={rendered_count}")


if __name__ == "__main__":
    main()
