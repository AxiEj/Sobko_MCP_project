"""将 Sobko 知识源标准化为 source/chunk/image/section 记录。"""

from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple

from .common import (
    SOFTWARE_SYNONYMS,
    TOPIC_SYNONYMS,
    detect_language,
    extract_method_tags,
    extract_tags,
    load_frontmatter_markdown,
    make_snippet,
    normalize_whitespace,
    read_jsonl,
    split_paragraph_to_chunks,
    stable_hash,
    write_jsonl,
)
from .config import ProjectLayout, resolve_portable_path, to_portable_path

IMAGE_PATTERN = re.compile(r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)]+)\)")
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.*)$")


def _parse_markdown_blocks(text: str) -> List[Dict[str, Any]]:
    """把 Markdown 文本解析为轻量 block 列表。

    功能目的：
        在不引入 Markdown 解析依赖的情况下识别标题、代码块、图片和段落。
    输入参数：
        text：Markdown 正文。
    返回值：
        block 字典列表。
    关键流程：
        按行扫描；标题和代码块优先，单独图片行记录为 image，其余连续非空行合并为段落。
    可能报错或边界情况：
        内联图片不会从段落中拆出；当前 Sobko 学术帖主要使用独立图片行，足够稳定。
    """

    lines = text.splitlines()
    blocks: List[Dict[str, Any]] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue
        heading_match = HEADING_PATTERN.match(stripped)
        if heading_match:
            blocks.append({"type": "heading", "level": len(heading_match.group(1)), "text": heading_match.group(2).strip()})
            index += 1
            continue
        if stripped.startswith("```"):
            fence = stripped[:3]
            code_lines = [line]
            index += 1
            while index < len(lines):
                code_lines.append(lines[index])
                if lines[index].strip().startswith(fence):
                    index += 1
                    break
                index += 1
            blocks.append({"type": "code", "text": "\n".join(code_lines).strip()})
            continue
        image_match = IMAGE_PATTERN.fullmatch(stripped)
        if image_match:
            blocks.append(
                {
                    "type": "image",
                    "alt": image_match.group("alt").strip(),
                    "path": image_match.group("path").strip(),
                }
            )
            index += 1
            continue
        paragraph_lines = [line]
        index += 1
        while index < len(lines):
            peek = lines[index]
            peek_stripped = peek.strip()
            if not peek_stripped:
                break
            if HEADING_PATTERN.match(peek_stripped) or peek_stripped.startswith("```") or IMAGE_PATTERN.fullmatch(peek_stripped):
                break
            paragraph_lines.append(peek)
            index += 1
        blocks.append({"type": "paragraph", "text": normalize_whitespace("\n".join(paragraph_lines))})
    return blocks


def _classify_chunk_type(text: str) -> str:
    """推断 chunk 类型。

    功能目的：
        给命令、FAQ、普通文本设置粗粒度类型，便于后续过滤或展示。
    输入参数：
        text：chunk 文本。
    返回值：
        `text`、`command` 或 `faq`。
    关键流程：
        使用简单关键词匹配，不改变正文内容。
    可能报错或边界情况：
        类型只是辅助字段，误判不会影响检索正确性。
    """

    lowered = text.lower()
    if "faq" in lowered or "常见问题" in text:
        return "faq"
    if re.search(r"\b(?:command-line|命令行|orca_2mkl|formchk|cubegen|gmx|mpirun)\b", text, flags=re.IGNORECASE):
        return "command"
    return "text"


