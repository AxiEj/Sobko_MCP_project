# Sobko MCP Server

启动命令：

```bash
python scripts/run_server.py
```

server 会优先使用官方 `mcp` Python 包的 FastMCP。若环境未安装 `mcp`，会自动回退到项目内置的 stdio JSON-RPC MCP 实现。

暴露工具：

- `sobko_search`
- `sobko_fetch`
- `sobko_get_image`
- `sobko_trace_source`

建议先运行：

```bash
python scripts/smoke_mcp.py
```

确认 `tools/list` 返回 4 个工具，并且 `sobko_search("ORCA TDDFT 空穴电子分析")` 能命中 `blog_post:758`。
