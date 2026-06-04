#!/usr/bin/env python
"""标准化 Sobko source。"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sobko_mcp.config import build_layout, ensure_project_dirs
from sobko_mcp.normalizer import normalize_sources


def main() -> None:
    """脚本入口。

    功能目的：
        从 `source_registry.jsonl` 生成 chunk、image 和 section 中间产物。
    输入参数：
        无。
    返回值：
        无，向 stdout 打印构建计数。
    关键流程：
        构建目录 -> 调用 normalizer -> 打印结果。
    可能报错或边界情况：
        registry 尚未构建时会抛出文件缺失错误。
    """

    layout = build_layout(PROJECT_ROOT)
    ensure_project_dirs(layout)
    counts = normalize_sources(layout)
    print(counts)


if __name__ == "__main__":
    main()
