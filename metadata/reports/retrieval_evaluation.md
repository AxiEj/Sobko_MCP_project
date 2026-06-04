# Sobko 检索评测报告

- 样本数：8
- top-1 命中率：100.00%
- top-3 命中率：100.00%
- top-5 命中率：100.00%
- authority 优先正确率：100.00%
- lexical only 比例：100.00%

## 逐条样本

### 1. ORCA TDDFT 空穴电子分析怎么做
- 说明：已知帖子 758 应高位命中
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 3, 4, 5]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：blog_post:758

### 2. NPT 和 NVT 系综什么时候适合使用
- 说明：已知帖子 761 应高位命中
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 3, 4, 5]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：blog_post:761

### 3. Multiwfn quick start 在手册哪里提到
- 说明：手册应优先于博客
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：manual:multiwfn_manual

### 4. Multiwfn command-line mode 说明
- 说明：命令行模式主要在手册中
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 4]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：manual:multiwfn_manual

### 5. IGMH 格点屏蔽 降低可视化耗时
- 说明：已知帖子 756 讨论 IGMH 格点屏蔽
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 3, 4, 5]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：blog_post:756

### 6. mIGM 方法 图形化展现弱相互作用
- 说明：已知帖子 755 讨论 mIGM
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 3, 4, 5]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：blog_post:755

### 7. Gaussian NMR CSGT 轨道对 NICS 贡献
- 说明：已知帖子 670 讨论 Gaussian NMR=CSGT
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 3, 4, 5]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：blog_post:670

### 8. CP2K 波函数 Multiwfn 模拟 STM 图像
- 说明：已知帖子 671 讨论 Multiwfn 结合 CP2K
- top1/top3/top5：True/True/True
- matched_ranks：[1, 2, 3, 4, 5]
- effective_mode：lexical_only
- backend_warnings：['dense_fallback: Ollama embedding 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>', 'rerank_fallback: local=本地 FlagEmbedding reranker 不可用: SOBKO_DISABLE_LOCAL_RERANKER=1; ollama=Ollama rerank 服务不可用: http://127.0.0.1:11434: <urlopen error [Errno 61] Connection refused>']
- top_result：blog_post:671
