#!/usr/bin/env python
"""运行 Sobko 固定检索评测。"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sobko_mcp.config import build_layout, load_config
from sobko_mcp.evaluation import evaluate, render_markdown_report
from sobko_mcp.retriever import RetrievalEngine


def main() -> None:
    """脚本入口。

    功能目的：
        执行固定评测集并写出 JSON/Markdown 报告。
    输入参数：
        无。
    返回值：
        无，向 stdout 打印报告路径。
    关键流程：
        加载检索引擎 -> 运行评测 -> 渲染 Markdown。
    可能报错或边界情况：
        索引未构建时检索引擎初始化会抛出文件错误。
    """

    layout = build_layout(PROJECT_ROOT)
    config = load_config(layout.configs_dir / "default.json")
    engine = RetrievalEngine(layout, config)
    payload = evaluate(layout, engine)
    report = render_markdown_report(payload)
    report_path = layout.reports_dir / "retrieval_evaluation.md"
    report_path.write_text(report, encoding="utf-8")
    print(report_path)


if __name__ == "__main__":
    main()
