# Forum thread ingestion rules

Scope: this file governs `data_sources/sobko_sources/forum_threads/` and all child directories.

## Goal

Forum sources must be clean, browser-verified knowledge archives. Keep forum material separate from blog posts, manuals, and software docs.

## Anti-ban / access rules

- Do not bypass WAF, CAPTCHA, or login gates. Use only a user-verified browser session when the user has explicitly helped pass a challenge.
- Do not bulk crawl. Fetch one public page at a time, keep low frequency, and avoid aggressive pagination.
- Prefer public sorted/list pages for candidate discovery. If a page says login is required, stop using that route unless the user explicitly authorizes login.
- Avoid huge megathreads unless a pagination/completeness plan is explicitly chosen. For large threads, do not silently index only page 1 as a full thread.

## What is allowed into the knowledge base

- Only add threads that are clearly related to sobereva/sober老师: authored by sobereva, answered substantively by sobereva, or otherwise technically authoritative because of sobereva's content.
- Prefer high-value posts by views/replies, but also prefer small or self-contained threads first to reduce request volume and completeness risk.
- Full-floor archival capture is allowed and often useful for context. However, do not treat every reply in a high-view thread as authoritative during retrieval.
- Store each accepted thread in its own folder:
  - `<thread_id>/index.md` for clean Markdown content.
  - `<thread_id>/thread.html` for clean standalone archival HTML rendered from `index.md`.
- Register accepted threads only through `manifests/threads.jsonl` with `source_type: forum_thread`.

## Authority and floor-selection rules

- Full-floor archives are allowed. Complete conversation context can be valuable, especially for long tutorial/Q&A threads.
- Separate **archive completeness** from **retrieval authority**:
  - archive completeness says which floors were captured and kept;
  - retrieval authority says which floors should be trusted as expert guidance.
- Source-level `authority_level` currently applies to every generated chunk for that source. Until the pipeline supports per-floor/per-chunk authority, be careful with full multi-user threads.
- If a full thread includes many ordinary-user replies and is indexed as one source, either:
  - set source-level authority conservatively, e.g. `B`, and explain that non-sobereva replies are context; or
  - split/mark content so sobereva floors can keep higher authority than ordinary context floors.
- Preferred high-quality pattern when possible:
  - preserve all floors in the archive if useful;
  - mark sobereva-authored main posts and substantive sobereva answers as authoritative;
  - mark ordinary-user questions/replies as context unless they are directly endorsed/corrected by sobereva;
  - omit or de-emphasize praise-only, thanks-only, duplicate, or off-topic replies in retrieval-facing summaries.
- If preserving all floors, explicitly state in `classification_reason` and `入库完整性评估` that non-sobereva replies are included as conversation context, not as authoritative guidance.
- For canonical sobereva long-form forum articles, `A` is acceptable for the source only when the indexed chunks are dominated by sobereva-authored technical content or the normalizer can distinguish floor-level authority. If all ordinary replies are indexed equally, prefer `B` or split the source.

## Metadata and tag rules

- `topic_tags` in front matter and `manifests/threads.jsonl` must use only the project's standard topic tags from `sobko_mcp/common.py` (`TOPIC_TAGS`).
- Do not invent ad-hoc topic tags such as `DFT`, `泛函选择`, or `综述/教程`. Prefer standard tags such as `量子化学` and `综述/教程/投稿经验`.
- Method names and fine-grained concepts belong in the text and will be extracted as method tags where supported; do not force them into `topic_tags`.
- `software_tags` must use only standard software tags from `sobko_mcp/common.py` (`SOFTWARE_TAGS`).
- Keep front matter and `manifests/threads.jsonl` synchronized for: `source_id`, `title`, URL, date, tags, authority, coverage, crawl time, reply/page counts, confidence, and classification rationale.
- Use stable `source_id` values of the form `forum_thread:<thread_id>`.

## Required Markdown structure

Use this structure for every accepted thread:

```markdown
---
thread_id: 12345
source_id: forum_thread:12345
title: '...'
url: http://bbs.keinsci.com/thread-12345-1-1.html
date: 'YYYY-MM-DDTHH:MM:SS+08:00'
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: windows_chrome_verified_session
source_crawled_at: 'YYYY-MM-DDTHH:MM:SS+08:00'
original_reply_count: 0
page_count: 1
views: 0
software_tags:
- Gaussian
topic_tags:
- 量子化学
authority_level: B
confidence: 0.95
classification_reason: ...
---

# 标题

- 原帖 URL：<...>
- 论坛板块：...
- 作者/关键回答者：...
- 完整性：...

## 核心结论

...

## 楼层正文

### 1 楼｜作者｜YYYY-MM-DD HH:MM:SS

...

## 入库完整性评估

...
```

