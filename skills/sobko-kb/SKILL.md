---
name: sobko-kb
description: 显式调用 Sobko MCP 知识库，检索思想家公社学术帖和 Multiwfn 用户手册证据。
allow_implicit_invocation: false
---

# Sobko KB

当用户显式要求检索 Sobko、思想家公社帖子知识库、Multiwfn 手册知识库，或写出 `$sobko-kb` 时使用。

优先调用 MCP 工具：

- `sobko_search`：检索证据片段。
- `sobko_fetch`：展开 source/chunk 上下文。
- `sobko_get_image`：按 image_id 取图片路径。
- `sobko_trace_source`：追溯 source/chunk 来源。

回答时应说明证据来自帖子还是手册，并保留 `source_id` 或本地路径，避免把检索结果外推成未被来源支持的新结论。
