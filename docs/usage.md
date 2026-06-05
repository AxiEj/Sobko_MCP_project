# Sobko 使用说明

## 使用目标

Sobko 的目标是提供可迁移、可离线降级的 MCP 知识库。BM25 是基础路径；embedding 和 rerank 是增强路径。增强后端不可用时，检索不会失败，而是返回 BM25 结果并在 `backend_warnings` 中写明降级原因。

## 环境要求

- Python 3.10 或更高版本。
- 不安装任何额外依赖也可以运行 BM25 和内置 stdio MCP server。
- 可选依赖：
  - `mcp`：使用官方 FastMCP server。
  - `FlagEmbedding`：启用本地 reranker。
  - `transformers` + `torch`：启用默认 BGE-M3 本地语义检索。
  - Ollama：启用 `/api/embed` embedding；如果当前 Ollama 版本没有 `/api/rerank`，rerank 会自动降级。

## 最小验证

```bash
cd Sobko_MCP_project
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

期望结果：

- source 数量为 578。
- chunk 数量大于 10000。
- `sobko_search("ORCA TDDFT 空穴电子分析")` 命中 `blog_post:758`。
- `sobko_search("Multiwfn command-line mode")` 命中 `manual:multiwfn_manual`。
- MCP `tools/list` 返回 4 个 Sobko 工具。

## MCP 使用

启动 server：

```bash
python scripts/run_server.py
```

Codex 注册示例：

```bash
codex mcp add sobko-kb \
  --env SOBKO_FORCE_BUILTIN_MCP=1 \
  --env SOBKO_DISABLE_LOCAL_RERANKER=1 \
  -- python "/ABSOLUTE/PATH/TO/Sobko_MCP_project/scripts/run_server.py"
```

`SOBKO_FORCE_BUILTIN_MCP=1` 用于强制使用项目内置 JSON-RPC MCP 实现，适合没有安装 `mcp` 包的环境。`SOBKO_DISABLE_LOCAL_RERANKER=1` 用于避免首次加载本地 reranker 模型造成启动或查询变慢。

如果同一台机器上 Codex 和 Claude 会同时连接 Sobko，建议先启动共享 embedding daemon：

```bash
python scripts/run_embedding_daemon.py
```

默认配置中 `embedding_daemon_enabled=true`，MCP 会优先调用 `http://127.0.0.1:8769/api/embed`。daemon 不在线时会回退到 MCP 进程内的本地 HuggingFace encoder；若要避免任何 MCP 进程加载 BGE-M3，可设置：

```bash
export SOBKO_EMBEDDING_DAEMON_REQUIRED=1
```

## Python 直接调用示例

```python
from pathlib import Path

from sobko_mcp.config import build_layout, load_config
from sobko_mcp.retriever import RetrievalEngine

project_root = Path("/ABSOLUTE/PATH/TO/Sobko_MCP_project")
layout = build_layout(project_root)
config = load_config(layout.configs_dir / "default.json")

# 如果只想离线测试 BM25，可关闭增强检索。
config.rag_use_embedding = False
config.rag_use_reranker = False

engine = RetrievalEngine(layout, config)
result = engine.search(query="ORCA TDDFT 空穴电子分析", top_k=5)

for item in result.results:
    print(item["source_id"], item["score"], item["title"])
```

## 配置说明

主要配置文件是 `configs/default.json`：

- `posts_manifest_path`、`posts_root_path`：思想家公社学术帖快照路径。
- `manual_root_path`、`manual_markdown_path`、`manual_html_path`：Multiwfn 手册快照路径。
- `embedding_api_base_url`、`embedding_api_endpoint`、`embedding_model`：embedding 服务配置。
- `embedding_daemon_enabled`、`embedding_daemon_base_url`：是否优先使用共享 embedding daemon。
- `rerank_api_base_url`、`rerank_api_endpoint`、`rerank_model`：rerank 服务配置。
- `rag_use_embedding`、`rag_use_reranker`：是否启用增强检索。
- `rag_embedding_weight`、`rag_bm25_weight`：hybrid 融合权重。
- `dense_batch_size`、`dense_shard_max_bytes`：dense 构建批大小和分片上限。

如果 API 地址不想写入配置文件，可以使用环境变量覆盖：

```bash
export SOBKO_EMBEDDING_API_BASE_URL="http://127.0.0.1:11434"
export SOBKO_RERANK_API_BASE_URL="http://127.0.0.1:11434"
```

## 重建流程

```bash
python scripts/build_registry.py
python scripts/normalize_sources.py
python scripts/build_indexes.py
python scripts/evaluate_retrieval.py
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

`scripts/build_indexes.py` 支持增量 embedding cache。它会从上一版 dense shards 中按 chunk hash 和 embedding vector-space fingerprint 复用未变化向量；新增或变更的 chunk 才会重新计算。缓存统计会写入 `indexes/dense/metadata.json` 的 `cache_stats`。

## 输入格式

- 学术帖 manifest：JSONL，每行一篇帖子，必须包含 `post_id`、`title`、`academic_markdown_path`。
- 学术帖正文：Markdown，路径相对于 `posts_root_path`。
- Multiwfn 手册：`Multiwfn_manual.md`，推荐保留同目录 HTML 和资源文件。

## 输出格式

- `normalized/source_registry.jsonl`：source 元数据。
- `normalized/chunks.jsonl`：检索 chunk。
- `normalized/images.jsonl`：图片索引原始记录。
- `indexes/bm25/lexical_index.json`：BM25 索引。
- `indexes/dense/metadata.json` 与 `indexes/dense/shards/*.jsonl`：dense 分片索引。
- dense shard 记录中的 `chunk_hash` 和 `cache_key`：用于下一次增量构建复用 embedding。
- `metadata/reports/retrieval_evaluation.*`：评测报告。

## 易错点

- 如果只想测试 BM25，可把 `rag_use_embedding` 设为 `false`。
- 如果本地 `FlagEmbedding` 模型加载太慢，可设置 `SOBKO_DISABLE_LOCAL_RERANKER=1`。
- 如果想让 Codex/Claude 共享 BGE-M3 模型，先运行 `python scripts/run_embedding_daemon.py`，再重启 MCP 客户端。
- 如果 Ollama 不在本机，修改 `embedding_api_base_url` 和 `rerank_api_base_url`。
- Ollama 旧版本可能没有 `/api/rerank`，这是可接受降级，不是 Sobko 构建失败。
