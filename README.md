# Sobko MCP Knowledge Base

Sobko 是一个可迁移的 Python MCP 知识库服务，知识源限定为思想家公社学术帖和 Multiwfn 用户手册。项目内已经携带 source snapshot、normalized 数据、BM25 索引、dense embedding 分片、图片索引和评测报告，因此克隆后不需要重新爬取源数据即可直接启动 MCP。

## 当前状态

- MCP server：`sobko-kb`
- Python 包：`sobko_mcp`
- 知识源：577 篇思想家公社学术帖 + 1 份 Multiwfn 用户手册
- 构建规模：578 条 source、11304 个 chunk、2377 条图片记录
- 检索后端：BM25 必选；Ollama embedding 和 rerank 可选增强
- 文件体积：项目约 650 MB；dense 索引分成 4 个 `<50 MB` JSONL 分片；BM25 JSON 约 61 MB，低于 GitHub 100 MB 单文件硬限制

## 能否直接使用

可以。这个目录是完整可运行包，不是只含源码的半成品。用户需要准备 Python 3.10+，然后在项目根目录运行：

```bash
python scripts/smoke_mcp.py
python scripts/run_server.py
```

如果本机没有 embedding 或 rerank 服务，Sobko 会自动降级到 BM25，并在 `backend_warnings` 中写明原因。要启用 hybrid 检索，请修改 `configs/default.json` 中的 Ollama 地址和模型名。

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

## 配置 Ollama

默认配置使用本机 Ollama 示例端口：

```json
{
  "embedding_api_base_url": "http://127.0.0.1:11434",
  "embedding_api_endpoint": "/api/embed",
  "embedding_model": "bge-m3:latest",
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

## GitHub 发布建议

完整包可以上传到 GitHub，但公开发布前必须确认知识源快照的再分发权限。推荐先发布为 private 仓库。若要公开仓库，更稳妥的方案是只发布代码、配置模板和构建脚本，不提交 `data_sources/`、`normalized/`、`indexes/` 中的第三方内容或衍生产物。

详细部署和发布流程见：

- [使用说明](docs/usage.md)
- [部署方案](docs/deployment.md)
- [GitHub 发布方案](docs/github_release.md)
- [迁移说明](docs/migration.md)
- [构建报告](docs/Sobko_MCP_project_build_report.md)
- [权利与来源声明](NOTICE.md)
