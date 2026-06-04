# Sobko 迁移说明

## 迁移结论

当前 `Sobko_MCP_project` 是完整迁移包。只要保留下面目录，迁移到新机器后不需要重新爬取源数据，也不需要立即重建索引。

## 必须携带的目录

- `configs/`
- `data_sources/`
- `normalized/`
- `indexes/`
- `metadata/`
- `sobko_mcp/`
- `scripts/`
- `tests/`
- `docs/`
- `server/`
- `skills/`

## 默认配置原则

`configs/default.json` 不应保存个人内网、反向代理或临时测试地址。公开或共享前，默认只保留：

```json
{
  "embedding_api_base_url": "http://127.0.0.1:11434",
  "embedding_fallback_base_urls": [],
  "rerank_api_base_url": "http://127.0.0.1:11434",
  "rerank_fallback_base_urls": []
}
```

迁移到新机器后，用户可以直接修改配置，也可以用环境变量覆盖：

```bash
export SOBKO_EMBEDDING_API_BASE_URL="http://YOUR_HOST:11434"
export SOBKO_RERANK_API_BASE_URL="http://YOUR_HOST:11434"
```

## GitHub 文件体积

dense embedding 使用 `indexes/dense/shards/chunk_embeddings_*.jsonl` 分片保存，默认单片上限约 45 MB。迁移或发布前可检查：

```bash
find indexes/dense/shards -type f -size +90M -print
```

如果出现大文件，调小 `configs/default.json` 中的 `dense_shard_max_bytes` 后重新运行：

```bash
python scripts/build_indexes.py
```

当前完整包还有一个 BM25 JSON 文件约 61 MB：

```bash
find indexes/bm25 -type f -size +50M -print
```

该文件低于 GitHub 100 MB 单文件硬限制，但 push 时可能出现 large file warning。若希望避免 warning，可把它改用 Git LFS 或把索引作为 Release asset 分发。

## 新机器验证

```bash
python scripts/evaluate_retrieval.py
python -m unittest discover -s tests
python scripts/smoke_mcp.py
```

如果没有 embedding 服务，评测会以 BM25 降级路径运行，`backend_warnings` 会记录原因。

## 公开发布注意事项

完整包包含第三方知识源快照和衍生索引。公开发布前请确认源内容再分发权限。若不能确认，应采用代码公开、数据自备的发布方式。
