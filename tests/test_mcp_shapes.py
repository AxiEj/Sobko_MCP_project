"""Sobko MCP 结果形状测试。"""

from __future__ import annotations

import os
import unittest
from pathlib import Path

from sobko_mcp.config import build_layout, load_config
from sobko_mcp.retriever import RetrievalEngine


class McpShapeTests(unittest.TestCase):
    """验证 fetch、image 和 trace 的基础行为。"""

    @classmethod
    def setUpClass(cls) -> None:
        """加载检索引擎。"""

        os.environ["SOBKO_DISABLE_LOCAL_RERANKER"] = "1"
        cls.project_root = Path(__file__).resolve().parents[1]
        cls.layout = build_layout(cls.project_root)
        cls.config = load_config(cls.layout.configs_dir / "default.json")
        cls.config.rag_use_embedding = False
        cls.config.rag_use_reranker = False
        cls.engine = RetrievalEngine(cls.layout, cls.config)

    def test_fetch_manual_source(self) -> None:
        """手册 source 应支持 fetch。"""

        payload = self.engine.fetch(source_id="manual:multiwfn_manual", expand_prev_next=1)
        self.assertEqual(payload["source_id"], "manual:multiwfn_manual")
        self.assertTrue(payload["context_chunks"])

    def test_trace_known_chunk(self) -> None:
        """search 出来的 chunk 应可 trace 到 source。"""

        result = self.engine.search(query="NPT 和 NVT 系综什么时候用", top_k=1)
        self.assertTrue(result.results)
        trace = self.engine.trace_source(chunk_id=result.results[0]["chunk_id"])
        self.assertEqual(trace["source_id"], result.results[0]["source_id"])

    def test_get_known_image(self) -> None:
        """博客图片应能通过 image_id 返回本地路径。"""

        result = self.engine.search(query="键双描述符 Multiwfn", top_k=5)
        image_ids = [image_id for item in result.results for image_id in item["image_ids"]]
        if not image_ids:
            self.skipTest("当前 top5 没有图片结果，跳过图片形状测试。")
        payload = self.engine.get_image(image_id=image_ids[0])
        self.assertEqual(payload["return_mode"], "path")
        self.assertTrue(payload["path"])
        self.assertIn("nearby_text", payload)

    def test_trace_manual_source(self) -> None:
        """手册 source trace 应返回 HTML 路径和 authority。"""

        payload = self.engine.trace_source(source_id="manual:multiwfn_manual")
        self.assertEqual(payload["authority_level"], "A")
        self.assertTrue(payload["html_path"].endswith("Multiwfn_manual.html"))


if __name__ == "__main__":
    unittest.main()