- Every retained floor heading should include floor number, author, and timestamp: `### N 楼｜作者｜YYYY-MM-DD HH:MM:SS`.
- If the timestamp or author is not available, write `未知作者` or `时间未知`; do not silently omit the field.
- If all floors are kept, say so and state which floors are authoritative versus context when known.
- If only a subset of floors is kept, say exactly which floors were kept and why in `入库完整性评估`.

## Mandatory cleanup rules

- Never keep raw Discuz full-page dumps as `thread.html`. Raw forum pages include navigation, login/register widgets, reply forms, search boxes, footer text, ad containers, and marketing/training signatures.
- `thread.html` must be a clean archival page generated from extracted Markdown, not the original full website shell.
- Remove these non-content areas before saving/indexing:
  - top workshop/training banners,
  - login/register forms,
  - search/navigation bars,
  - reply/editor forms,
  - footer/site chrome,
  - Discuz ad rows such as `class="ad"`,
  - user signatures when they are marketing/training/QQ-group boilerplate rather than part of the answer.
- Keep only the actual question/answer floor text and source metadata needed for traceability.
- Remove marketing/training/QQ-group boilerplate even when it appears inside signatures or repeated copied text.
- For sobereva's own article body, brief mentions of training resources can remain only if they are inseparable from technical context. Pure promotional sentences such as “欢迎参加”, workshop signup pitches, QQ-group promotion, or repeated `keinsci.com/workshop/...` paragraphs should be removed or replaced with a neutral note like `[已省略培训班推广信息]`.
- Do not let marketing text dominate searchable chunks. If a paragraph is mostly promotional, remove it.

## Encoding pitfall

- Discuz pages advertise GBK, but browser/CDP DOM dumps are often written as UTF-8 while retaining `charset=gbk` in the HTML. Opening such files locally causes Chinese mojibake.
- Fix by rendering clean HTML from Markdown with:
  - `python scripts/render_clean_forum_html.py data_sources/sobko_sources/forum_threads`
- If a raw HTML file must be normalized temporarily, use:
  - `python scripts/normalize_forum_html_charset.py <path-or-dir>`
- Final committed HTML must declare UTF-8 and must not contain `charset=gbk`.

## Completeness and metadata

- Mark coverage honestly. Use `browser_verified_full_thread_text` only when all visible pages/floors needed for the thread were captured.
- For large multi-page threads, distinguish archive completeness from indexed-authority completeness:
  - `browser_verified_full_thread_text` means all retained/claimed floors were captured;
  - full-floor archives may still contain low-authority context floors;
  - if only selected floors are kept, use a coverage value such as `browser_verified_selected_thread_text` and list retained floors.
- Record `source_provider`, `source_crawled_at`, `original_reply_count`, `authority_level`, `confidence`, and a short `classification_reason` in both front matter and manifest when applicable.
- If attachments/images are missing, state that explicitly. Do not claim full asset coverage.
- `page_count`, `views`, `last_updated`, and retained floor ranges are recommended for forum posts sorted by views/replies.

## Database/indexing requirements

- Adding a thread to `manifests/threads.jsonl` is not enough. It is only discoverable by MCP after registry, normalization, and indexes are rebuilt.
- After accepted content changes, rebuild the pipeline with the project scripts normally used for this repository, then verify that the new `source_id` appears in:
  - `normalized/source_registry.jsonl`,
  - `normalized/chunks.jsonl`,
  - `indexes/bm25/lexical_index.json`,
  - `indexes/dense/chunk_records.json`,
  - `data_sources/source_registry_snapshot.json`,
  - `metadata/build_manifest.json`.
- Run a targeted retrieval query and confirm the new forum source is returned before claiming it is usable through MCP.

## Validation before handoff

Run these checks after adding or editing forum sources:

```bash
python scripts/render_clean_forum_html.py data_sources/sobko_sources/forum_threads
python scripts/normalize_forum_html_charset.py data_sources/sobko_sources/forum_threads
python -m unittest discover -s tests -p 'test_pipeline.py'
```

For each newly added `forum_thread:<thread_id>`, also verify database membership:

```bash
for f in normalized/source_registry.jsonl normalized/chunks.jsonl indexes/dense/chunk_records.json indexes/bm25/lexical_index.json data_sources/source_registry_snapshot.json metadata/build_manifest.json; do
  rg -q 'forum_thread:<thread_id>' "$f" && echo "ok $f" || echo "missing $f"
done
```

Also manually grep or inspect for forbidden raw-page markers:

- `charset=gbk`
- `用户名 Username`
- `注册 Register`
- `发表回复 Post reply`
- `思想家公社QQ群`
- `北京科音自然科学研究中心`
- `keinsci.com/workshop`
- `class="ad"`
- `<form`

Do not leave scratch/raw browser dumps under this directory. Put temporary raw dumps outside the repo or delete them after extraction.
