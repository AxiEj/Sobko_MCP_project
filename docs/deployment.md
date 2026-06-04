# Sobko 部署方案

## 目标

部署 Sobko 的目标是让用户在新机器上直接启动 MCP 知识库，并能按需启用 Ollama embedding/rerank。项目已经携带完整 source snapshot 和索引，因此默认部署不需要重新爬取或重新标准化。

## 推荐部署模式

### 模式 A：完整包私有仓库

这是当前最推荐的发布方式。

- 提交 `data_sources/`、`normalized/`、`indexes/`、`metadata/` 等完整产物。
- 用户克隆后即可运行 smoke test 和 MCP server。
- 适合个人、多机器同步、课题组内部共享。
- 注意：公开发布前需确认思想家公社帖子和 Multiwfn 手册镜像的再分发权限。

### 模式 B：公开代码仓库

如果目标是公开开源，建议只发布代码和构建脚本。

- 提交 `sobko_mcp/`、`scripts/`、`configs/`、`tests/`、`docs/`。
- 不提交 `data_sources/`、`normalized/`、`indexes/` 中的第三方内容或衍生产物。
- README 中说明用户需自行准备源数据并运行构建流程。

### 模式 C：完整包公开仓库

只有在确认源内容再分发许可后再使用。

- 当前体积约 650 MB，低于 GitHub 建议的 1 GB 理想仓库大小。
- `indexes/bm25/lexical_index.json` 约 61 MB，会触发 GitHub 大文件警告，但未超过 100 MB 硬限制。
- dense embedding 已分片，单片低于 50 MB。
- 如果未来任一文件超过 100 MB，必须改用 Git LFS、Release asset 或外部对象存储。

## 新机器部署步骤

```bash
git clone <REPO_URL>
cd Sobko_MCP_project
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

启动 MCP server：

```bash
python scripts/run_server.py
```

注册到 Codex：

```bash
codex mcp add sobko-kb \
  --env SOBKO_FORCE_BUILTIN_MCP=1 \
  --env SOBKO_DISABLE_LOCAL_RERANKER=1 \
  -- python "/ABSOLUTE/PATH/TO/Sobko_MCP_project/scripts/run_server.py"
```

注册后重启 Codex，再用 `tools/list` 确认有以下 4 个工具：

- `sobko_search`
- `sobko_fetch`
- `sobko_get_image`
- `sobko_trace_source`

## Ollama 配置

默认配置文件是 `configs/default.json`。如果 Ollama 在本机，保留：

```json
{
  "embedding_api_base_url": "http://127.0.0.1:11434",
  "rerank_api_base_url": "http://127.0.0.1:11434"
}
```

如果 Ollama 在远程服务器，改成远程地址：

```json
{
  "embedding_api_base_url": "http://YOUR_HOST:11434",
  "rerank_api_base_url": "http://YOUR_HOST:11434"
}
```

也可以用环境变量覆盖，避免把私有地址写进 Git：

```bash
export SOBKO_EMBEDDING_API_BASE_URL="http://YOUR_HOST:11434"
export SOBKO_RERANK_API_BASE_URL="http://YOUR_HOST:11434"
```

## 重建索引

只有在以下情况需要重建：

- 修改知识源快照。
- 修改 chunk 切分逻辑。
- 更换 embedding 模型。
- 修改 dense 分片上限。

重建命令：

```bash
python scripts/build_registry.py
python scripts/normalize_sources.py
python scripts/build_indexes.py
python scripts/evaluate_retrieval.py
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

## 验收标准

- `source registry = 578`。
- `chunks > 10000`。
- `images > 2000`。
- `sobko_search("ORCA TDDFT 空穴电子分析")` 命中 `blog_post:758`。
- `sobko_search("Multiwfn command-line mode")` 命中 `manual:multiwfn_manual`。
- rerank API 不可用时，检索仍返回结果并记录 `rerank_fallback`。
- MCP `tools/list` 返回 4 个 Sobko 工具。

## 运行注意事项

- 首次加载 dense 索引会占用额外内存，因为 JSONL 分片会读入内存用于实时余弦相似度计算。
- 没有 embedding 服务时，查询会降级到 BM25，速度通常更快但语义匹配能力下降。
- 本地 `FlagEmbedding` reranker 首次加载可能较慢；发布和 smoke test 建议设置 `SOBKO_DISABLE_LOCAL_RERANKER=1`。
- 路径中包含中文目录名，Python 代码按 UTF-8 读取；迁移到 Linux/CentOS 时确认文件系统和终端 locale 支持 UTF-8。
