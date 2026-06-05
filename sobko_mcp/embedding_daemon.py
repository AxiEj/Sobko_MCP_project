"""Shared local embedding daemon for Sobko MCP clients."""

from __future__ import annotations

import argparse
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Tuple

from .config import build_layout, load_config
from .retriever import OllamaClient


class EmbeddingDaemonApp:
    """Small HTTP app that keeps one embedding model warm for many MCP clients."""

    def __init__(self, project_root: Path | None = None):
        self.layout = build_layout(project_root)
        self.config = load_config(self.layout.configs_dir / "default.json")
        self.client = OllamaClient(self.config, allow_daemon=False)
        self.lock = threading.Lock()

    def health(self) -> Tuple[int, Dict[str, Any]]:
        """Return daemon health without loading the heavyweight model."""

        ok, reason = self.client.embedding_available()
        return (
            200 if ok else 503,
            {
                "status": "ok" if ok else "error",
                "reason": reason,
                "provider": self.client._embedding_provider(),
                "model_name": self.client._embedding_model(),
            },
        )

    def embed(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Embed one string or a list of strings."""

        raw_input = payload.get("input", payload.get("texts"))
        if isinstance(raw_input, str):
            texts = [raw_input]
            single = True
        elif isinstance(raw_input, list) and all(isinstance(item, str) for item in raw_input):
            texts = raw_input
            single = False
        else:
            raise ValueError("请求体必须包含 input 字符串或字符串列表。")
        model_name = str(payload.get("model") or self.client._embedding_model())
        with self.lock:
            embeddings = self.client.embed_texts(texts, model=model_name)
        response: Dict[str, Any] = {
            "provider": self.client._embedding_provider(),
            "model_name": model_name,
            "embeddings": embeddings,
        }
        if single and embeddings:
            response["embedding"] = embeddings[0]
        return response


class EmbeddingDaemonHandler(BaseHTTPRequestHandler):
    """HTTP handler for the embedding daemon."""

    server: "EmbeddingDaemonServer"

    def _write_json(self, status: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path in {"/health", "/api/version", "/api/tags", "/api/ps"}:
            status, payload = self.server.app.health()
            if self.path == "/api/version":
                payload = payload | {"version": "sobko-embedding-daemon-v1"}
            elif self.path == "/api/tags":
                payload = payload | {"models": [{"name": payload.get("model_name")}]}
            elif self.path == "/api/ps":
                payload = payload | {"models": []}
            self._write_json(status, payload)
            return
        self._write_json(404, {"error": f"unknown endpoint: {self.path}"})

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        if self.path not in {"/api/embed", "/embed"}:
            self._write_json(404, {"error": f"unknown endpoint: {self.path}"})
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw) if raw else {}
            self._write_json(200, self.server.app.embed(payload))
        except Exception as exc:
            self._write_json(500, {"error": str(exc)})

    def log_message(self, fmt: str, *args: Any) -> None:
        """Keep daemon logs compact and out of JSON responses."""

        print(f"sobko-embedding-daemon: {fmt % args}", file=sys.stderr)


class EmbeddingDaemonServer(ThreadingHTTPServer):
    """Threading server carrying the shared daemon app."""

    def __init__(self, server_address: Tuple[str, int], app: EmbeddingDaemonApp):
        super().__init__(server_address, EmbeddingDaemonHandler)
        self.app = app


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Run the Sobko shared embedding daemon.")
    parser.add_argument("--host", default=None, help="Bind host; default comes from configs/default.json.")
    parser.add_argument("--port", type=int, default=None, help="Bind port; default comes from configs/default.json.")
    parser.add_argument("--project-root", default=None, help="Sobko project root; defaults to auto-discovery.")
    args = parser.parse_args(argv)

    project_root = Path(args.project_root).resolve() if args.project_root else None
    app = EmbeddingDaemonApp(project_root)
    host = args.host or app.config.embedding_daemon_bind_host
    port = args.port or app.config.embedding_daemon_bind_port
    server = EmbeddingDaemonServer((host, port), app)
    print(f"sobko-embedding-daemon listening on http://{host}:{port}", file=sys.stderr)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
