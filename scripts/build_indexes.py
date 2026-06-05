#!/usr/bin/env python
"""构建 BM25、dense embedding 分片与图片查找索引。"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sobko_mcp.common import read_jsonl, tokenize, write_json
from sobko_mcp.config import build_layout, ensure_project_dirs, load_config
from sobko_mcp.retriever import OllamaClient


def build_lexical_index(chunks: List[Dict[str, Any]], output_path: Path) -> Dict[str, Any]:
    """构建 BM25 词法索引。

    功能目的：
        提供无需 embedding 后端也可工作的基础检索能力。
    输入参数：
        chunks：标准化 chunk 列表。
        output_path：索引 JSON 输出路径。
    返回值：
        BM25 索引 payload。
    关键流程：
        对标题、小节路径和正文分词，统计每个 chunk 的 term frequency 和全局 document frequency。
    可能报错或边界情况：
        chunk 列表为空时仍写出合法空索引，但后续检索不会有结果。
    """

    doc_freqs: Counter[str] = Counter()
    doc_stats: Dict[str, Dict[str, Any]] = {}
    total_length = 0
    for chunk in chunks:
        tokens = tokenize(f'{chunk["title"]}\n{" / ".join(chunk["section_path"])}\n{chunk["text"]}')
        term_freqs = Counter(tokens)
        total_length += len(tokens)
        doc_stats[chunk["chunk_id"]] = {
            "length": len(tokens),
            "term_freqs": dict(term_freqs),
        }
        for token in term_freqs:
            doc_freqs[token] += 1
    payload = {
        "doc_count": len(chunks),
        "avg_doc_len": total_length / max(len(chunks), 1),
        "doc_freqs": dict(doc_freqs),
        "doc_stats": doc_stats,
    }
    write_json(output_path, payload)
    return payload


def _clear_dense_shards(shards_dir: Path) -> None:
    """清理旧 dense 分片。

    功能目的：
        防止新索引构建后残留旧 shard 文件造成迁移包混乱。
    输入参数：
        shards_dir：dense shard 目录。
    返回值：
        无。
    关键流程：
        只删除本脚本命名规则下的 `chunk_embeddings_*.jsonl`。
    可能报错或边界情况：
        目录不存在时会先创建。
    """

    shards_dir.mkdir(parents=True, exist_ok=True)
    for path in shards_dir.glob("chunk_embeddings_*.jsonl"):
        path.unlink()


def _write_dense_shards(
    *,
    layout,
    chunk_ids: List[str],
    vectors: Dict[str, List[float]],
    max_bytes: int,
) -> List[Dict[str, Any]]:
    """写入 dense embedding JSONL 分片。

    功能目的：
        把完整 dense 索引拆成小于 GitHub 单文件限制的多个 shard。
    输入参数：
        layout：项目目录布局。
        chunk_ids：按构建顺序排列的 chunk ID。
        vectors：`chunk_id -> vector` 映射。
        max_bytes：单个 shard 的目标最大字节数。
    返回值：
        shard metadata 列表。
    关键流程：
        逐条生成紧凑 JSON 行，累计字节数接近阈值时切换到新 shard。
    可能报错或边界情况：
        单条向量如果超过 max_bytes，会单独占一个 shard；当前 bge-m3 向量远小于阈值。
    """

    _clear_dense_shards(layout.dense_shards_dir)
    shards: List[Dict[str, Any]] = []
    shard_index = 1
    current_lines: List[bytes] = []
    current_bytes = 0
    current_count = 0

    def flush() -> None:
        nonlocal shard_index, current_lines, current_bytes, current_count
        if not current_lines:
            return
        filename = f"chunk_embeddings_{shard_index:04d}.jsonl"
        path = layout.dense_shards_dir / filename
        with path.open("wb") as handle:
            for line in current_lines:
                handle.write(line)
        shards.append(
            {
                "path": f"shards/{filename}",
                "record_count": current_count,
                "bytes": path.stat().st_size,
            }
        )
        shard_index += 1
        current_lines = []
        current_bytes = 0
        current_count = 0

    for chunk_id in chunk_ids:
        vector = vectors.get(chunk_id)
        if vector is None:
            continue
        line = (json.dumps({"chunk_id": chunk_id, "vector": vector}, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        if current_lines and current_bytes + len(line) > max_bytes:
            flush()
        current_lines.append(line)
        current_bytes += len(line)
        current_count += 1
    flush()
    return shards


def _write_dense_unavailable(layout, config, reason: str) -> Dict[str, Any]:
    """写入 dense 不可用状态。

    功能目的：
        当 embedding API 不可用时仍保留可审计状态文件，并允许 BM25 降级检索。
    输入参数：
        layout：项目目录布局。
        config：运行配置。
        reason：不可用原因。
    返回值：
        status payload。
    关键流程：
        同时写 `status.json` 和 `metadata.json`，二者均标记 available=false。
    可能报错或边界情况：
        不删除旧 shard，但 metadata=false 会阻止检索层加载旧向量。
    """

    status = {
        "available": False,
        "reason": reason,
        "model_name": config.embedding_model,
        "generated_at": datetime.now().astimezone().isoformat(),
        "provider": config.embedding_provider,
    }
    write_json(layout.dense_dir / "status.json", status)
    write_json(layout.dense_dir / "metadata.json", status | {"shards": [], "vector_count": 0, "dimension": 0})
    return status


def build_dense_index(chunks: List[Dict[str, Any]], config, layout) -> Dict[str, Any]:
    """构建 dense embedding 索引。

    功能目的：
        使用配置的 embedding API 为全部 chunk 生成向量，并写为分片索引。
    输入参数：
        chunks：标准化 chunk 列表。
        config：运行配置。
        layout：项目目录布局。
    返回值：
        dense metadata 或 unavailable status。
    关键流程：
        ping embedding API -> 分 batch 获取向量 -> 写 shard -> 写 metadata/status。
    可能报错或边界情况：
        API 不可用或某批 embedding 失败时不会中断整体索引构建，而是写出 unavailable 状态。
    """

    if not config.rag_use_embedding:
        return _write_dense_unavailable(layout, config, "rag_use_embedding=false")

    client = OllamaClient(config)
    ok, reason = client.embedding_available()
    if not ok:
        return _write_dense_unavailable(layout, config, reason)

    texts = [f'{chunk["title"]}\n{" / ".join(chunk["section_path"])}\n{chunk["text"]}' for chunk in chunks]
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    vectors: Dict[str, List[float]] = {}
    try:
        for start in range(0, len(texts), config.dense_batch_size):
            batch_texts = texts[start : start + config.dense_batch_size]
            batch_ids = chunk_ids[start : start + config.dense_batch_size]
            embeddings = client.embed_texts(batch_texts)
            if len(embeddings) != len(batch_ids):
                raise RuntimeError(f"embedding 返回条数不匹配：expected={len(batch_ids)} actual={len(embeddings)}")
            for chunk_id, vector in zip(batch_ids, embeddings):
                vectors[chunk_id] = vector
            if start and start % (config.dense_batch_size * 20) == 0:
                print(f"dense_progress={len(vectors)}/{len(chunks)}")
    except Exception as exc:
        return _write_dense_unavailable(layout, config, str(exc))

    dimension = len(next(iter(vectors.values()))) if vectors else 0
    shards = _write_dense_shards(
        layout=layout,
        chunk_ids=chunk_ids,
        vectors=vectors,
        max_bytes=max(1_000_000, int(config.dense_shard_max_bytes)),
    )
    metadata = {
        "available": True,
        "provider": client._embedding_provider(),
        "model_name": client._embedding_model(),
        "dimension": dimension,
        "generated_at": datetime.now().astimezone().isoformat(),
        "vector_count": len(vectors),
        "shard_count": len(shards),
        "shards": shards,
    }
    write_json(layout.dense_dir / "metadata.json", metadata)
    write_json(layout.dense_dir / "status.json", metadata | {"shards": None})
    return metadata


def build_image_lookup(images: List[Dict[str, Any]], output_path: Path) -> Dict[str, Any]:
    """构建图片查找表。

    功能目的：
        支持 `sobko_get_image` 通过 image_id 快速定位图片路径和邻近文本。
    输入参数：
        images：标准化图片记录。
        output_path：输出 JSON 路径。
    返回值：
        `image_id -> image record` 映射。
    关键流程：
        直接按 image_id 建字典并写出 JSON。
    可能报错或边界情况：
        图片记录为空时写出空对象。
    """

    payload = {image["image_id"]: image for image in images}
    write_json(output_path, payload)
    return payload


def main() -> None:
    """脚本入口。

    功能目的：
        构建 Sobko 的 BM25、dense、image lookup 与 build manifest。
    输入参数：
        无，使用项目默认配置。
    返回值：
        无，向 stdout 打印 build manifest。
    关键流程：
        读取 normalized 数据 -> 构建索引 -> 写 metadata。
    可能报错或边界情况：
        normalized 数据缺失时抛出文件错误；embedding 失败时降级但不阻断 BM25 索引。
    """

    layout = build_layout(PROJECT_ROOT)
    ensure_project_dirs(layout)
    config = load_config(layout.configs_dir / "default.json")
    chunks = read_jsonl(layout.normalized_dir / "chunks.jsonl")
    images = read_jsonl(layout.normalized_dir / "images.jsonl")

    lexical = build_lexical_index(chunks, layout.bm25_dir / "lexical_index.json")
    dense = build_dense_index(chunks, config, layout)
    image_lookup = build_image_lookup(images, layout.image_refs_dir / "image_lookup.json")

    build_manifest = {
        "index_version": config.index_version,
        "generated_at": datetime.now().astimezone().isoformat(),
        "chunk_count": len(chunks),
        "image_count": len(images),
        "bm25_doc_count": lexical["doc_count"],
        "dense_available": bool(dense.get("available")),
        "dense_reason": dense.get("reason"),
        "dense_vector_count": dense.get("vector_count", 0),
        "dense_shard_count": dense.get("shard_count", 0),
        "image_lookup_count": len(image_lookup),
        "rerank_enabled": bool(config.rag_use_reranker),
        "rerank_model_name": config.rerank_model,
    }
    write_json(layout.metadata_dir / "build_manifest.json", build_manifest)
    write_json(layout.metadata_dir / "index_version.json", {"index_version": config.index_version})
    feedback_path = layout.metadata_dir / "feedback.jsonl"
    feedback_path.touch(exist_ok=True)
    print(build_manifest)


if __name__ == "__main__":
    main()
