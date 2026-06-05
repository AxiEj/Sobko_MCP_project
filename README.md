# Sobko MCP Knowledge Base

<p align="center">
  <img src="docs/assets/sobko_logo/Sobko_LOGO.png" alt="Sobko logo" width="180">
</p>

Sobko 是一个可迁移的 Python MCP 知识库服务，知识源限定为思想家公社学术帖和 Multiwfn 用户手册。项目内已经携带 source snapshot、normalized 数据、BM25 索引、dense embedding 分片、图片索引和评测报告，因此克隆后不需要重新爬取源数据即可直接启动 MCP。

## 当前状态

- MCP server：`sobko-kb`
- Python 包：`sobko_mcp`
- 知识源：577 篇思想家公社学术帖 + 1 份 Multiwfn 用户手册
- 构建规模：578 条 source、11304 个 chunk、2377 条图片记录
- 检索后端：BM25 必选；本地 HuggingFace embedding 可选增强；支持共享 embedding daemon；OpenAI/Ollama 仍可手动配置
- 文件体积：项目约 1.2 GB；BGE-M3 dense 索引分成 6 个 `<50 MB` JSONL 分片；BM25 JSON 约 61 MB，低于 GitHub 100 MB 单文件硬限制；BGE-M3 模型另存在 HuggingFace cache 中

## 能否直接使用

可以。这个目录是完整可运行包，不是只含源码的半成品。用户需要准备 Python 3.10+，然后在项目根目录运行：

```bash
python scripts/smoke_mcp.py
python scripts/run_server.py
```

如果本机没有可用 embedding 后端，Sobko 会自动降级到 BM25，并在 `backend_warnings` 中写明原因。默认语义后端是本地 HuggingFace encoder（BAAI/bge-m3），不需要 Ollama 或 OpenAI API key；首次使用前需要能下载或本地已有配置模型。

## 目录结构

```text
configs/       用户配置，主要填写 embedding/rerank API 地址和模型
data_sources/  本项目实际使用的知识源快照
normalized/    标准化 source、chunk、section、image 数据
indexes/       BM25、dense embedding、图片查找索引
metadata/      构建清单、评测样例和评测报告
sobko_mcp/     MCP server、检索器、normalizer、registry 等源码
scripts/       构建、评测、启动和 smoke test 脚本
tests/         单元测试
docs/          使用、迁移、部署和构建报告
skills/        Codex skill 示例
server/        server 说明
```

## 快速开始

```bash
cd Sobko_MCP_project
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

注册到 Codex MCP 的示例命令：

```bash
codex mcp add sobko-kb \
  --env SOBKO_FORCE_BUILTIN_MCP=1 \
  --env SOBKO_DISABLE_LOCAL_RERANKER=1 \
  -- python "/ABSOLUTE/PATH/TO/Sobko_MCP_project/scripts/run_server.py"
```

之后重启 Codex，确认 `tools/list` 能看到 4 个工具：

- `sobko_search`
- `sobko_fetch`
- `sobko_get_image`
- `sobko_trace_source`

如果 Codex 和 Claude 会同时使用 Sobko，建议额外启动一个共享 embedding daemon，避免两个 MCP 进程各自加载 BGE-M3：

```bash
python scripts/run_embedding_daemon.py
```

默认 MCP 会优先尝试 `http://127.0.0.1:8769` 的 daemon；daemon 不在线时自动回退到 MCP 进程内本地 embedding。若要强制只用 daemon，可设置：

```bash
export SOBKO_EMBEDDING_DAEMON_REQUIRED=1
```

## 配置本地语义检索（不需要 Ollama / OpenAI API）

默认配置使用本地 HuggingFace encoder（BGE-M3，1024 维，多语言）：

```json
{
  "embedding_provider": "local_hf",
  "embedding_model": "BAAI/bge-m3",
  "embedding_dimensions": null,
  "local_embedding_max_length": 8192,
  "embedding_daemon_enabled": true,
  "embedding_daemon_base_url": "http://127.0.0.1:8769",
  "rag_use_reranker": false
}
```

这个模式不使用 OpenAI API key，也不需要 Ollama。它依赖当前 Python 环境中的 `transformers` 和 `torch`；模型可以是 HuggingFace 模型名，也可以是本地模型目录。首次构建 dense 索引时如果本地没有 BGE-M3，会尝试从 HuggingFace 下载约 2GB 级模型。

切换 embedding provider 或模型后必须运行：

```bash
python scripts/build_indexes.py
```

否则旧 dense 索引不能混用，检索会自动降级到 BM25 并提示 provider/model 不匹配。`build_indexes.py` 会按 `chunk_hash + provider + model + dimension + local encoder options` 复用未变化 chunk 的旧向量；新增或改动的 chunk 才会重新 embedding。

如果你想用 OpenAI-compatible embeddings，也可以手动改成：

```json
{
  "embedding_provider": "openai",
  "embedding_api_base_url": "https://api.openai.com",
  "embedding_api_endpoint": "/v1/embeddings",
  "embedding_model": "text-embedding-3-small",
  "embedding_dimensions": 1536
}
```

并用环境变量提供 key：`OPENAI_API_KEY` 或 `SOBKO_OPENAI_API_KEY`。

## 配置 Ollama

如果你仍想使用本机或远程 Ollama，可以把配置改回：

```json
{
  "embedding_provider": "ollama",
  "embedding_api_base_url": "http://127.0.0.1:11434",
  "embedding_api_endpoint": "/api/embed",
  "embedding_model": "bge-m3:latest",
  "embedding_dimensions": null,
  "rag_use_reranker": true,
  "rerank_api_base_url": "http://127.0.0.1:11434",
  "rerank_api_endpoint": "/api/rerank",
  "rerank_model": "dengcao/bge-reranker-v2-m3:latest"
}
```

如果 Ollama 在远程机器，将 `embedding_api_base_url`、`rerank_api_base_url` 改成对应地址。也可以临时用环境变量覆盖：

```bash
export SOBKO_EMBEDDING_API_BASE_URL="http://127.0.0.1:11434"
export SOBKO_RERANK_API_BASE_URL="http://127.0.0.1:11434"
```

## 重建索引

已有索引可直接使用。只有在修改知识源、chunk 参数、embedding 模型或 API 地址后，才需要重建：

```bash
python scripts/build_registry.py
python scripts/normalize_sources.py
python scripts/build_indexes.py
python scripts/evaluate_retrieval.py
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

重建 dense 索引时启用增量缓存：如果 embedding 配置和 chunk hash 未变，脚本会从上一版 dense shards 复用向量并在 `indexes/dense/metadata.json` 的 `cache_stats` 中记录 `reused/computed/total`。

## GitHub 发布建议

完整包可以上传到 GitHub，但公开发布前必须确认知识源快照的再分发权限。推荐先发布为 private 仓库。若要公开仓库，更稳妥的方案是只发布代码、配置模板和构建脚本，不提交 `data_sources/`、`normalized/`、`indexes/` 中的第三方内容或衍生产物。

详细部署和发布流程见：

- [使用说明](docs/usage.md)
- [部署方案](docs/deployment.md)
- [GitHub 发布方案](docs/github_release.md)
- [迁移说明](docs/migration.md)
- [构建报告](docs/Sobko_MCP_project_build_report.md)
- [权利与来源声明](NOTICE.md)
