"""构建 Sobko source registry。"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .common import (
    SOFTWARE_TAGS,
    TOPIC_TAGS,
    detect_language,
    extract_tags,
    extract_version_hints,
    read_json,
    read_jsonl,
    stable_hash,
    write_json,
    write_jsonl,
)
from .config import ProjectLayout, RagConfig, resolve_input_path, to_portable_path


def _merge_blog_software_tags(post: Dict[str, Any]) -> List[str]:
    """合并帖子软件标签。

    功能目的：
        将 manifest 中已有分类、关键词和标题摘要统一映射到固定软件标签表。
    输入参数：
        post：`posts_academic.jsonl` 中的一条帖子记录。
    返回值：
        去重排序后的软件标签。
    关键流程：
        优先使用 manifest 中的 source_categories / secondary_topics，再从标题摘要补充推断。
    可能报错或边界情况：
        manifest 个别字段为空时按空列表处理，不影响入库。
    """

    merged: List[str] = []
    for key in ["source_categories", "secondary_topics", "keyword_hints"]:
        merged.extend(post.get(key) or [])
    if post.get("primary_topic"):
        merged.append(post["primary_topic"])
    text = " ".join(str(item) for item in [*merged, post.get("title", ""), post.get("summary", "")])
    inferred = extract_tags(text, {tag: [tag] for tag in SOFTWARE_TAGS})
    merged.extend(inferred)
    return sorted({tag for tag in merged if tag in SOFTWARE_TAGS})


def _merge_blog_topic_tags(post: Dict[str, Any]) -> List[str]:
    """合并帖子主题标签。

    功能目的：
        保留已有高质量分类，同时为查询过滤提供统一主题集合。
    输入参数：
        post：`posts_academic.jsonl` 中的一条帖子记录。
    返回值：
        去重排序后的主题标签。
    关键流程：
        使用 primary_topic、secondary_topics、keyword_hints 和标题摘要共同推断。
    可能报错或边界情况：
        不在固定主题表中的标签会被过滤，避免污染查询接口。
    """

    merged: List[str] = []
    for key in ["secondary_topics", "keyword_hints"]:
        merged.extend(post.get(key) or [])
    if post.get("primary_topic"):
        merged.append(post["primary_topic"])
    text = " ".join(str(item) for item in [*merged, post.get("title", ""), post.get("summary", "")])
    inferred = extract_tags(text, {tag: [tag] for tag in TOPIC_TAGS})
    merged.extend(inferred)
    return sorted({tag for tag in merged if tag in TOPIC_TAGS})


def _count_asset_images(root: Path) -> int:
    """统计目录中的图片资源数。

    功能目的：
        给手册 source 记录提供资源规模信息。
    输入参数：
        root：待扫描目录。
    返回值：
        图片文件数量。
    关键流程：
        递归统计常见图片后缀。
    可能报错或边界情况：
        目录不存在时返回 0，便于在缺少可选资源时仍能构建文本索引。
    """

    if not root.exists():
        return 0
    image_suffixes = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
    return sum(1 for path in root.rglob("*") if path.is_file() and path.suffix.lower() in image_suffixes)


def build_source_registry(layout: ProjectLayout, config: RagConfig) -> List[Dict[str, Any]]:
    """构建 Sobko source registry。

    功能目的：
        把项目内 source snapshot 转成统一 source 记录，供 normalizer 和 MCP trace 使用。
    输入参数：
        layout：项目目录布局。
        config：运行配置。
    返回值：
        source 记录列表。
    关键流程：
        1. 读取 577 篇学术帖 manifest。
        2. 将每篇帖子映射为 `blog_post:<post_id>`。
        3. 将 Multiwfn 手册映射为唯一的 `manual:multiwfn_manual`。
        4. 写出 `normalized/source_registry.jsonl` 和迁移用 snapshot manifest。
    可能报错或边界情况：
        关键文件缺失时直接抛出 `FileNotFoundError`，避免生成不完整知识库。
    """

    posts_manifest_path = resolve_input_path(layout, config.posts_manifest_path)
    posts_root_path = resolve_input_path(layout, config.posts_root_path)
    manual_root_path = resolve_input_path(layout, config.manual_root_path)
    manual_md_path = resolve_input_path(layout, config.manual_markdown_path)
    manual_html_path = resolve_input_path(layout, config.manual_html_path)
    manual_manifest_path = resolve_input_path(layout, config.manual_manifest_path)

    required_paths = [posts_manifest_path, posts_root_path, manual_md_path, manual_html_path, manual_manifest_path]
    for path in required_paths:
        if not path.exists():
            raise FileNotFoundError(f"知识源路径不存在：{path}")

    build_time = datetime.now().astimezone().isoformat()
    posts = read_jsonl(posts_manifest_path)
    records: List[Dict[str, Any]] = []

    for post in posts:
        canonical_path = (posts_root_path / post["academic_markdown_path"]).resolve()
        if not canonical_path.exists():
            raise FileNotFoundError(f"学术帖 Markdown 不存在：{canonical_path}")
        post_text = canonical_path.read_text(encoding="utf-8")
        summary_text = f'{post.get("title", "")}\n{post.get("summary", "")}'
        canonical_portable_path = to_portable_path(layout, canonical_path)
        records.append(
            {
                "source_id": f'blog_post:{post["post_id"]}',
                "source_type": "blog_post",
                "title": post.get("title", ""),
                "canonical_path": canonical_portable_path,
                "canonical_url": post.get("url", ""),
                "authority_level": config.blog_authority_level,
                "date": post.get("date"),
                "software_tags": _merge_blog_software_tags(post),
                "topic_tags": _merge_blog_topic_tags(post),
                "image_count": int(post.get("image_count", 0)),
                "version_hint": extract_version_hints(summary_text),
                "language": detect_language(summary_text),
                "index_version": config.index_version,
                "raw_markdown_path": canonical_portable_path,
                "raw_post_dir": to_portable_path(layout, canonical_path.parent),
                "post_id": post["post_id"],
                "classification_reason": post.get("classification_reason", ""),
                "confidence": post.get("confidence"),
                "source_hash": stable_hash(post_text[:20000]),
            }
        )

    manual_text = manual_md_path.read_text(encoding="utf-8")
    manual_manifest = read_json(manual_manifest_path)
    manual_image_count = 0
    for dirname in ["Multiwfn_manual_files", "res", "extrafiles"]:
        manual_image_count += _count_asset_images(manual_root_path / dirname)
    records.append(
        {
            "source_id": "manual:multiwfn_manual",
            "source_type": "manual",
            "title": "Multiwfn 用户手册",
            "canonical_path": to_portable_path(layout, manual_md_path),
            "canonical_url": manual_manifest.get("url", "http://sobereva.com/multiwfn/Multiwfn_manual.html"),
            "authority_level": config.manual_authority_level,
            "date": manual_manifest.get("fetched_at"),
            "software_tags": ["Multiwfn"],
            "topic_tags": ["波函数分析", "量子化学", "综述/教程/投稿经验"],
            "image_count": manual_image_count,
            "version_hint": extract_version_hints(manual_text[:4000]),
            "language": detect_language(manual_text[:4000]),
            "index_version": config.index_version,
            "html_path": to_portable_path(layout, manual_html_path),
            "manual_root_path": to_portable_path(layout, manual_root_path),
            "manifest_path": to_portable_path(layout, manual_manifest_path),
            "source_hash": stable_hash(manual_text[:20000]),
        }
    )

    write_jsonl(layout.normalized_dir / "source_registry.jsonl", records)
    write_json(
        layout.data_sources_dir / "source_registry_snapshot.json",
        {
            "project": config.project_name,
            "index_version": config.index_version,
            "generated_at": build_time,
            "source_count": len(records),
            "source_type_counts": {
                "blog_post": sum(1 for item in records if item["source_type"] == "blog_post"),
                "manual": sum(1 for item in records if item["source_type"] == "manual"),
            },
            "source_ids": [item["source_id"] for item in records],
        },
    )
    return records
