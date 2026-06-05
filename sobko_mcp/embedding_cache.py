"""Embedding cache helpers for Sobko dense index builds."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .common import read_json, stable_hash
from .config import ProjectLayout, RagConfig

CACHE_FORMAT_VERSION = 1


def build_embedding_cache_config(
    *,
    config: RagConfig,
    provider: str,
    model_name: str,
    dimension: Optional[int],
) -> Dict[str, Any]:
    """Return the vector-space fingerprint used for incremental reuse.

    The user-visible key is based on chunk hash, provider, model and dimension;
    this helper deliberately includes local encoder options too, because pooling
    or max-length changes also change the vector space.
    """

    env_max_length = os.environ.get("SOBKO_LOCAL_EMBEDDING_MAX_LENGTH")
    max_length: Optional[int]
    if env_max_length:
        max_length = int(env_max_length)
    else:
        max_length = config.local_embedding_max_length
    return {
        "cache_format_version": CACHE_FORMAT_VERSION,
        "provider": provider.strip().lower(),
        "model_name": model_name,
        "dimension": int(dimension) if dimension is not None else None,
        "requested_dimensions": config.embedding_dimensions,
        "local_embedding_max_length": max_length,
        "pooling_strategy": os.environ.get("SOBKO_LOCAL_EMBEDDING_POOLING", "cls").strip().lower(),
        "normalize_embeddings": True,
        "encoder_revision": os.environ.get("SOBKO_EMBEDDING_MODEL_REVISION", ""),
    }


def embedding_cache_key(chunk_hash: str, cache_config: Dict[str, Any]) -> str:
    """Build a stable cache key for one chunk in one embedding vector space."""

    payload = {"chunk_hash": chunk_hash, "embedding": cache_config}
    return stable_hash(json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")))


def _compatible_legacy_metadata(metadata: Dict[str, Any], cache_config: Dict[str, Any]) -> bool:
    """Check whether old shard records without cache_key can be safely reused."""

    if not metadata.get("available"):
        return False
    if str(metadata.get("provider") or "").strip().lower() != str(cache_config.get("provider") or "").strip().lower():
        return False
    if str(metadata.get("model_name") or "").strip() != str(cache_config.get("model_name") or "").strip():
        return False
    metadata_dimension = metadata.get("dimension")
    cache_dimension = cache_config.get("dimension")
    if metadata_dimension and cache_dimension and int(metadata_dimension) != int(cache_dimension):
        return False
    return True


def _iter_previous_dense_records(layout: ProjectLayout, metadata: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """Yield records from the previous dense index, preferring binary metadata."""

    binary = metadata.get("binary")
    if isinstance(binary, dict) and binary.get("vectors_path") and binary.get("records_path"):
        yield from _iter_previous_binary_records(layout, binary)
        return

    for shard in metadata.get("shards", []) or []:
        shard_path = layout.dense_dir / shard["path"]
        if not shard_path.exists():
            continue
        with shard_path.open("r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                yield json.loads(line)


def _iter_previous_binary_records(layout: ProjectLayout, binary: Dict[str, Any]) -> Iterable[Dict[str, Any]]:
    """Yield cache records from a previous float32 binary dense index."""

    import numpy as np

    records_path = layout.dense_dir / str(binary["records_path"])
    vectors_path = layout.dense_dir / str(binary["vectors_path"])
    if not records_path.exists() or not vectors_path.exists():
        return
    payload = read_json(records_path)
    records = payload.get("records") if isinstance(payload, dict) else payload
    if not isinstance(records, list):
        return
    payload_dimension = payload.get("dimension") if isinstance(payload, dict) else None
    shape = binary.get("shape") or [len(records), payload_dimension]
    if not isinstance(shape, list) or len(shape) != 2:
        return
    row_count = int(shape[0])
    dimension = int(shape[1])
    matrix = np.memmap(vectors_path, dtype="<f4", mode="r", shape=(row_count, dimension))
    for record in records:
        row_index = int(record.get("row", -1))
        if row_index < 0 or row_index >= row_count:
            continue
        yield {
            "chunk_id": record.get("chunk_id"),
            "chunk_hash": record.get("chunk_hash"),
            "cache_key": record.get("cache_key"),
            "vector": matrix[row_index].astype(float).tolist(),
        }


def previous_dense_metadata(layout: ProjectLayout) -> Dict[str, Any]:
    """Read previous dense metadata if present."""

    metadata_path = layout.dense_dir / "metadata.json"
    if not metadata_path.exists():
        return {}
    try:
        return read_json(metadata_path)
    except Exception:
        return {}


def previous_dimension_for_cache(
    *,
    metadata: Dict[str, Any],
    provider: str,
    model_name: str,
) -> Optional[int]:
    """Return the previous actual dimension when it belongs to this vector space."""

    if not metadata.get("available"):
        return None
    if str(metadata.get("provider") or "").strip().lower() != provider.strip().lower():
        return None
    if str(metadata.get("model_name") or "").strip() != model_name.strip():
        return None
    dimension = metadata.get("dimension")
    return int(dimension) if dimension else None


def load_reusable_embedding_vectors(
    *,
    layout: ProjectLayout,
    chunks: List[Dict[str, Any]],
    cache_config: Dict[str, Any],
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, List[float]]:
    """Load reusable vectors from the previous dense index.

    New shard records contain ``cache_key`` and can be reused even if chunk IDs
    shift. Legacy shard records can still seed the cache on the first upgraded
    build when provider/model/dimension match and the current chunk_id still
    points at the same chunk hash.
    """

    metadata = metadata if metadata is not None else previous_dense_metadata(layout)
    if not metadata:
        return {}
    chunks_by_id = {chunk["chunk_id"]: chunk for chunk in chunks}
    reusable: Dict[str, List[float]] = {}
    legacy_compatible = _compatible_legacy_metadata(metadata, cache_config)
    for record in _iter_previous_dense_records(layout, metadata):
        vector = record.get("vector")
        if not isinstance(vector, list):
            continue
        record_key = record.get("cache_key")
        if isinstance(record_key, str) and record_key:
            reusable[record_key] = vector
            continue
        if not legacy_compatible:
            continue
        chunk = chunks_by_id.get(str(record.get("chunk_id")))
        if not chunk:
            continue
        chunk_hash = chunk.get("chunk_hash")
        if not chunk_hash:
            continue
        reusable[embedding_cache_key(str(chunk_hash), cache_config)] = vector
    return reusable
