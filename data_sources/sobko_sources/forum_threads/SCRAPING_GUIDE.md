# bbs.keinsci.com 抓取经验与踩坑记录

本文档记录从计算化学公社论坛抓取 sobereva 老师帖子过程中积累的经验、踩过的坑、以及最佳实践，方便下次继续。

## 1. WAF / 人机验证

### 1.1 阿里云 WAF 特征

bbs.keinsci.com 使用阿里云 ESA（Edge Security Acceleration）防护：

- **触发时返回**：滑块验证页面，标题为 "Verification" 或 "提示信息"
- **验证元素**：`验证您是真人`、`AliyunCaptcha`、滑块组件
- **Cookie**：`acw_tc`、`cdn_sec_tc` —— WAF 是 cookie/会话级别，不是 IP 级别
- **绕过方式**：必须在用户帮助下，用**可见 Chrome 窗口**手动通过滑块验证

### 1.2 页面状态判别（必须精确区分）

```
验证您是真人 / AliyunCaptcha     → WAF 墙，需要人工过验证
指定的版块不存在                  → URL 错误（版块 ID 写错了）
请先登录后才能继续浏览            → 需要登录（该页面不可公开访问）
普通论坛页面（标题不为"提示信息"）→ 正常
```

**重要**：永远不要假设所有 "提示信息" 都是 WAF。先读 `body.innerText` 前 500 字符判断。

### 1.3 版块 URL 对照表

| 版块名 | 正确 URL | 错误示例 |
|--------|----------|----------|
| 量子化学 | `forum-103-1.html` | - |
| 波函数分析与Multiwfn | `forum-112-1.html` | ~~forum-136~~ ❌ |
| 分子模拟 | `forum-104-1.html` | - |
| 第一性原理 | `forum-105-1.html` | - |

版块列表页比具体帖子页更容易触发 WAF。优先通过首页导航栏提取版块 URL。

## 2. Chrome CDP 远程控制

### 2.1 启动命令

```bash
google-chrome \
  --incognito \
  --no-sandbox \
  --disable-gpu \
  --ignore-certificate-errors \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-profile \
  'http://bbs.keinsci.com/forum.php' 2>/dev/null &
```

- `--remote-debugging-port=9222`：开启 CDP
- `--user-data-dir=/tmp/chrome-debug-profile`：独立 profile，可复用 cookie
- `--ignore-certificate-errors`：站点 SSL 证书有问题时的必要参数

### 2.2 连接方式

```javascript
const puppeteer = require('puppeteer-core'); // 不是 puppeteer！
const browser = await puppeteer.connect({ browserURL: 'http://127.0.0.1:9222' });
```

- 必须用 `puppeteer-core`，不是 `puppeteer`
- **不要 install 到项目目录**（污染工作区），装到 `/tmp/puppeteer-tmp/`

### 2.3 常见 CDP 问题

| 问题 | 原因 | 解决 |
|------|------|------|
| `Execution context was destroyed` | 页面在 evaluate 期间发生了导航/重定向 | catch 错误后重试，或等更久 |
| `Navigation timeout` | 页面加载超时（WAF 或网络慢） | 增加 timeout 到 20-30s，或检查是否被墙 |
| 新标签抢占焦点 | `browser.newPage()` 会弹到前台 | 用 `page.evaluate()` + `fetch()` 下载图片，不新建标签 |
| 附件弹窗残留 | 之前打开的 `mod=attachment` 页面未关闭 | 定期 `page.close()` 非论坛标签 |

## 3. 防封策略（模拟人类）

### 3.1 请求节奏

```javascript
const delay = () => new Promise(r => setTimeout(r, 4000 + Math.random() * 4000));
// 每页之间 4-8 秒随机延迟
// 每张图片下载之间 1.5-2.5 秒延迟
// 每个帖子之间 5-10 秒随机休息
```

### 3.2 行为模拟

- 每页加载后执行 `window.scrollBy(0, 200 + Math.random() * 400)` 模拟滚动
- 不要连续快速翻页
- 不要同时打开多个标签请求论坛
- 每 3-5 页保存一次进度（防止中途被墙丢失数据）

### 3.3 自检机制

```javascript
// 空页检测：每页提取后检查 floor 数量
if (floors.every(f => !f)) {
  await new Promise(r => setTimeout(r, 2500));
  floors = await page.evaluate(() =>
    [...document.querySelectorAll('.t_f')].map(el => el.innerText.trim())
  );
}
// 如果仍然为空，说明该页确实没有内容或被墙
```

### 3.4 WAF 检测包装

每次导航前后都检查页面状态，一旦检测到 WAF 立即停止并通知用户：

```javascript
async function checkWAF(page) {
  const body = await page.evaluate(() => document.body.innerText.substring(0, 400));
  if (body.includes('验证您是真人') || body.includes('AliyunCaptcha')) {
    console.log('❌ 被墙！需要人工过验证');
    return true;
  }
  return false;
}
```

## 4. 帖子内容提取

### 4.1 Discuz 页面结构

