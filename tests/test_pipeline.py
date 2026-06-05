"""Sobko 基础流水线测试。"""

from __future__ import annotations

import os
import unittest
from collections import Counter
from pathlib import Path

from sobko_mcp.config import build_layout, load_config
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
        self.assertEqual(counts["blog_post"], 577)
        self.assertEqual(counts["manual"], 1)
        self.assertEqual(len(self.engine.sources), 578)

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


if __name__ == "__main__":
    unittest.main()
