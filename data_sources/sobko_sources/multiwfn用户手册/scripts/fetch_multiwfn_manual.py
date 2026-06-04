#!/usr/bin/env python3
"""抓取 Multiwfn 用户手册并生成本地镜像与文本版。

功能目的:
- 下载 http://sobereva.com/multiwfn/Multiwfn_manual.html
- 镜像页面依赖的 CSS、SVG、字体等资源，保证本地离线浏览
- 从 HTML 中抽取可检索文本，导出 Markdown 版本

输入参数:
- 通过命令行参数控制输出目录、并发数以及是否强制覆盖

返回值:
- 无显式返回值；在输出目录生成 HTML、资源目录、Markdown 和 manifest

关键流程:
- 抓取 HTML 主页面
- 解析 HTML 中的 href/src/data 与 CSS 中的 url(...) 资源
- 并发下载资源到本地相同相对路径
- 解析每页文本块，导出为分页 Markdown

可能报错或边界情况:
- 网络超时、单个资源下载失败、HTML 结构变化导致文本抽取效果下降
- 页面是 PDF 转 HTML 格式，Markdown 版主要强调可检索，不追求原版式
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


MANUAL_URL = "http://sobereva.com/multiwfn/Multiwfn_manual.html"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X) Codex Multiwfn Manual Fetcher/1.0"
THREAD_LOCAL = threading.local()


def create_session() -> requests.Session:
    """创建带重试的请求会话。

    功能目的:
    - 提高资源下载阶段的稳定性，降低偶发超时和 5xx 错误的影响

    输入参数:
    - 无

    返回值:
    - 配置完成的 requests.Session

    关键流程:
    - 设置 UA
    - 对 HTTP/HTTPS 适配器启用有限重试

    可能报错或边界情况:
    - 远端持续不可达时，重试后仍会抛出异常
    """

    session = requests.Session()
    retry = Retry(
        total=4,
        backoff_factor=1.0,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET", "HEAD"),
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=16, pool_maxsize=16)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": USER_AGENT})
    return session


def get_session() -> requests.Session:
    """获取当前线程专属 Session。"""

    if not hasattr(THREAD_LOCAL, "session"):
        THREAD_LOCAL.session = create_session()
    return THREAD_LOCAL.session


def fetch_bytes(url: str, timeout: tuple[int, int] = (20, 90)) -> bytes:
    """抓取二进制内容。"""

    response = get_session().get(url, timeout=timeout)
    response.raise_for_status()
    return response.content


def fetch_text(url: str, timeout: tuple[int, int] = (20, 90)) -> str:
    """抓取文本内容并按页面声明编码解码。

    功能目的:
    - 减少 PDF 转 HTML 页面中因 requests 自动猜编码造成的乱码

    输入参数:
    - url: 目标地址
    - timeout: 连接/读取超时

    返回值:
    - 以 UTF-8 优先方式解码得到的文本

    关键流程:
    - 先取 bytes，再按 utf-8 解码；失败时回退 response.text 思路

    可能报错或边界情况:
    - 极少数资源若非文本内容，调用方应改用 fetch_bytes
    """

    data = fetch_bytes(url, timeout=timeout)
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace")


def normalize_text(text: str) -> str:
    """压缩空白字符。"""

    return re.sub(r"\s+", " ", text).strip()


def collect_html_assets(html: str, base_url: str) -> set[str]:
    """从 HTML 中收集相对资源路径。

    功能目的:
    - 找出手册页运行所需的 CSS、SVG、字体等直接资源

    输入参数:
    - html: 主页面 HTML
    - base_url: 主页面地址，用于判断资源所属范围

    返回值:
    - 相对资源路径集合

    关键流程:
    - 遍历 href/src/data 属性
    - 排除锚点、mailto、javascript 与站外链接

    可能报错或边界情况:
    - 若页面新增了通过脚本动态加载的资源，此方法不会捕捉到
    """

    soup = BeautifulSoup(html, "lxml")
    assets: set[str] = set()
    for tag in soup.find_all(True):
        for attr in ("href", "src", "data"):
            value = tag.get(attr)
            if not value:
                continue
            value = value.strip()
            if value.startswith(("http://", "https://")):
                # 手册中存在大量站外或站内绝对链接，它们属于参考链接而非页面运行依赖，
                # 不应被镜像成本地资源，否则会产生类似 http:/... 的脏路径。
                continue
            if value.startswith(("#", "mailto:", "javascript:")):
                continue
            assets.add(value)
    return assets


def collect_css_assets(css_text: str) -> set[str]:
    """从 CSS 文本中提取 url(...) 资源。"""

    assets: set[str] = set()
    for match in re.findall(r"url\(([^)]+)\)", css_text):
        ref = match.strip().strip('"').strip("'")
        if not ref or ref.startswith(("data:", "http://", "https://")):
            continue
        assets.add(ref)
    return assets


def save_file(path: Path, data: bytes) -> None:
    """保存二进制文件到本地。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def download_asset(asset_rel: str, output_dir: Path) -> dict[str, Any]:
    """下载单个相对资源。

    功能目的:
    - 将页面依赖文件落到与远端相同的相对路径结构

    输入参数:
    - asset_rel: 相对资源路径
    - output_dir: 根输出目录

    返回值:
    - 下载状态记录

    关键流程:
    - 拼接绝对 URL
    - 下载并写入到 output_dir / asset_rel

    可能报错或边界情况:
    - 若单个资源失效，返回 failed 而不是中断整体任务
    """

    asset_url = urljoin(MANUAL_URL, asset_rel)
    local_path = output_dir / asset_rel
    try:
        data = fetch_bytes(asset_url)
        save_file(local_path, data)
        return {"asset": asset_rel, "status": "ok", "size": len(data)}
    except Exception as exc:  # noqa: BLE001
        return {"asset": asset_rel, "status": "failed", "error": f"{type(exc).__name__}: {exc}"}