- **帖子正文**：`.t_f` 元素
- **作者名**：不在 `.t_f` 中，在 `a[href*="uid="]` 链接中（用户侧边栏）
- **楼层信息**：`.pi` 或 `.authi` 中包含楼层号和发帖时间
- **分页**：`a[href*="thread-{tid}-"]` 链接中的数字提取 `Math.max(...nums)`
- **浏览/回复数**：`Views: XXX` / `回复 Reply: XXX` 正则提取

### 4.2 纯文本提取（推荐，简单可靠）

```javascript
const floors = await page.evaluate(() =>
  [...document.querySelectorAll('.t_f')].map(el => el.innerText.trim())
);
```

- `.innerText` 自动去除 HTML 标签
- 简单快速，正文完整
- **缺点**：丢失图片

### 4.3 带图片提取（仅在需要时使用）

图片在 Discuz 中以附件形式存在：

```html
<img class="zoom" src="static/image/common/none.gif"
     zoomfile="forum.php?mod=attachment&aid=XXXXX..."
     file="forum.php?mod=attachment&aid=XXXXX...">
```

- `src` 是占位图 `none.gif`
- 真正的图片 URL 在 `zoomfile` 属性中
- 下载 URL = `http://bbs.keinsci.com/{zoomfile}`

### 4.4 图片下载（静默方式，不弹新标签）

```javascript
const b64 = await page.evaluate(async (url) => {
  const resp = await fetch(url);
  const blob = await resp.blob();
  const buf = await blob.arrayBuffer();
  const bytes = new Uint8Array(buf);
  let bin = '';
  for (let i = 0; i < bytes.length; i++) bin += String.fromCharCode(bytes[i]);
  return { b64: btoa(bin), size: blob.size };
}, 'http://bbs.keinsci.com/' + zoomfileUrl);
```

**关键**：使用 `page.evaluate()` 内的 `fetch()` 下载——不创建新标签，不抢用户焦点。

### 4.5 图片魔数校验（防止 HTML 错误页冒充图片）

```javascript
function isImage(buf) {
  if (buf[0] === 0xFF && buf[1] === 0xD8 && buf[2] === 0xFF) return '.jpg';
  if (buf[0] === 0x89 && buf[1] === 0x50 && buf[2] === 0x4E && buf[3] === 0x47) return '.png';
  if (buf[0] === 0x47 && buf[1] === 0x49 && buf[2] === 0x46) return '.gif';      // "GIF"
  if (buf[0] === 0x42 && buf[1] === 0x4D) return '.bmp';                          // "BM"
  return null; // 不是图片（很可能是 HTML 错误页）
}
```

**常见陷阱**：
- **3191 字节的文件**：通常是 Discuz 错误 HTML 页面，不是图片
- **4321 字节的文件**：同样的问题
- 仅靠 `size > 500` 不够——必须检查文件头魔数
- 已下载的假图片用 `file` 命令检查：`file *.jpg | grep HTML` → 删除

## 5. 文件格式与规范

### 5.1 目录结构

```
data_sources/sobko_sources/forum_threads/
├── AGENTS.md                    # 规则文件（必须遵守）
├── SCRAPING_GUIDE.md            # 本文档
├── manifests/
│   └── threads.jsonl            # 所有线程的注册清单
├── {thread_id}/
│   ├── index.md                 # 纯净 Markdown 正文
│   ├── thread.html              # 从 index.md 渲染的 HTML
│   └── images/                  # 附属图片（可选）
│       ├── img_1.png
│       └── ...
```

### 5.2 index.md 格式

```markdown
---
thread_id: 536
source_id: forum_thread:536
title: '帖子标题'
url: http://bbs.keinsci.com/thread-536-1-1.html
date: '2014-12-29T12:27:24+08:00'
source_type: forum_thread
coverage: browser_verified_full_thread_text
source_provider: wsl2_chrome_cdp_verified_session
image_count: 0
original_reply_count: 91
page_count: 7
authority_level: A
confidence: 0.99
---

# 帖子标题

- 原帖 URL：<http://bbs.keinsci.com/thread-XXX-1-1.html>

## 楼层正文

### 1 楼（楼主）｜sobereva

{正文内容}

### 2 楼

{正文内容}
...
```

### 5.3 重要规则（来自 AGENTS.md）

- **`thread.html` 必须是从 `index.md` 渲染的干净 HTML**，不能是原始 Discuz 页面 dump
- **删除非正文区域**：登录/注册表单、导航栏、回复框、页脚、广告、营销签名
- **URL 必须用 `http://`**，不能用 `https://`（站点不支持）
- **编码必须是 UTF-8**，不能出现 `charset=gbk`
- **禁止标记**：`charset=gbk`、`用户名 Username`、`注册 Register`、`发表回复 Post reply`、`<form`

### 5.4 生成命令

```bash
# 从 index.md 生成干净 HTML
python scripts/render_clean_forum_html.py data_sources/sobko_sources/forum_threads

# 修复编码问题
python scripts/normalize_forum_html_charset.py data_sources/sobko_sources/forum_threads

# 运行验证测试
python -m unittest discover -s tests -p 'test_pipeline.py'
```

