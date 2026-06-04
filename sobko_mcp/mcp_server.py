"""Sobko 知识库 MCP server 封装。"""

from __future__ import annotations

import json
import sys
from typing import Any, Dict, Optional

from .config import build_layout, load_config
from .retriever import RetrievalEngine


class SobkoMcpServer:
    """内置 stdio JSON-RPC MCP server。

    功能目的：
        在没有官方 `mcp` Python 包时，仍能暴露 Sobko 的四个 MCP 工具。
    输入参数：
        初始化时自动加载配置和索引。
    返回值：
        提供 `serve_forever()` 事件循环。
    关键流程：
        读取 Content-Length framed JSON-RPC 消息，处理 initialize、tools/list、tools/call。
    可能报错或边界情况：
        单次工具调用失败会返回 JSON-RPC error，不让 server 进程直接退出。
    """

    def __init__(self) -> None:
        self.layout = build_layout()
        self.config = load_config()
        self.engine = RetrievalEngine(self.layout, self.config)

    def _tool_definitions(self) -> list[Dict[str, Any]]:
        """返回 MCP 工具定义。

        功能目的：
            让客户端通过 `tools/list` 发现 Sobko 可用能力。
        输入参数：
            无。
        返回值：
            MCP tool schema 列表。
        关键流程：
            固定暴露 search、fetch、get_image、trace_source 四个工具。
        可能报错或边界情况：
            schema 保持简单 JSON Schema，兼容内置和 FastMCP 两种 server。
        """

        return [
            {
                "name": "sobko_search",
                "description": "Search the Sobko knowledge base and return traceable evidence snippets.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "top_k": {"type": "integer", "default": 8},
                        "source_types": {"type": ["array", "null"], "items": {"type": "string"}},
                        "software": {"type": ["array", "null"], "items": {"type": "string"}},
                        "topics": {"type": ["array", "null"], "items": {"type": "string"}},
                        "authority_at_least": {"type": ["string", "null"]},
                        "include_images": {"type": "boolean", "default": True},
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "sobko_fetch",
                "description": "Fetch source or chunk context from Sobko with neighboring chunks.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "chunk_id": {"type": ["string", "null"]},
                        "source_id": {"type": ["string", "null"]},
                        "expand_prev_next": {"type": "integer", "default": 1},
                        "include_html_anchor": {"type": "boolean", "default": True},
                    },
                },
            },
            {
                "name": "sobko_get_image",
                "description": "Return local image path, caption, and nearby text for a known Sobko image_id.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "image_id": {"type": "string"},
                        "return_mode": {"type": "string", "default": "path"},
                    },
                    "required": ["image_id"],
                },
            },
            {
                "name": "sobko_trace_source",
                "description": "Trace authority level, local path, source URL, and lineage for a Sobko source or chunk.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "source_id": {"type": ["string", "null"]},
                        "chunk_id": {"type": ["string", "null"]},
                    },
                },
            },
        ]

    def _read_message(self) -> Optional[Dict[str, Any]]:
        """读取一条 framed JSON-RPC 消息。

        功能目的：
            实现 MCP stdio transport 的基础读入协议。
        输入参数：
            无，从 stdin 读取。
        返回值：
            JSON-RPC 消息字典；EOF 时返回 None。
        关键流程：
            读取 header，解析 Content-Length，再读取指定长度 body。
        可能报错或边界情况：
            非法 JSON 会抛出异常并由外层处理。
        """

        headers: Dict[str, str] = {}
        while True:
            line = sys.stdin.buffer.readline()
            if not line:
                return None
            if line in {b"\r\n", b"\n"}:
                break
            key, value = line.decode("utf-8").split(":", 1)
            headers[key.strip().lower()] = value.strip()
        content_length = int(headers.get("content-length", "0"))
        body = sys.stdin.buffer.read(content_length)
        if not body:
            return None
        return json.loads(body.decode("utf-8"))

    def _write_message(self, payload: Dict[str, Any]) -> None:
        """写出一条 framed JSON-RPC 消息。

        功能目的：
            实现 MCP stdio transport 的基础响应协议。
        输入参数：
            payload：响应对象。
        返回值：
            无。
        关键流程：
            先计算 UTF-8 body 字节长度，再写 Content-Length header 和 body。
        可能报错或边界情况：
            stdout 管道关闭时会抛出 BrokenPipeError，进程自然退出。
        """

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        header = f"Content-Length: {len(body)}\r\n\r\n".encode("utf-8")
        sys.stdout.buffer.write(header)
        sys.stdout.buffer.write(body)
        sys.stdout.buffer.flush()

    def _success(self, message_id: Any, result: Dict[str, Any]) -> None:
        """返回成功响应。"""

        self._write_message({"jsonrpc": "2.0", "id": message_id, "result": result})

    def _error(self, message_id: Any, code: int, message: str) -> None:
        """返回错误响应。"""

        self._write_message({"jsonrpc": "2.0", "id": message_id, "error": {"code": code, "message": message}})

    def _handle_tool_call(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """执行 MCP 工具调用。

        功能目的：
            将 MCP tool name 映射到 `RetrievalEngine` 方法。
        输入参数：
            name：工具名称。
            arguments：工具参数。
        返回值：
            MCP tool response 字典。
        关键流程：
            调用检索引擎后，同时返回 text content 和 structuredContent。
        可能报错或边界情况：
            未知工具抛出 `KeyError`，由外层包装为 JSON-RPC error。
        """

        if name == "sobko_search":
            payload = self.engine.search(
                query=arguments["query"],
                top_k=arguments.get("top_k"),
                source_types=arguments.get("source_types"),
                software=arguments.get("software"),
                topics=arguments.get("topics"),
                authority_at_least=arguments.get("authority_at_least"),
                include_images=arguments.get("include_images", True),
            ).__dict__
        elif name == "sobko_fetch":
            payload = self.engine.fetch(
                chunk_id=arguments.get("chunk_id"),
                source_id=arguments.get("source_id"),
                expand_prev_next=int(arguments.get("expand_prev_next", 1)),
                include_html_anchor=bool(arguments.get("include_html_anchor", True)),
            )
        elif name == "sobko_get_image":
            payload = self.engine.get_image(
                image_id=arguments["image_id"],
                return_mode=arguments.get("return_mode", "path"),
            )
        elif name == "sobko_trace_source":
            payload = self.engine.trace_source(
                source_id=arguments.get("source_id"),
                chunk_id=arguments.get("chunk_id"),
            )
        else:
            raise KeyError(f"未知工具：{name}")
        return {
            "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
            "structuredContent": payload,
            "isError": False,
        }

    def serve_forever(self) -> None:
        """启动内置 MCP 事件循环。

        功能目的：
            持续处理 MCP stdio 消息，直到 stdin EOF。
        输入参数：
            无。
        返回值：
            无。
        关键流程：
            分派 initialize、ping、tools/list、tools/call 和 initialized notification。
        可能报错或边界情况：
            单条消息异常会写 error；notification 没有 id 时不回包。
        """

        while True:
            message = self._read_message()
            if message is None:
                return
            method = message.get("method")
            message_id = message.get("id")
            try:
                if method == "initialize":
                    self._success(
                        message_id,
                        {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {"tools": {"listChanged": False}},
                            "serverInfo": {"name": self.config.mcp_server_name, "version": self.config.index_version},
                        },
                    )
                elif method == "notifications/initialized":
                    continue
                elif method == "ping":
                    self._success(message_id, {})
                elif method == "tools/list":
                    self._success(message_id, {"tools": self._tool_definitions()})
                elif method == "tools/call":
                    params = message.get("params", {})
                    result = self._handle_tool_call(params["name"], params.get("arguments", {}))
                    self._success(message_id, result)
                else:
                    if message_id is not None:
                        self._error(message_id, -32601, f"不支持的方法：{method}")
            except Exception as exc:  # pragma: no cover - server 需要在工具异常后继续存活
                if message_id is not None:
                    self._error(message_id, -32000, str(exc))


def build_fastmcp_server():
    """构建官方 FastMCP server。

    功能目的：
        在安装了官方 `mcp` 包的环境中使用更标准的 MCP server 实现。
    输入参数：
        无，内部自动加载配置和索引。
    返回值：
        `FastMCP` server 实例。
    关键流程：
        创建检索引擎单例并注册四个工具。
    可能报错或边界情况：
        `mcp` 包不可用时抛出 `ImportError`，启动脚本会回退到内置 server。
    """

    from mcp.server.fastmcp import FastMCP

    layout = build_layout()
    config = load_config()
    engine = RetrievalEngine(layout, config)
    server = FastMCP(
        name=config.mcp_server_name,
        instructions=(
            "Sobko evidence-first knowledge base built from Sobereva academic posts and the Multiwfn manual. "
            "Return traceable snippets, source lineage, and local paths. "
            "Do not synthesize unsupported scientific conclusions."
        ),
    )

    @server.tool(name="sobko_search", description="Search the Sobko knowledge base and return traceable evidence snippets.")
    def sobko_search(
        query: str,
        top_k: int = 8,
        source_types: list[str] | None = None,
        software: list[str] | None = None,
        topics: list[str] | None = None,
        authority_at_least: str | None = None,
        include_images: bool = True,
    ) -> Dict[str, Any]:
        """执行 Sobko 检索。"""

        return engine.search(
            query=query,
            top_k=top_k,
            source_types=source_types,
            software=software,
            topics=topics,
            authority_at_least=authority_at_least,
            include_images=include_images,
        ).__dict__

    @server.tool(name="sobko_fetch", description="Fetch source or chunk context from Sobko.")
    def sobko_fetch(
        chunk_id: str | None = None,
        source_id: str | None = None,
        expand_prev_next: int = 1,
        include_html_anchor: bool = True,
    ) -> Dict[str, Any]:
        """展开 source 或 chunk 上下文。"""

        return engine.fetch(
            chunk_id=chunk_id,
            source_id=source_id,
            expand_prev_next=expand_prev_next,
            include_html_anchor=include_html_anchor,
        )

    @server.tool(name="sobko_get_image", description="Return local image path, caption, and nearby text for a known image_id.")
    def sobko_get_image(image_id: str, return_mode: str = "path") -> Dict[str, Any]:
        """返回图片路径与邻近说明。"""

        return engine.get_image(image_id=image_id, return_mode=return_mode)

    @server.tool(name="sobko_trace_source", description="Trace authority level, local path, source URL, and lineage.")
    def sobko_trace_source(source_id: str | None = None, chunk_id: str | None = None) -> Dict[str, Any]:
        """追溯来源链路。"""

        return engine.trace_source(source_id=source_id, chunk_id=chunk_id)

    return server