def _flush_text_buffer(
    *,
    source: Dict[str, Any],
    buffer_texts: List[str],
    section_path: List[str],
    page_range: List[int] | None,
    pending_image_ids: List[str],
    chunk_records: List[Dict[str, Any]],
) -> None:
    """把缓冲区文本写成一个或多个 chunk。

    功能目的：
        将连续段落合并后按长度切分，并附带 source 元数据与图片引用。
    输入参数：
        source：当前 source 记录。
        buffer_texts：待写出的段落缓冲区。
        section_path：当前小节路径。
        page_range：手册页码范围；博客为 None。
        pending_image_ids：紧邻文本前出现的图片 ID。
        chunk_records：输出 chunk 列表。
    返回值：
        无，直接修改 `chunk_records`、`buffer_texts` 和 `pending_image_ids`。
    关键流程：
        先合并段落，再按自然边界切分，每个子段生成稳定 chunk_id。
    可能报错或边界情况：
        空缓冲区直接返回；图片如果位于文末且无后续文本，会保留 orphan image 记录。
    """

    if not buffer_texts:
        return
    merged = "\n\n".join(item for item in buffer_texts if item).strip()
    if not merged:
        buffer_texts.clear()
        return
    for piece in split_paragraph_to_chunks(merged):
        chunk_index = len(chunk_records) + 1
        chunk_id = f'{source["source_id"]}#chunk-{chunk_index:04d}'
        text_for_tags = f'{source["title"]}\n{" / ".join(section_path)}\n{piece}'
        image_ids = list(pending_image_ids)
        chunk_records.append(
            {
                "chunk_id": chunk_id,
                "source_id": source["source_id"],
                "title": source["title"],
                "section_path": list(section_path),
                "page_range": page_range,
                "chunk_type": _classify_chunk_type(piece),
                "software_tags": sorted(set(source.get("software_tags", []) + extract_tags(text_for_tags, SOFTWARE_SYNONYMS))),
                "method_tags": extract_method_tags(text_for_tags),
                "topic_tags": sorted(set(source.get("topic_tags", []) + extract_tags(text_for_tags, TOPIC_SYNONYMS))),
                "authority_level": source["authority_level"],
                "source_type": source["source_type"],
                "language": detect_language(text_for_tags),
                "has_image": bool(image_ids),
                "image_ids": image_ids,
                "prev_chunk_id": None,
                "next_chunk_id": None,
                "text": piece,
                "snippet": make_snippet(piece),
                "canonical_path": source["canonical_path"],
                "canonical_url": source["canonical_url"],
                "html_path": source.get("html_path"),
                "dom_anchor": None,
                "chunk_hash": stable_hash(piece),
            }
        )
        pending_image_ids.clear()
    buffer_texts.clear()


def _finalize_chunk_links(chunk_records: List[Dict[str, Any]]) -> None:
    """补齐 chunk 前后指针。

    功能目的：
        支持 `sobko_fetch` 展开前后上下文。
    输入参数：
        chunk_records：同一 source 内按顺序生成的 chunk 列表。
    返回值：
        无，原地写入 `prev_chunk_id` 和 `next_chunk_id`。
    关键流程：
        按列表顺序给每个 chunk 连接相邻 ID。
    可能报错或边界情况：
        空列表会自然跳过。
    """

    for index, record in enumerate(chunk_records):
        record["prev_chunk_id"] = chunk_records[index - 1]["chunk_id"] if index > 0 else None
        record["next_chunk_id"] = chunk_records[index + 1]["chunk_id"] if index + 1 < len(chunk_records) else None


def _next_section_path(current: List[str], heading_level: int, heading_text: str) -> List[str]:
    """根据 Markdown 标题层级更新 section_path。

    功能目的：
        避免同级标题互相嵌套，生成更准确的小节路径。
    输入参数：
        current：当前 section_path。
        heading_level：Markdown 标题层级，`#` 为 1。
        heading_text：标题文本。
    返回值：
        更新后的 section_path。
    关键流程：
        source 标题固定保留在第 0 层；Markdown 标题层级映射到其后的层级。
    可能报错或边界情况：
        如果文档从 `###` 开始，会保留已有上级路径并追加当前标题。
    """

    keep = max(1, heading_level - 1)
    return [*current[:keep], heading_text]


