#!/usr/bin/env python
"""构建 BM25、dense embedding 二进制索引与图片查找索引。"""

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
from sobko_mcp.embedding_cache import (
    build_embedding_cache_config,
    embedding_cache_key,
    load_reusable_embedding_vectors,
    previous_dense_metadata,
    previous_dimension_for_cache,
)
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
    """清理旧 dense JSONL 分片。

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


def _clear_dense_binary(dense_dir: Path) -> None:
    """清理旧 dense 二进制产物。"""

    for filename in ["vectors.f32", "chunk_records.json"]:
        path = dense_dir / filename
        if path.exists():
            path.unlink()


def _write_dense_binary(
    *,
    layout,
    chunks: List[Dict[str, Any]],
    vectors: Dict[str, List[float]],
    cache_config: Dict[str, Any],
    dimension: int,
) -> Dict[str, Any]:
    """写入 dense embedding 二进制矩阵。

    功能目的：
        用 float32 行主序矩阵替代 JSONL 分片，显著减少 MCP 进程查询时的 Python 对象内存。
    输入参数：
        layout：项目目录布局。
        chunks：按构建顺序排列的 chunk 记录。
        vectors：`chunk_id -> vector` 映射。
        cache_config：当前 embedding vector-space fingerprint。
        dimension：embedding 维度。
    返回值：
        binary metadata。
    关键流程：
        写 `vectors.f32` 连续矩阵，再写 `chunk_records.json` 保存行号到 chunk/cache key 的映射。
    可能报错或边界情况：
        numpy 不可导入时抛出明确错误；上层会将 dense 标为不可用。
    """

    import numpy as np

    layout.dense_dir.mkdir(parents=True, exist_ok=True)
    _clear_dense_shards(layout.dense_shards_dir)
    _clear_dense_binary(layout.dense_dir)

    ordered_chunks = [chunk for chunk in chunks if chunk["chunk_id"] in vectors]
    matrix = np.empty((len(ordered_chunks), dimension), dtype="<f4")
    records: List[Dict[str, Any]] = []

    for row_index, chunk in enumerate(ordered_chunks):
        chunk_id = chunk["chunk_id"]
        vector = vectors[chunk_id]
        if len(vector) != dimension:
            raise RuntimeError(f"embedding 维度不一致：chunk_id={chunk_id} expected={dimension} actual={len(vector)}")
        matrix[row_index, :] = np.asarray(vector, dtype="<f4")
        chunk_hash = str(chunk.get("chunk_hash") or "")
        records.append(
            {
                "row": row_index,
                "chunk_id": chunk_id,
                "chunk_hash": chunk_hash,
                "cache_key": embedding_cache_key(chunk_hash, cache_config) if chunk_hash else None,
            }
        )

    vectors_path = layout.dense_dir / "vectors.f32"
    records_path = layout.dense_dir / "chunk_records.json"
    with vectors_path.open("wb") as handle:
        matrix.tofile(handle)
    write_json(
        records_path,
        {
            "format": "chunk_records_v1",
            "vector_count": len(records),
            "dimension": dimension,
            "records": records,
        },
    )
    return {
        "format": "f32_row_major_v1",
        "vectors_path": vectors_path.name,
        "records_path": records_path.name,
        "dtype": "float32",
        "byte_order": "little",
        "shape": [len(records), dimension],
        "bytes": vectors_path.stat().st_size,
    }


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
        使用配置的 embedding API 为全部 chunk 生成向量，并写为二进制矩阵索引。
    输入参数：
        chunks：标准化 chunk 列表。
        config：运行配置。
        layout：项目目录布局。
    返回值：
        dense metadata 或 unavailable status。
    关键流程：
        ping embedding API -> 分 batch 获取向量 -> 写 binary -> 写 metadata/status。
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
    provider = client._embedding_provider()
    model_name = client._embedding_model()
    previous_metadata = previous_dense_metadata(layout)
    previous_dimension = previous_dimension_for_cache(
        metadata=previous_metadata,
        provider=provider,
        model_name=model_name,
    )
    cache_config = build_embedding_cache_config(
        config=config,
        provider=provider,
        model_name=model_name,
        dimension=previous_dimension or config.embedding_dimensions,
    )
    reusable_vectors = load_reusable_embedding_vectors(
        layout=layout,
        chunks=chunks,
        cache_config=cache_config,
        metadata=previous_metadata,
    )
    missing_indexes: List[int] = []
    cache_hits = 0
    cache_misses = 0
    for index, chunk in enumerate(chunks):
        chunk_hash = str(chunk.get("chunk_hash") or "")
        cache_key = embedding_cache_key(chunk_hash, cache_config) if chunk_hash else ""
        cached_vector = reusable_vectors.get(cache_key)
        if cached_vector is not None:
            vectors[chunk["chunk_id"]] = cached_vector
            cache_hits += 1
        else:
            missing_indexes.append(index)
            cache_misses += 1
    try:
        for start in range(0, len(missing_indexes), config.dense_batch_size):
            batch_indexes = missing_indexes[start : start + config.dense_batch_size]
            batch_texts = [texts[index] for index in batch_indexes]
            batch_ids = [chunk_ids[index] for index in batch_indexes]
            embeddings = client.embed_texts(batch_texts)
            if len(embeddings) != len(batch_ids):
                raise RuntimeError(f"embedding 返回条数不匹配：expected={len(batch_ids)} actual={len(embeddings)}")
            for chunk_id, vector in zip(batch_ids, embeddings):
                vectors[chunk_id] = vector
            if start and start % (config.dense_batch_size * 20) == 0:
                print(f"dense_progress={len(vectors)}/{len(chunks)} cache_hits={cache_hits} computed={len(vectors) - cache_hits}")
    except Exception as exc:
        return _write_dense_unavailable(layout, config, str(exc))

    dimension = len(next(iter(vectors.values()))) if vectors else 0
    final_cache_config = build_embedding_cache_config(
        config=config,
        provider=provider,
        model_name=model_name,
        dimension=dimension or previous_dimension or config.embedding_dimensions,
    )
    binary = _write_dense_binary(
        layout=layout,
        chunks=chunks,
        vectors=vectors,
        cache_config=final_cache_config,
        dimension=dimension,
    )
    metadata = {
        "available": True,
        "provider": provider,
        "model_name": model_name,
        "dimension": dimension,
        "generated_at": datetime.now().astimezone().isoformat(),
        "vector_count": len(vectors),
        "format": "binary_f32_v1",
        "binary": binary,
        "shard_count": 0,
        "embedding_cache_config": final_cache_config,
        "cache_stats": {
            "reused": cache_hits,
            "computed": cache_misses,
            "total": len(chunks),
        },
        "shards": [],
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
