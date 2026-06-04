#!/usr/bin/env python
"""启动 Sobko stdio MCP server。"""

from __future__ import annotations

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sobko_mcp.mcp_server import SobkoMcpServer, build_fastmcp_server


def main() -> None:
    """脚本入口。

    功能目的：
        启动 Sobko MCP server。
    输入参数：
        无。
    返回值：
        无。
    关键流程：
        优先使用官方 `mcp` 包的 FastMCP；不可用时回退到内置 JSON-RPC stdio server。
    可能报错或边界情况：
        索引尚未构建时会在启动时抛出文件缺失错误。
    """

    if os.environ.get("SOBKO_FORCE_BUILTIN_MCP") == "1":
        SobkoMcpServer().serve_forever()
        return
    try:
        build_fastmcp_server().run(transport="stdio")
    except ImportError:
        SobkoMcpServer().serve_forever()


if __name__ == "__main__":
    main()
