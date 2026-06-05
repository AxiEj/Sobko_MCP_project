"""Sobko 基础流水线测试。"""

from __future__ import annotations

import os
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from sobko_mcp.config import ProjectLayout, build_layout, load_config
from sobko_mcp.embedding_cache import (
    build_embedding_cache_config,
    embedding_cache_key,
    load_reusable_embedding_vectors,
)
from sobko_mcp.retriever import OllamaClient, RetrievalEngine


class PipelineSmokeTests(unittest.TestCase):
    """验证构建产物与核心检索行为。"""

    @classmethod
    def setUpClass(cls) -> None:
        """加载检索引擎。

        功能目的：
            在所有测试间复用同一个 RetrievalEngine，减少索引加载成本。
        输入参数：
            无。
        返回值：
            无。
        关键流程：
            默认关闭 embedding/rerank，单元测试优先覆盖可离线 BM25 路径。
        可能报错或边界情况：
            如果构建产物缺失，engine 初始化会失败，提示先运行构建脚本。
        """

        os.environ["SOBKO_DISABLE_LOCAL_RERANKER"] = "1"
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.layout = build_layout(cls.project_root)
        cls.config = load_config(cls.layout.configs_dir / "default.json")
        cls.config.rag_use_embedding = False
        cls.config.rag_use_reranker = False
        cls.engine = RetrievalEngine(cls.layout, cls.config)

    def test_registry_count(self) -> None:
        """source registry 应只包含学术帖和 Multiwfn 手册。"""

        counts = Counter(source["source_type"] for source in self.engine.sources)
        self.assertEqual(counts["blog_post"], 580)
        self.assertEqual(counts["manual"], 1)
        self.assertEqual(len(self.engine.sources), 581)

    def test_chunk_and_image_counts(self) -> None:
        """标准化产物规模应符合完整迁移包预期。"""

        self.assertGreater(len(self.engine.chunks), 10000)
        self.assertGreater(len(self.engine.images), 2000)

    def test_known_orca_tddft_post_search(self) -> None:
        """ORCA TDDFT 空穴电子分析 query 应命中帖子 758。"""

        result = self.engine.search(query="ORCA TDDFT 空穴电子分析", top_k=5)
        self.assertTrue(any(item["source_id"] == "blog_post:758" for item in result.results))

    def test_known_manual_search(self) -> None:
        """Multiwfn command-line mode query 应命中手册 source。"""

        result = self.engine.search(query="Multiwfn command-line mode", top_k=5)
        self.assertTrue(any(item["source_id"] == "manual:multiwfn_manual" for item in result.results))

    def test_rerank_unavailable_records_warning(self) -> None:
        """rerank API 不可用时应降级并返回 warning。"""

        self.config.rag_use_reranker = True
        self.config.rerank_api_base_url = "http://127.0.0.1:9"
        self.config.rerank_fallback_base_urls = []
        self.engine.ollama_client._rerank_ping_status = None
        self.engine.ollama_client._rerank_base_url = None
        result = self.engine.search(query="ORCA TDDFT 空穴电子分析", top_k=2)
        self.assertTrue(result.results)
        self.assertTrue(any(item.startswith("rerank_fallback:") for item in result.backend_warnings))
        self.config.rag_use_reranker = False

    def test_openai_embedding_response_parsing(self) -> None:
        """OpenAI embeddings 响应应按 index 还原成输入顺序。"""

        config = load_config(self.layout.configs_dir / "default.json")
        config.embedding_provider = "openai"
        config.embedding_model = "text-embedding-3-small"
        config.embedding_dimensions = 3
        client = OllamaClient(config)

        def fake_post(payload):
            self.assertEqual(payload["model"], "text-embedding-3-small")
            self.assertEqual(payload["dimensions"], 3)
            return {
                "data": [
                    {"index": 1, "embedding": [0.2, 0.3, 0.4]},
                    {"index": 0, "embedding": [0.1, 0.2, 0.3]},
                ]
            }

        client._post_openai_embeddings = fake_post
        self.assertEqual(
            client.embed_texts(["first", "second"]),
            [[0.1, 0.2, 0.3], [0.2, 0.3, 0.4]],
        )

    def test_embedding_provider_mismatch_degrades_to_lexical(self) -> None:
        """当前配置和 dense 索引 provider 不一致时不得混用向量空间。"""

        old_use_embedding = self.config.rag_use_embedding
        old_provider = self.config.embedding_provider
        old_model = self.config.embedding_model
        try:
            self.config.rag_use_embedding = True
            self.config.embedding_provider = "openai"
            self.config.embedding_model = "text-embedding-3-small"
            result = self.engine.search(query="ORCA TDDFT 空穴电子分析", top_k=2)
            self.assertEqual(result.effective_mode, "lexical_only")
            self.assertTrue(any("provider=" in item and "不一致" in item for item in result.backend_warnings))
        finally:
            self.config.rag_use_embedding = old_use_embedding
            self.config.embedding_provider = old_provider
            self.config.embedding_model = old_model

    def test_embedding_daemon_is_preferred_for_local_hf(self) -> None:
        """local_hf 查询应优先走共享 daemon，避免 MCP 进程重复加载模型。"""

        config = load_config(self.layout.configs_dir / "default.json")
        config.embedding_provider = "local_hf"
        config.embedding_daemon_enabled = True
        client = OllamaClient(config)

        def fake_post(texts, model_name):
            self.assertEqual(list(texts), ["query"])
            self.assertEqual(model_name, "fake-model")
            return [[0.1, 0.2, 0.3]]

        client._post_daemon_embeddings = fake_post
        self.assertEqual(client.embed_texts(["query"], model="fake-model"), [[0.1, 0.2, 0.3]])
        self.assertIsNone(client._local_embedding_model)

    def test_embedding_cache_key_includes_chunk_hash(self) -> None:
        """chunk_hash 变化必须导致增量缓存失效。"""

        config = load_config(self.layout.configs_dir / "default.json")
        cache_config = build_embedding_cache_config(
            config=config,
            provider="local_hf",
            model_name="BAAI/bge-m3",
            dimension=1024,
        )
        self.assertNotEqual(
            embedding_cache_key("hash-a", cache_config),
            embedding_cache_key("hash-b", cache_config),
        )

    def test_legacy_dense_shard_can_seed_incremental_cache(self) -> None:
        """旧 shard 无 cache_key 时，也能按 chunk_id+chunk_hash 安全初始化缓存。"""

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            dense_dir = root / "indexes" / "dense"
            shards_dir = dense_dir / "shards"
            shards_dir.mkdir(parents=True)
            (dense_dir / "metadata.json").write_text(
                """{
  "available": true,
  "provider": "local_hf",
  "model_name": "BAAI/bge-m3",
  "dimension": 3,
  "shards": [{"path": "shards/chunk_embeddings_0001.jsonl"}]
}""",
                encoding="utf-8",
            )
            (shards_dir / "chunk_embeddings_0001.jsonl").write_text(
                '{"chunk_id":"chunk-1","vector":[1.0,0.0,0.0]}\n',
                encoding="utf-8",
            )
            layout = ProjectLayout(
                root=root,
                configs_dir=root / "configs",
                data_sources_dir=root / "data_sources",
                normalized_dir=root / "normalized",
                indexes_dir=root / "indexes",
                bm25_dir=root / "indexes" / "bm25",
                dense_dir=dense_dir,
                dense_shards_dir=shards_dir,
                image_refs_dir=root / "indexes" / "image_refs",
                rerank_cache_dir=root / "indexes" / "rerank_cache",
                metadata_dir=root / "metadata",
                reports_dir=root / "metadata" / "reports",
                scripts_dir=root / "scripts",
                tests_dir=root / "tests",
                docs_dir=root / "docs",
                server_dir=root / "server",
                skills_dir=root / "skills",
            )
            config = load_config(self.layout.configs_dir / "default.json")
            cache_config = build_embedding_cache_config(
                config=config,
                provider="local_hf",
                model_name="BAAI/bge-m3",
                dimension=3,
            )
            cache = load_reusable_embedding_vectors(
                layout=layout,
                chunks=[{"chunk_id": "chunk-1", "chunk_hash": "hash-1"}],
                cache_config=cache_config,
            )
            self.assertEqual(cache[embedding_cache_key("hash-1", cache_config)], [1.0, 0.0, 0.0])


if __name__ == "__main__":
    unittest.main()