def extract_markdown_text(html: str) -> str:
    """从 PDF 转 HTML 页面抽取可检索的 Markdown 文本。

    功能目的:
    - 保留手册原文的主要文本信息，便于本地搜索与后续知识整理

    输入参数:
    - html: 主页面 HTML

    返回值:
    - 分页 Markdown 文本

    关键流程:
    - 逐个 stl_view 容器提取页面文本
    - 每页按 DOM 顺序拼接行文本
    - 加入分页标题，便于定位

    可能报错或边界情况:
    - 由于原始 HTML 是绝对定位文本，Markdown 版不保证视觉排版与原版一致
    """

    soup = BeautifulSoup(html, "lxml")
    pages = soup.select("div.stl_view")
    lines = [
        "# Multiwfn 用户手册",
        "",
        f"- 原始页面：<{MANUAL_URL}>",
        "- 说明：此 Markdown 版本强调可检索性；版式保真请优先打开同目录下的 `Multiwfn_manual.html`。",
        "",
    ]
    for page_index, page in enumerate(pages, start=1):
        text_lines: list[str] = []
        for block in page.select("div.stl_01"):
            text = normalize_text(block.get_text(" ", strip=True))
            if not text:
                continue
            text_lines.append(text)
        if not text_lines:
            continue
        lines.append(f"## Page {page_index}")
        lines.append("")
        merged = []
        last = None
        for text in text_lines:
            if text == last:
                continue
            merged.append(text)
            last = text
        lines.extend(merged)
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_args() -> argparse.Namespace:
    """解析命令行参数。"""

    parser = argparse.ArgumentParser(description="抓取 Multiwfn 用户手册并生成本地镜像")
    parser.add_argument(
        "--output-dir",
        default=str(Path(__file__).resolve().parents[1]),
        help="输出目录，默认脚本上级目录",
    )
    parser.add_argument("--workers", type=int, default=6, help="资源下载并发数，默认 6")
    parser.add_argument("--force", action="store_true", help="强制删除旧输出后重新下载")
    return parser.parse_args()


def main() -> int:
    """脚本入口。"""

    args = parse_args()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    html_path = output_dir / "Multiwfn_manual.html"
    markdown_path = output_dir / "Multiwfn_manual.md"
    manifest_path = output_dir / "manifest.json"
    assets_dir = output_dir / "Multiwfn_manual_files"

    if args.force and assets_dir.exists():
        shutil.rmtree(assets_dir)

    html_text = fetch_text(MANUAL_URL)
    html_path.write_text(html_text, encoding="utf-8")

    html_assets = collect_html_assets(html_text, MANUAL_URL)
    css_assets = {asset for asset in html_assets if asset.endswith(".css")}
    all_assets = set(html_assets)
    for css_asset in css_assets:
        css_url = urljoin(MANUAL_URL, css_asset)
        css_text = fetch_text(css_url)
        all_assets.update({f"{Path(css_asset).parent}/{ref}" if "/" not in ref else ref for ref in collect_css_assets(css_text)})

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {
            executor.submit(download_asset, asset_rel, output_dir): asset_rel
            for asset_rel in sorted(all_assets)
        }
        for index, future in enumerate(as_completed(future_map), start=1):
            result = future.result()
            results.append(result)
            print(
                f"[manual] {index:04d}/{len(future_map)} asset={result['asset']} status={result['status']}",
                flush=True,
            )

    markdown_text = extract_markdown_text(html_text)
    markdown_path.write_text(markdown_text, encoding="utf-8")

    manifest = {
        "url": MANUAL_URL,
        "html_path": html_path.name,
        "markdown_path": markdown_path.name,
        "asset_root": assets_dir.name,
        "asset_count": len(all_assets),
        "download_ok": sum(1 for item in results if item["status"] == "ok"),
        "download_failed": sum(1 for item in results if item["status"] != "ok"),
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
