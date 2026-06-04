# GitHub 发布方案

## 发布前结论

`Sobko_MCP_project` 是完整可运行包，可以作为一个独立 GitHub 仓库发布。当前最稳妥的选择是发布为 private 仓库，因为项目包含思想家公社帖子和 Multiwfn 手册的本地镜像及其衍生索引。公开发布前需要确认这些内容允许再分发。

## GitHub 大文件边界

GitHub 对普通 Git 仓库的大文件有明确限制：超过 50 MiB 会警告，超过 100 MiB 会阻止提交；仓库理想大小建议小于 1 GB，低于 5 GB 是强烈建议。本项目当前约 650 MB，符合仓库大小建议；`indexes/bm25/lexical_index.json` 约 61 MB，会触发 warning，但不会被 100 MB 限制阻止。

发布前检查：

```bash
cd Sobko_MCP_project
find . -type f -size +90M -print
find . -type f -size +50M -print
du -sh .
```

当前预期：

- `find . -type f -size +90M -print` 无输出。
- `find . -type f -size +50M -print` 只显示 `./indexes/bm25/lexical_index.json`。
- `du -sh .` 约为 `650M`。

## 推荐上传流程

当前目录位于一个更大的工作区下，不应从父目录执行 `git add -A`。请把 `Sobko_MCP_project` 初始化成独立仓库：

```bash
cd "/ABSOLUTE/PATH/TO/Sobko_MCP_project"
git init
git branch -M main
git status --short
```

显式添加本项目文件：

```bash
git add .gitattributes .gitignore README.md NOTICE.md requirements-optional.txt
git add configs data_sources docs indexes metadata normalized scripts server skills sobko_mcp tests
git status --short
```

提交：

```bash
git commit -m "Initial Sobko MCP knowledge base release"
```

创建 private 仓库并 push：

```bash
gh repo create <OWNER>/Sobko_MCP_project --private --source . --remote origin --push
```

如果已经在 GitHub 网页端建好了仓库：

```bash
git remote add origin git@github.com:<OWNER>/Sobko_MCP_project.git
git push -u origin main
```

## 可选 Git LFS 方案

当前普通 Git 可以上传，但如果希望避免 61 MB BM25 文件的 warning，可以把大型索引放入 Git LFS：

```bash
git lfs install
git lfs track "indexes/bm25/lexical_index.json"
git add .gitattributes indexes/bm25/lexical_index.json
git commit -m "Track large Sobko indexes with Git LFS"
```

注意事项：

- Git LFS 有配额和下载带宽限制。
- GitHub 生成源码归档时是否包含 LFS 对象取决于仓库设置。
- 如果目标是“克隆即用”，普通 Git 对当前 650 MB 包更直接；如果后续索引继续变大，再迁移到 LFS 或 Release asset。

## 公开发布前必须确认

- 是否获得思想家公社帖子内容的再分发许可。
- 是否获得 Multiwfn 手册 HTML/Markdown 镜像和资源文件的再分发许可。
- 仓库是否应去掉 `data_sources/`、`normalized/`、`indexes/` 后公开。
- 是否需要单独给源码添加开源许可证，并明确该许可证不覆盖第三方知识源内容。

## 发布后验证

在另一台机器或临时目录中重新 clone：

```bash
git clone <REPO_URL>
cd Sobko_MCP_project
python -m unittest discover -s tests
SOBKO_DISABLE_LOCAL_RERANKER=1 python scripts/smoke_mcp.py
```

如果要验证 hybrid 检索，再配置 Ollama：

```bash
export SOBKO_EMBEDDING_API_BASE_URL="http://YOUR_HOST:11434"
python scripts/evaluate_retrieval.py
```
