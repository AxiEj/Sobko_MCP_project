---
thread_id: 27982
source_id: forum_thread:27982
title: 'Gaussian 16中对Ti的计算采用SDD基组考虑了相对论效应吗？'
url: http://bbs.keinsci.com/forum.php?mod=viewthread&tid=27982&extra=&ordertype=1
date: '2022-02-27T23:30:45+08:00'
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: windows_chrome_verified_session
source_crawled_at: '2026-06-05T15:15:00+08:00'
original_reply_count: 2
software_tags:
- Gaussian
topic_tags:
- 量子化学
- 赝势
- 综述/教程/投稿经验
authority_level: B
confidence: 0.96
classification_reason: 已通过用户手动验证后的浏览器会话读取完整论坛页正文；主题是 Gaussian 默认 SDD 对 Ti 是否体现相对论效应，sobereva 给出明确技术回答。
---

# Gaussian 16中对Ti的计算采用SDD基组考虑了相对论效应吗？

- 原帖 URL：<https://bbs.keinsci.com/forum.php?mod=viewthread&tid=27982&extra=&ordertype=1>
- 论坛板块：量子化学 (Quantum Chemistry)
- 发布时间：2022-02-27 23:30:45
- 抓取方式：用户手动通过论坛人机验证后，用同一 Windows Chrome 会话读取页面正文。
- 完整性：**正文完整**。本页共 3 层（楼主问题、sobereva 回答、楼主感谢）；无附件。

## 核心结论

Gaussian 16 中直接使用默认 SDD 描述 Ti 时，可以回答审稿人：**考虑了标量相对论效应**。原因不是“基组本身体现相对论效应”，而是 Gaussian 默认形式使用 SDD 时搭配的是考虑了相对论效应的赝势，因此等效体现了相对论效应。

## 楼层正文

### 1 楼｜zhaoyangwx｜2022-2-27 23:30:45

计算时对Ti采用了Gaussian 16中默认的SDD基组，审稿人提问“Are relativistic effects considered for titanium atom?”。请问等同于考虑了相对论效应吗？

### 2 楼｜sobereva｜2022-2-28 00:44:59

考虑了标量相对论效应
相对论效应不是从基组层面体现的，具体来说是Gaussian里直接以默认形式用SDD的时候搭配的是考虑了相对论效应的赝势，所以才能等效体现相对论效应。

### 3 楼｜zhaoyangwx｜2022-2-28 07:50:54

sobereva 发表于 2022-2-28 00:44
考虑了标量相对论效应
相对论效应不是从基组层面体现的，具体来说是Gaussian里直接以默认形式用SDD的时候 ...
非常感谢您的回复！

## 入库完整性评估

- 问题、回答、后续感谢均可见。
- 没有附件需要下载。
- 这是适合入库的完整短问答样例。
