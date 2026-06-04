#!/usr/bin/env python
"""构建 Sobko source registry。"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sobko_mcp.config import build_layout, ensure_project_dirs, load_config
from sobko_mcp.registry import build_source_registry


def main() -> None:
    """脚本入口。

    功能目的：
        读取项目内知识源 snapshot 并生成 `normalized/source_registry.jsonl`。
    输入参数：
        无，使用 `configs/default.json`。
    返回值：
        无，向 stdout 打印 source 数。
    关键流程：
        构建目录 -> 加载配置 -> 调用 registry 构建函数。
    可能报错或边界情况：
        知识源缺失时抛出明确文件错误。
    """

    layout = build_layout(PROJECT_ROOT)
    ensure_project_dirs(layout)
    config = load_config(layout.configs_dir / "default.json")
    records = build_source_registry(layout, config)
    print(f"source_registry_built={len(records)}")


if __name__ == "__main__":
    main()
