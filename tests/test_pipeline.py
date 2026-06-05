"""Sobko 基础流水线测试。"""

from __future__ import annotations

import json
import os
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from sobko_mcp.common import SOFTWARE_TAGS, TOPIC_TAGS
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
        """source registry 应包含博客、手册、软件文档和论坛帖。"""

        counts = Counter(source["source_type"] for source in self.engine.sources)
        self.assertEqual(counts["blog_post"], 580)
        self.assertEqual(counts["manual"], 1)
        self.assertEqual(counts["software_doc"], 1)
        self.assertEqual(counts["forum_thread"], 35)
        self.assertEqual(len(self.engine.sources), 617)

    def test_all_manifest_forum_threads_are_registered(self) -> None:
        """论坛 manifest 中的帖子必须全部进入 source registry。"""

        manifest_path = self.project_root / "data_sources" / "sobko_sources" / "forum_threads" / "manifests" / "threads.jsonl"
        manifest_ids = set()
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            manifest_ids.add(json.loads(line)["source_id"])
        registered_ids = {source["source_id"] for source in self.engine.sources if source["source_type"] == "forum_thread"}
        self.assertEqual(registered_ids, manifest_ids)
        build_manifest = json.loads((self.project_root / "metadata" / "build_manifest.json").read_text(encoding="utf-8"))
        build_manifest_ids = set(build_manifest["source_ids"])
        self.assertTrue(manifest_ids.issubset(build_manifest_ids))

    def test_forum_manifest_tags_are_standard_and_synchronized(self) -> None:
        """论坛帖标签必须使用标准 tag，并和 source registry 保持同步。"""

        manifest_path = self.project_root / "data_sources" / "sobko_sources" / "forum_threads" / "manifests" / "threads.jsonl"
        source_by_id = {source["source_id"]: source for source in self.engine.sources if source["source_type"] == "forum_thread"}
        valid_software_tags = set(SOFTWARE_TAGS)
        valid_topic_tags = set(TOPIC_TAGS)
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            source_id = record["source_id"]
            self.assertIn(source_id, source_by_id)
            self.assertTrue(record.get("software_tags"), source_id)
            self.assertTrue(record.get("topic_tags"), source_id)
            self.assertLessEqual(set(record["software_tags"]), valid_software_tags)
            self.assertLessEqual(set(record["topic_tags"]), valid_topic_tags)
            self.assertEqual(source_by_id[source_id]["software_tags"], sorted(set(record["software_tags"])))
            self.assertEqual(source_by_id[source_id]["topic_tags"], sorted(set(record["topic_tags"])))

    def test_forum_image_metadata_excludes_manifest_json(self) -> None:
        """论坛图片附件统计只应包含真实图片，不应把 images/manifest.json 当图片。"""

        forum_root = self.project_root / "data_sources" / "sobko_sources" / "forum_threads"
        manifest_path = forum_root / "manifests" / "threads.jsonl"
        image_suffixes = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"}
        for line in manifest_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            thread_id = record["source_id"].split(":", 1)[1]
            thread_dir = forum_root / thread_id
            index_text = (thread_dir / "index.md").read_text(encoding="utf-8")
            html_text = (thread_dir / "thread.html").read_text(encoding="utf-8")
            image_files = []
            images_dir = thread_dir / "images"
            if images_dir.exists():
                image_files = [
                    path
                    for path in images_dir.iterdir()
                    if path.is_file() and path.name != "manifest.json" and path.suffix.lower() in image_suffixes
                ]
            self.assertNotIn("images/manifest.json", index_text)
            self.assertNotIn("images/manifest.json", html_text)
            self.assertEqual(record["image_count"], len(image_files), record["source_id"])

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

    def test_known_sobtop_search(self) -> None:
        """Sobtop GROMACS topology query 应命中 Sobtop 软件文档。"""

        result = self.engine.search(query="Sobtop GROMACS topology GAFF Hessian", top_k=5)
        self.assertTrue(any(item["source_id"] == "software_doc:sobtop" for item in result.results))

    def test_browser_verified_forum_thread_search(self) -> None:
        """SDD scalar relativistic effect query 应命中完整论坛样例。"""

        result = self.engine.search(query="Gaussian SDD Ti 标量相对论效应 赝势", top_k=5)
        self.assertTrue(any(item["source_id"] == "forum_thread:27982" for item in result.results))

    def test_browser_verified_forum_html_declares_utf8(self) -> None:
        """论坛归档 HTML 应声明 UTF-8，并移除站点广告/登录/回帖噪声。"""

        forum_html_paths = sorted((self.project_root / "data_sources" / "sobko_sources" / "forum_threads").glob("*/*.html"))
        self.assertTrue(forum_html_paths)
        forbidden_markers = [
            "charset=gbk",
            "用户名 Username",
            "注册 Register",
            "发表回复 Post reply",
            'class="ad"',
            "<form",
        ]
        for html_path in forum_html_paths:
            text = html_path.read_text(encoding="utf-8")
            lowered = text.lower()
            for marker in forbidden_markers:
                self.assertNotIn(marker.lower(), lowered)
            self.assertRegex(lowered, r"charset\s*=\s*[\"']?utf-8")
            # Each forum HTML must contain more than just boilerplate — it should
            # include the thread title rendered as an <h1> or meaningful body text.
            self.assertTrue(
                "量子化学" in text
                or "Gaussian" in text
                or "DFT" in text
                or "Multiwfn" in text
                or "分子模拟" in text
                or "量化" in text
                or "波函数" in text
                or "计算化学" in text,
                f"{html_path.name} contains no recognisable forum topic text",
            )


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
