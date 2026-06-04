#!/usr/bin/env python
"""Sobko MCP stdio smoke test。"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _encode_message(payload: Dict[str, Any]) -> bytes:
    """编码 MCP framed JSON-RPC 消息。

    功能目的：
        生成符合 stdio MCP transport 的 Content-Length 消息。
    输入参数：
        payload：JSON-RPC 消息对象。
    返回值：
        可写入子进程 stdin 的字节串。
    关键流程：
        JSON UTF-8 编码后计算 body 长度，再拼接 header。
    可能报错或边界情况：
        payload 不可 JSON 序列化时会抛出 `TypeError`。
    """

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8") + body


def _read_message(proc: subprocess.Popen[bytes]) -> Dict[str, Any]:
    """从 MCP 子进程读取一条 framed JSON-RPC 消息。

    功能目的：
        验证 server 的 initialize、tools/list 和 tools/call 响应。
    输入参数：
        proc：MCP server 子进程。
    返回值：
        JSON-RPC 响应字典。
    关键流程：
        读取 header 到空行，再按 Content-Length 读取 body。
    可能报错或边界情况：
        子进程提前退出或 body 为空时抛出 `RuntimeError`。
    """

    if proc.stdout is None:
        raise RuntimeError("MCP 子进程 stdout 不可读。")
    headers: Dict[str, str] = {}
    while True:
        line = proc.stdout.readline()
        if not line:
            stderr = proc.stderr.read().decode("utf-8", errors="replace") if proc.stderr else ""
            raise RuntimeError(f"MCP 子进程无响应。stderr={stderr}")
        if line in {b"\r\n", b"\n"}:
            break
        key, value = line.decode("utf-8").split(":", 1)
        headers[key.strip().lower()] = value.strip()
    content_length = int(headers.get("content-length", "0"))
    body = proc.stdout.read(content_length)
    if not body:
        raise RuntimeError("MCP 响应 body 为空。")
    return json.loads(body.decode("utf-8"))


def _send(proc: subprocess.Popen[bytes], payload: Dict[str, Any]) -> Dict[str, Any]:
    """发送一条 MCP 请求并读取响应。

    功能目的：
        简化 smoke test 的请求/响应流程。
    输入参数：
        proc：MCP server 子进程。
        payload：请求对象。
    返回值：
        响应对象。
    关键流程：
        写入 framed message，flush 后读取一条响应。
    可能报错或边界情况：
        notification 不应使用本函数，因为 notification 没有响应。
    """

    if proc.stdin is None:
        raise RuntimeError("MCP 子进程 stdin 不可写。")
    proc.stdin.write(_encode_message(payload))
    proc.stdin.flush()
    return _read_message(proc)


def main() -> None:
    """脚本入口。

    功能目的：
        端到端验证 Sobko MCP server 至少能列出工具并完成一次检索。
    输入参数：
        无。
    返回值：
        无，失败时抛出 AssertionError 或 RuntimeError。
    关键流程：
        启动 server -> initialize -> tools/list -> tools/call(sobko_search) -> 校验结果。
    可能报错或边界情况：
        smoke test 默认禁用本地 FlagEmbedding reranker，避免模型加载影响协议测试。
    """

    env = os.environ.copy()
    env.setdefault("SOBKO_DISABLE_LOCAL_RERANKER", "1")
    env["SOBKO_FORCE_BUILTIN_MCP"] = "1"
    proc = subprocess.Popen(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "run_server.py")],
        cwd=str(PROJECT_ROOT),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
    try:
        initialize = _send(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "clientInfo": {"name": "sobko-smoke", "version": "1"},
                },
            },
        )
        assert initialize["result"]["serverInfo"]["name"] == "sobko-kb", initialize
        tools = _send(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tool_names = {item["name"] for item in tools["result"]["tools"]}
        expected = {"sobko_search", "sobko_fetch", "sobko_get_image", "sobko_trace_source"}
        assert tool_names == expected, tool_names
        search = _send(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "sobko_search",
                    "arguments": {"query": "ORCA TDDFT 空穴电子分析", "top_k": 5},
                },
            },
        )
        payload = search["result"]["structuredContent"]
        assert payload["results"], payload
        assert any(item["source_id"] == "blog_post:758" for item in payload["results"]), payload["results"]
        print(
            json.dumps(
                {
                    "tools": sorted(tool_names),
                    "top_result": payload["results"][0]["source_id"],
                    "effective_mode": payload["effective_mode"],
                    "backend_warnings": payload["backend_warnings"],
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)


if __name__ == "__main__":
    main()
