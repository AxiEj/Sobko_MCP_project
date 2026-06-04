# Sobko MCP Project Build Report

## 构建摘要

- 项目目录：`Sobko_MCP_project`
- Python 包：`sobko_mcp`
- MCP server：`sobko-kb`
- 索引版本：`2026.06.sobko.v1`
- 知识源范围：
  - 思想家公社学术帖：577 篇
  - Multiwfn 用户手册：1 份

## 构建产物

- source registry：578 条 source
- chunks：11304 条
- images：2377 条
- BM25 文档数：11304
- dense embedding：可用
- dense 模型：`bge-m3:latest`
- dense 向量数：11304
- dense 分片数：4
- dense 分片大小：约 43 MB、43 MB、43 MB、9.4 MB，均小于 50 MB

## 验证记录

已执行：

```bash
python scripts/build_registry.py
python scripts/normalize_sources.py
python scripts/build_indexes.py
SOBKO_DISABLE_LOCAL_RERANKER=1 python scripts/evaluate_retrieval.py
SOBKO_DISABLE_LOCAL_RERANKER=1 python -m unittest discover -s tests
SOBKO_DISABLE_LOCAL_RERANKER=1 python scripts/smoke_mcp.py
```

结果：

- 固定评测：8/8 top-1、top-3、top-5 命中；当前默认配置无本机 Ollama 服务时 `lexical_only_rate=1.0`
- 单元测试：9 tests OK
- MCP smoke：`tools/list` 返回 4 个工具，`sobko_search("ORCA TDDFT 空穴电子分析")` 命中 `blog_post:758`
- 降级行为：embedding/rerank 服务不可用时，检索仍返回结果，并在 `backend_warnings` 中记录 `dense_fallback` 和 `rerank_fallback`

## 注意事项

- `configs/default.json` 默认使用 `http://127.0.0.1:11434`，不保留个人内网或反向代理 fallback 地址；迁移后由用户自行填写。
- `scripts/smoke_mcp.py` 会设置 `SOBKO_FORCE_BUILTIN_MCP=1`，用于稳定测试内置 stdio MCP 实现。
- 如果迁移到新机器后 embedding 模型或端口变化，修改 `configs/default.json` 后重新运行 `scripts/build_indexes.py`。
- registry、chunk、image 产物中的项目内路径保存为相对路径；MCP 运行时会按当前项目根解析为实际本地路径。