### 5.5 Manifest 格式 (threads.jsonl)

每行一个 JSON 对象，必须包含：

```json
{
  "source_id": "forum_thread:536",
  "source_type": "forum_thread",
  "title": "标题",
  "canonical_url": "http://bbs.keinsci.com/thread-536-1-1.html",
  "markdown_path": "data_sources/sobko_sources/forum_threads/536/index.md",
  "html_path": "data_sources/sobko_sources/forum_threads/536/thread.html",
  "authority_level": "A",
  "image_count": 0,
  "software_tags": ["Gaussian", "ORCA"],
  "topic_tags": ["量子化学", "综述/教程/投稿经验"],
  "coverage": "browser_verified_full_thread_text",
  "source_provider": "wsl2_chrome_cdp_verified_session",
  "original_reply_count": 91,
  "confidence": 0.97
}
```

**注意**：`software_tags` 和 `topic_tags` 必须与 source registry 自动推断的标签完全一致（排序也要一致）。有效值来自 `sobko_mcp/common.py` 中的 `SOFTWARE_TAGS` 和 `TOPIC_TAGS`。

## 6. 线程分级标准

| 级别 | 条件 | 示例 |
|------|------|------|
| **A** | sobereva 亲笔长篇原创教程，持续更新，数万-数十万浏览 | DFT泛函选择、基组选择、TDDFT教程、Multiwfn系列 |
| **B** | sobereva 参与回答、专题工具帖、较短教程、答疑专帖 | 具体问题Q&A、工具脚本介绍、报错专帖 |

## 7. 已知巨帖（谨慎处理）

| TID | 标题 | 页数 | 说明 |
|-----|------|------|------|
| 10181 | 简单Multiwfn使用问题和波函数分析问题答疑专贴 | 106 | 46万浏览，Q&A巨帖，下载需 10+ 分钟 |
| 33965 | 简单量子化学问题答疑专帖 | ? | 量子化学版置顶Q&A |
| 806 | 简单量化问题答疑专帖 | ? | 老版Q&A |

AGENTS.md 规定：**Avoid huge megathreads unless a pagination/completeness plan is explicitly chosen.**

## 8. 工具脚本速查

| 脚本 | 位置 | 功能 |
|------|------|------|
| `dl_thread.sh` | `/tmp/dl_thread.sh` | 下载单个线程所有页面（纯文本） |
| `rex_final.sh` | `/tmp/rex_final.sh` | 重提取线程 + 静默下载图片 + 魔数校验 |
| `save_thread.js` | `/tmp/save_thread.js` | 将 /tmp 中的 JSON 数据写成 index.md |
| `dl_images_v2.sh` | `/tmp/dl_images_v2.sh` | 单独下载图片（使用 CDP 导航方式，会弹新标签⚠️） |

所有脚本都在 `/tmp` 下——**不污染项目工作区**。

### 典型工作流

```bash
# 1. 下载纯文本帖子（dl_thread.sh 自动提取所有页面）
bash /tmp/dl_thread.sh 536

# 2. 保存为 index.md
node /tmp/save_thread.js 536 "帖子标题" "日期" "版块" "topic标签" "入库理由"

# 3. 如有图片，下载附属图片（不动文本）
bash /tmp/rex_final.sh 536

# 4. 生成 HTML
python scripts/render_clean_forum_html.py data_sources/sobko_sources/forum_threads

# 5. 验证
python -m unittest discover -s tests -p 'test_pipeline.py'
```

## 9. 常见踩坑汇总

| 坑 | 现象 | 解决 |
|----|------|------|
| 用了 `https://` URL | SSL 错误或重定向 | 全部用 `http://` |
| 版块 ID 写错 | "指定的版块不存在" | 从首页导航栏提取真实 URL |
| 把 WAF 当版块不存在 | 盲目重试导致 IP 被封 | 读 body 内容精确判断 |
| 图片下载弹新标签 | 抢占用户桌面焦点 | 用 fetch() 静默下载 |
| 假图片混入 | `file *.jpg` 显示 HTML | 魔数校验，拒绝非图片文件 |
| manifest 缺 `software_tags` | 测试失败 | 从 registry 读出实际标签对齐 |
| .innerHTML 破坏正文 | 混入 HTML 标签导致排版乱 | 默认用 .innerText，图片只做附件 |
| 连续快速翻页 | WAF 拦截 | 每页 4-8 秒随机延迟 |
| 大帖中途失败 | 丢失已下载数据 | 每 3 页保存一次进度 |
| Chrome 弹附件窗口 | 累积多个标签导致导航混乱 | 定期关闭非论坛标签 |

## 10. 当前成果（2026-06-05）

- **35 个线程**，23 个 A 级，12 个 B 级
- **204 张附属图片**（14 个帖子含截图/附件，其中 6 个 Multiwfn 教程帖含大量截图）
- 覆盖 **4 个版块**：量子化学、波函数分析、分子模拟、第一性原理
- 所有 20 个 pipeline 测试通过