def _normalize_blog_source(
    layout: ProjectLayout,
    source: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """标准化思想家公社学术帖。

    功能目的：
        将单篇 Markdown 帖子切分为可检索 chunk，并保留图片路径和邻近文本。
    输入参数：
        layout：项目目录布局。
        source：source registry 中的一条 `blog_post` 记录。
    返回值：
        `(chunks, images, sections)` 三类记录列表。
    关键流程：
        解析 front matter -> 扫描 Markdown block -> 生成 chunk/image/section -> 关联图片邻近文本。
    可能报错或边界情况：
        图片文件缺失不会阻断文本索引，但 `get_image` 返回路径时用户会看到实际文件不存在。
    """

    markdown_path = resolve_portable_path(layout, source["canonical_path"])
    metadata, body = load_frontmatter_markdown(markdown_path.read_text(encoding="utf-8"))
    blocks = _parse_markdown_blocks(body)
    section_path: List[str] = [source["title"]]
    buffer_texts: List[str] = []
    pending_image_ids: List[str] = []
    chunk_records: List[Dict[str, Any]] = []
    image_records: List[Dict[str, Any]] = []
    section_records: List[Dict[str, Any]] = [
        {
            "source_id": source["source_id"],
            "section_path": list(section_path),
            "page_range": None,
            "heading": source["title"],
            "frontmatter_keys": sorted(metadata.keys()),
        }
    ]

    for block in blocks:
        if block["type"] == "heading":
            _flush_text_buffer(
                source=source,
                buffer_texts=buffer_texts,
                section_path=section_path,
                page_range=None,
                pending_image_ids=pending_image_ids,
                chunk_records=chunk_records,
            )
            section_path = _next_section_path(section_path, int(block["level"]), block["text"])
            section_records.append(
                {
                    "source_id": source["source_id"],
                    "section_path": list(section_path),
                    "page_range": None,
                    "heading": block["text"],
                }
            )
            continue
        if block["type"] == "code":
            _flush_text_buffer(
                source=source,
                buffer_texts=buffer_texts,
                section_path=section_path,
                page_range=None,
                pending_image_ids=pending_image_ids,
                chunk_records=chunk_records,
            )
            chunk_index = len(chunk_records) + 1
            chunk_id = f'{source["source_id"]}#chunk-{chunk_index:04d}'
            text_for_tags = f'{source["title"]}\n{" / ".join(section_path)}\n{block["text"]}'
            image_ids = list(pending_image_ids)
            chunk_records.append(
                {
                    "chunk_id": chunk_id,
                    "source_id": source["source_id"],
                    "title": source["title"],
                    "section_path": list(section_path),
                    "page_range": None,
                    "chunk_type": "code",
                    "software_tags": sorted(set(source.get("software_tags", []) + extract_tags(text_for_tags, SOFTWARE_SYNONYMS))),
                    "method_tags": extract_method_tags(text_for_tags),
                    "topic_tags": sorted(set(source.get("topic_tags", []) + extract_tags(text_for_tags, TOPIC_SYNONYMS))),
                    "authority_level": source["authority_level"],
                    "source_type": source["source_type"],
                    "language": detect_language(text_for_tags),
                    "has_image": bool(image_ids),
                    "image_ids": image_ids,
                    "prev_chunk_id": None,
                    "next_chunk_id": None,
                    "text": block["text"],
                    "snippet": make_snippet(block["text"]),
                    "canonical_path": source["canonical_path"],
                    "canonical_url": source["canonical_url"],
                    "html_path": source.get("html_path"),
                    "dom_anchor": None,
                    "chunk_hash": stable_hash(block["text"]),
                }
            )
            pending_image_ids.clear()
            continue
        if block["type"] == "image":
            image_id = f'{source["source_id"]}#img-{len(image_records) + 1:03d}'
            image_path = (markdown_path.parent / block["path"]).resolve()
            image_records.append(
                {
                    "image_id": image_id,
                    "source_id": source["source_id"],
                    "chunk_id": None,
                    "alt": block["alt"],
                    "caption": block["alt"] or "",
                    "nearby_text": "",
                    "path": to_portable_path(layout, image_path),
                    "relative_path": block["path"],
                    "canonical_url": source["canonical_url"],
                    "section_path": list(section_path),
                    "exists": image_path.exists(),
                }
            )
            pending_image_ids.append(image_id)
            continue
        if block["type"] == "paragraph":
            buffer_texts.append(block["text"])

    _flush_text_buffer(
        source=source,
        buffer_texts=buffer_texts,
        section_path=section_path,
        page_range=None,
        pending_image_ids=pending_image_ids,
        chunk_records=chunk_records,
    )
    _finalize_chunk_links(chunk_records)
    for image in image_records:
        for chunk in chunk_records:
            if image["image_id"] in chunk["image_ids"]:
                image["chunk_id"] = chunk["chunk_id"]
                image["nearby_text"] = make_snippet(chunk["text"], limit=400)
                image["caption"] = image["caption"] or image["nearby_text"]
                break
    return chunk_records, image_records, section_records


def _is_manual_heading(text: str) -> bool:
    """判断 Multiwfn 手册段落是否像小节标题。

    功能目的：
        在 PDF 转 Markdown 的弱结构文本中恢复一部分章节层级。
    输入参数：
        text：手册中的一个段落块。
    返回值：
        像标题返回 True。
    关键流程：
        匹配 `Chapter/Section/Appendix` 开头或较短全大写英文段落。
    可能报错或边界情况：
        手册转写中有大量换行噪声，标题识别保守处理，宁可少识别也不误切太碎。
    """

    stripped = text.strip()
    if not stripped:
        return False
    if re.match(r"^(chapter|section|appendix)\b", stripped, flags=re.IGNORECASE):
        return True
    if len(stripped) <= 80 and stripped == stripped.upper() and any(character.isalpha() for character in stripped):
        return True
    return False


def _normalize_manual_source(
    layout: ProjectLayout,
    source: Dict[str, Any],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """标准化 Multiwfn 用户手册。

    功能目的：
        将 `Multiwfn_manual.md` 按页和段落切分为可检索 chunk。
    输入参数：
        layout：项目目录布局。
        source：source registry 中的 `manual:multiwfn_manual` 记录。
    返回值：
        `(chunks, images, sections)` 三类记录列表；手册图片资源暂不逐图建索引。
    关键流程：
        按 `## Page N` 切页，再按空行切段，识别少量标题并生成 page anchor。
    可能报错或边界情况：
        如果手册 Markdown 不含页标记，会整体作为第 1 页处理。
    """

    manual_path = resolve_portable_path(layout, source["canonical_path"])
    text = manual_path.read_text(encoding="utf-8")
    parts = re.split(r"^## Page (\d+)\s*$", text, flags=re.MULTILINE)
    if len(parts) < 3:
        parts = ["", "1", text]
    chunk_records: List[Dict[str, Any]] = []
    image_records: List[Dict[str, Any]] = []
    section_records: List[Dict[str, Any]] = []

    for index in range(1, len(parts), 2):
        page_number = int(parts[index])
        page_text = parts[index + 1].strip()
        page_heading = f"Page {page_number}"
        section_path: List[str] = [source["title"], page_heading]
        section_records.append(
            {
                "source_id": source["source_id"],
                "section_path": list(section_path),
                "page_range": [page_number, page_number],
                "heading": page_heading,
            }
        )
        blocks = [normalize_whitespace(block) for block in re.split(r"\n\s*\n", page_text) if normalize_whitespace(block)]
        buffer_texts: List[str] = []
        for block in blocks:
            if _is_manual_heading(block):
                _flush_text_buffer(
                    source=source,
                    buffer_texts=buffer_texts,
                    section_path=section_path,
                    page_range=[page_number, page_number],
                    pending_image_ids=[],
                    chunk_records=chunk_records,
                )
                section_path = [source["title"], page_heading, block]
                section_records.append(
                    {
                        "source_id": source["source_id"],
                        "section_path": list(section_path),
                        "page_range": [page_number, page_number],
                        "heading": block,
                    }
                )
                continue
            buffer_texts.append(block)
        _flush_text_buffer(
            source=source,
            buffer_texts=buffer_texts,
            section_path=section_path,
            page_range=[page_number, page_number],
            pending_image_ids=[],
            chunk_records=chunk_records,
        )

    for chunk in chunk_records:
        page_value = chunk["page_range"][0] if chunk["page_range"] else None
        chunk["dom_anchor"] = f"page-{page_value}" if page_value is not None else None
    _finalize_chunk_links(chunk_records)
    return chunk_records, image_records, section_records


def normalize_sources(layout: ProjectLayout) -> Dict[str, int]:
    """标准化全部 Sobko source。

    功能目的：
        生成 MCP 检索需要的 `chunks.jsonl`、`images.jsonl` 和 `sections.jsonl`。
    输入参数：
        layout：项目目录布局。
    返回值：
        包含 source/chunk/image/section 数量的字典。
    关键流程：
        读取 source registry，按 source_type 分发到博客或手册 normalizer，再统一写出 JSONL。
    可能报错或边界情况：
        未知 source_type 会抛出 `ValueError`，防止未来误导入未处理来源。
    """

    sources = read_jsonl(layout.normalized_dir / "source_registry.jsonl")
    all_chunks: List[Dict[str, Any]] = []
    all_images: List[Dict[str, Any]] = []
    all_sections: List[Dict[str, Any]] = []
    for source in sources:
        if source["source_type"] in {"blog_post", "software_doc"}:
            chunks, images, sections = _normalize_blog_source(layout, source)
        elif source["source_type"] == "manual":
            chunks, images, sections = _normalize_manual_source(layout, source)
        else:
            raise ValueError(f"未知 source_type：{source['source_type']}")
        all_chunks.extend(chunks)
        all_images.extend(images)
        all_sections.extend(sections)

    write_jsonl(layout.normalized_dir / "chunks.jsonl", all_chunks)
    write_jsonl(layout.normalized_dir / "images.jsonl", all_images)
    write_jsonl(layout.normalized_dir / "sections.jsonl", all_sections)
    return {
        "source_count": len(sources),
        "chunk_count": len(all_chunks),
        "image_count": len(all_images),
        "section_count": len(all_sections),
    }
