"""Sobko MCP 检索引擎。"""

from __future__ import annotations

import contextlib
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence
from urllib import error, request

from .common import AUTHORITY_ORDER, authority_meets, read_json, read_jsonl, tokenize
from .config import ProjectLayout, RagConfig, resolve_portable_path


def _normalize_scores(scores: Dict[str, float]) -> Dict[str, float]:
    """将一组分数归一化到 0-1。

    功能目的：
        让 BM25、embedding 和 rerank 分数可以稳定融合。
    输入参数：
        scores：`chunk_id -> 原始分数` 映射。
    返回值：
        同样 key 的归一化分数。
    关键流程：
        使用 min-max 归一化；如果所有分数相同则统一置为 1。
    可能报错或边界情况：
        空输入返回空字典，避免后续流程中断。
    """

    if not scores:
        return {}
    values = list(scores.values())
    min_value = min(values)
    max_value = max(values)
    if math.isclose(min_value, max_value):
        return {key: 1.0 for key in scores}
    return {key: (value - min_value) / (max_value - min_value) for key, value in scores.items()}


def _dot_product(left: Sequence[float], right: Sequence[float]) -> float:
    """计算两个等长向量的点积。

    功能目的：
        支持余弦相似度计算。
    输入参数：
        left/right：两个数值序列。
    返回值：
        点积浮点值。
    关键流程：
        使用 `zip` 逐项相乘求和。
    可能报错或边界情况：
        如果向量长度不同，`zip` 会按较短长度计算；上层索引构建保证维度一致。
    """

    return float(sum(a * b for a, b in zip(left, right)))


def _vector_norm(values: Sequence[float]) -> float:
    """计算向量 L2 范数。

    功能目的：
        支持余弦相似度归一化。
    输入参数：
        values：数值序列。
    返回值：
        L2 范数。
    关键流程：
        对平方和开方。
    可能报错或边界情况：
        空向量返回 0。
    """

    return math.sqrt(sum(item * item for item in values))


def _cosine_similarity(left: Sequence[float], right: Sequence[float]) -> float:
    """计算余弦相似度。

    功能目的：
        将 query embedding 与 chunk embedding 转成 dense 检索分数。
    输入参数：
        left/right：两个 embedding 向量。
    返回值：
        余弦相似度。
    关键流程：
        点积除以两个向量范数乘积。
    可能报错或边界情况：
        任一向量范数接近 0 时返回 0，避免除零。
    """

    denominator = _vector_norm(left) * _vector_norm(right)
    if denominator <= 1e-12:
        return 0.0
    return _dot_product(left, right) / denominator


@dataclass
class SearchResult:
    """封装一次检索结果。

    功能目的：
        让 MCP 返回包含检索模式、后端状态和证据结果的结构化对象。
    输入参数：
        由 `RetrievalEngine.search` 构造。
    返回值：
        dataclass 实例，可通过 `.__dict__` JSON 化。
    关键流程：
        保存 requested/effective mode，便于用户判断是否发生 dense 或 rerank 降级。
    可能报错或边界情况：
        无结果时 `results` 为空列表，不抛异常。
    """

    query: str
    requested_mode: str
    effective_mode: str
    embedding_available: bool
    rerank_available: bool
    backend_warnings: List[str]
    results: List[Dict[str, Any]]
    index_version: str


class OllamaClient:
    """Embedding / rerank API 客户端。

    功能目的：
        支持用户通过配置填写 embedding 与 rerank API 端口；embedding 支持 Ollama 和 OpenAI，
        rerank 继续兼容 Ollama 的 `/api/rerank` 形态。
    输入参数：
        config：Sobko RAG 配置。
    返回值：
        `OllamaClient` 实例。
    关键流程：
        对 Ollama embedding 与 rerank 分别维护候选 base URL；OpenAI embedding 直接调用 HTTPS API。
    可能报错或边界情况：
        服务不可达、API key 缺失、模型缺失、接口不存在或 JSON 形状不兼容时抛出 `RuntimeError`，上层会降级。
    """

    def __init__(self, config: RagConfig, *, allow_daemon: bool = True):
        self.config = config
        self.allow_daemon = allow_daemon
        self.timeout = max(10, config.request_timeout)
        self._embedding_base_url: str | None = None
        self._rerank_base_url: str | None = None
        self._embedding_ping_status: Optional[tuple[bool, str]] = None
        self._rerank_ping_status: Optional[tuple[bool, str]] = None
        self._embedding_daemon_status: Optional[tuple[bool, str]] = None
        self._local_embedding_tokenizer = None
        self._local_embedding_model = None
        self._local_embedding_model_name: str | None = None
        self._local_embedding_device: str | None = None

    def _candidate_base_urls(self, kind: str) -> List[str]:
        """返回指定 API 类型的候选 base URL。

        功能目的：
            支持主地址和 fallback 地址，并允许用环境变量临时覆盖端口。
        输入参数：
            kind：`embedding` 或 `rerank`。
        返回值：
            去重后的 base URL 列表。
        关键流程：
            环境变量优先，然后是配置主地址，再是配置 fallback。
        可能报错或边界情况：
            空字符串会被过滤。
        """

        if kind == "embedding":
            env_value = os.environ.get("SOBKO_EMBEDDING_API_BASE_URL")
            configured = [self.config.embedding_api_base_url, *self.config.embedding_fallback_base_urls]
        elif kind == "rerank":
            env_value = os.environ.get("SOBKO_RERANK_API_BASE_URL")
            configured = [self.config.rerank_api_base_url, *self.config.rerank_fallback_base_urls]
        else:
            raise ValueError(f"未知 API 类型：{kind}")
        urls: List[str] = []
        for item in [env_value, *configured]:
            if item:
                normalized = item.rstrip("/")
                if normalized and normalized not in urls:
                    urls.append(normalized)
        return urls

    def _embedding_provider(self) -> str:
        """返回当前 embedding provider。

        功能目的：
            允许通过 `SOBKO_EMBEDDING_PROVIDER` 临时覆盖配置，便于同一迁移包在 local_hf/Ollama/OpenAI 间切换。
        输入参数：
            无。
        返回值：
            小写 provider 名称。
        关键流程：
            环境变量优先，否则使用配置文件。
        可能报错或边界情况：
            空字符串会退回配置值。
        """

        return (os.environ.get("SOBKO_EMBEDDING_PROVIDER") or self.config.embedding_provider).strip().lower()

    def _embedding_model(self, explicit_model: Optional[str] = None) -> str:
        """返回当前 embedding 模型名。"""

        return explicit_model or os.environ.get("SOBKO_EMBEDDING_MODEL") or self.config.embedding_model

    def _embedding_dimensions(self) -> int | None:
        """返回 OpenAI embedding dimensions 覆盖值。"""

        env_value = os.environ.get("SOBKO_EMBEDDING_DIMENSIONS")
        if env_value:
            return int(env_value)
        return self.config.embedding_dimensions

    def _env_bool(self, name: str, default: bool) -> bool:
        """Parse a boolean environment override."""

        value = os.environ.get(name)
        if value is None:
            return default
        return value.strip().lower() in {"1", "true", "yes", "on"}

    def _embedding_daemon_enabled(self) -> bool:
        """Return whether local_hf embeddings should prefer the shared daemon."""

        if not self.allow_daemon:
            return False
        return self._env_bool("SOBKO_EMBEDDING_DAEMON_ENABLED", bool(self.config.embedding_daemon_enabled))

    def _embedding_daemon_required(self) -> bool:
        """Return whether local_hf embeddings must use the shared daemon."""

        return self._env_bool("SOBKO_EMBEDDING_DAEMON_REQUIRED", bool(self.config.embedding_daemon_required))

    def _embedding_daemon_autostart(self) -> bool:
        """Return whether MCP may start the shared embedding daemon when absent."""

        return self._env_bool("SOBKO_EMBEDDING_DAEMON_AUTOSTART", bool(self.config.embedding_daemon_autostart))

    def _embedding_daemon_base_url(self) -> str:
        """Return the shared embedding daemon base URL."""

        return (os.environ.get("SOBKO_EMBEDDING_DAEMON_URL") or self.config.embedding_daemon_base_url).rstrip("/")

    def _daemon_url(self, endpoint: str) -> str:
        """Join daemon base URL and endpoint."""

        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        return f"{self._embedding_daemon_base_url()}{normalized_endpoint}"

    def _embedding_daemon_available(self) -> tuple[bool, str]:
        """Check whether the shared embedding daemon is reachable."""

        if not self._embedding_daemon_enabled():
            return False, "embedding daemon disabled"
        if self._embedding_daemon_status and self._embedding_daemon_status[0]:
            return self._embedding_daemon_status
        ok, reason = self._probe_embedding_daemon()
        if ok:
            return True, reason
        if self._embedding_daemon_autostart():
            start_reason = self._start_embedding_daemon()
            ok, reason = self._probe_embedding_daemon(wait_seconds=8)
            if ok:
                return True, reason
            return False, f"{reason}; autostart={start_reason}"
        return False, reason

    def _probe_embedding_daemon(self, *, wait_seconds: float = 0) -> tuple[bool, str]:
        """Probe daemon health, optionally waiting for startup."""

        deadline = time.time() + max(0.0, wait_seconds)
        last_error = "unknown"
        while True:
            try:
                with request.urlopen(self._daemon_url("/health"), timeout=2) as response:
                    status_code = response.status
                    text = response.read().decode("utf-8")
                if status_code != 200:
                    last_error = f"HTTP {status_code}"
                else:
                    data = json.loads(text)
                    if data.get("status") == "ok":
                        self._embedding_daemon_status = (True, "ok")
                        return self._embedding_daemon_status
                    last_error = f"health status={data.get('status')}"
            except Exception as exc:
                last_error = str(exc)
            if time.time() >= deadline:
                self._embedding_daemon_status = None
                return False, last_error
            time.sleep(0.25)

    def _start_embedding_daemon(self) -> str:
        """Start the shared embedding daemon in the project directory."""

        try:
            project_root = Path(__file__).resolve().parents[1]
            logs_dir = project_root / ".omx" / "logs"
            state_dir = project_root / ".omx" / "state"
            logs_dir.mkdir(parents=True, exist_ok=True)
            state_dir.mkdir(parents=True, exist_ok=True)
            log_path = logs_dir / "sobko-embedding-daemon.log"
            pid_path = state_dir / "sobko-embedding-daemon.pid"
            command = [sys.executable, str(project_root / "scripts" / "run_embedding_daemon.py")]
            with log_path.open("ab") as log_handle:
                proc = subprocess.Popen(
                    command,
                    cwd=str(project_root),
                    stdin=subprocess.DEVNULL,
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
            pid_path.write_text(str(proc.pid), encoding="utf-8")
            return f"started pid={proc.pid}"
        except Exception as exc:
            return f"failed: {exc}"

    def embedding_available(self) -> tuple[bool, str]:
        """检查 embedding provider 是否具备最小可调用条件。

        功能目的：
            构建 dense 索引前快速判断后端是否可用，避免无意义地遍历全部 chunk。
        输入参数：
            无。
        返回值：
            `(是否可用, 原因)`。
        关键流程：
            Ollama 走原 ping 逻辑；OpenAI 只检查 API key 是否存在；local_hf 检查 transformers/torch 是否存在。
        可能报错或边界情况：
            OpenAI key 不会被打印，错误信息只说明缺少环境变量。
        """

        provider = self._embedding_provider()
        if provider == "ollama":
            return self._ping("embedding")
        if provider == "openai":
            if os.environ.get("SOBKO_OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY"):
                return True, "ok"
            return False, "OpenAI embedding 需要设置 SOBKO_OPENAI_API_KEY 或 OPENAI_API_KEY。"
        if provider in {"local_hf", "local"}:
            if self._embedding_daemon_enabled():
                ok, reason = self._embedding_daemon_available()
                if ok:
                    return True, "ok"
                if self._embedding_daemon_required():
                    return False, f"embedding daemon required but unavailable: {reason}"
            try:
                import torch  # noqa: F401
                from transformers import AutoModel, AutoTokenizer  # noqa: F401

                return True, "ok"
            except Exception as exc:
                return False, f"local_hf embedding 需要可导入 transformers 和 torch: {exc}"
        return False, f"暂不支持 embedding_provider={provider}"

    def _build_url(self, base_url: str, endpoint: str) -> str:
        """拼接 API URL。

        功能目的：
            同时兼容 base URL 写到服务根和写到 `/api` 的两种配置方式。
        输入参数：
            base_url：API 服务基础地址。
            endpoint：接口路径，例如 `/api/embed`。
        返回值：
            完整 URL。
        关键流程：
            如果 endpoint 已是绝对 URL 则直接返回；否则处理 `/api` 的重复或缺失。
        可能报错或边界情况：
            endpoint 为空时会生成 base URL 本身，调用方不应传空 endpoint。
        """

        if endpoint.startswith("http://") or endpoint.startswith("https://"):
            return endpoint
        normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
        if base_url.endswith("/api") and normalized_endpoint.startswith("/api/"):
            return f"{base_url}{normalized_endpoint[4:]}"
        if not base_url.endswith("/api") and not normalized_endpoint.startswith("/api/"):
            return f"{base_url}/api{normalized_endpoint}"
        return f"{base_url}{normalized_endpoint}"

    def _ping(self, kind: str) -> tuple[bool, str]:
        """检查 API 服务是否可用。

        功能目的：
            在真正请求 embedding/rerank 前确认服务地址可访问，并缓存成功地址。
        输入参数：
            kind：`embedding` 或 `rerank`。
        返回值：
            `(是否可用, 原因)`。
        关键流程：
            对候选地址依次请求 `/api/version`、`/api/tags`、`/api/ps`，任一 200 即认为服务可用。
        可能报错或边界情况：
            这里不检查具体模型是否存在，模型错误会在 POST 时暴露。
        """

        if kind == "embedding" and self._embedding_ping_status is not None:
            return self._embedding_ping_status
        if kind == "rerank" and self._rerank_ping_status is not None:
            return self._rerank_ping_status
        last_error = "unknown"
        for base_url in self._candidate_base_urls(kind):
            for endpoint in ["/api/version", "/api/tags", "/api/ps"]:
                try:
                    with request.urlopen(self._build_url(base_url, endpoint), timeout=8) as response:
                        status_code = response.status
                    if status_code == 200:
                        if kind == "embedding":
                            self._embedding_base_url = base_url
                            self._embedding_ping_status = (True, "ok")
                            return self._embedding_ping_status
                        self._rerank_base_url = base_url
                        self._rerank_ping_status = (True, "ok")
                        return self._rerank_ping_status
                    last_error = f"{base_url}: HTTP {status_code}"
                    if status_code != 404:
                        break
                except Exception as exc:
                    last_error = f"{base_url}: {exc}"
                    break
        if kind == "embedding":
            self._embedding_ping_status = (False, last_error)
            return self._embedding_ping_status
        self._rerank_ping_status = (False, last_error)
        return self._rerank_ping_status

    def _post_json(self, kind: str, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """发送 JSON POST 请求。

        功能目的：
            使用标准库完成 HTTP JSON 调用，避免把 `requests` 作为硬依赖。
        输入参数：
            kind：`embedding` 或 `rerank`。
            endpoint：接口路径。
            payload：请求体。
        返回值：
            JSON 响应字典。
        关键流程：
            ping 成功后使用缓存 base URL；HTTP 非 200 或非法 JSON 都转成 `RuntimeError`。
        可能报错或边界情况：
            Ollama 旧版本没有 `/api/rerank` 时会返回 404，上层会记录 warning 并降级。
        """

        body = json.dumps(payload).encode("utf-8")
        ok, reason = self._ping(kind)
        if not ok:
            raise RuntimeError(f"Ollama {kind} 服务不可用: {reason}")

        # 某些反向代理可以通过 /api/version，但在 POST /api/embed 时偶发断流。
        # 因此 POST 阶段不能只相信 ping 选出的第一个地址，而要继续尝试 fallback。
        cached_base_url = self._embedding_base_url if kind == "embedding" else self._rerank_base_url
        candidate_urls: List[str] = []
        for item in [cached_base_url, *self._candidate_base_urls(kind)]:
            if item and item not in candidate_urls:
                candidate_urls.append(item)

        last_error = "unknown"
        for base_url in candidate_urls:
            url = self._build_url(base_url, endpoint)
            http_request = request.Request(
                url,
                data=body,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            try:
                with request.urlopen(http_request, timeout=self.timeout) as response:
                    text = response.read().decode("utf-8")
                data = json.loads(text)
                if kind == "embedding":
                    self._embedding_base_url = base_url
                else:
                    self._rerank_base_url = base_url
                return data
            except error.HTTPError as exc:
                detail = exc.read().decode("utf-8", errors="replace")[:240]
                last_error = f"{base_url} {endpoint} HTTP {exc.code}: {detail}"
            except json.JSONDecodeError as exc:
                last_error = f"{base_url} {endpoint} 返回非法 JSON: {exc}"
            except Exception as exc:
                last_error = f"{base_url} {endpoint}: {exc}"
        raise RuntimeError(f"调用 Ollama {endpoint} 失败: {last_error}")

    def _post_openai_embeddings(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """调用 OpenAI embeddings API。

        功能目的：
            让没有 Ollama 的环境可以用 OpenAI embedding 模型构建和查询 dense 索引。
        输入参数：
            payload：OpenAI `/v1/embeddings` 请求体。
        返回值：
            JSON 响应字典。
        关键流程：
            从 `SOBKO_OPENAI_API_KEY` 或 `OPENAI_API_KEY` 读取密钥，使用标准库发 HTTPS JSON 请求。
        可能报错或边界情况：
            缺少 API key、HTTP 非 2xx 或响应不是 JSON 都抛出 `RuntimeError`，上层降级。
        """

        api_key = os.environ.get("SOBKO_OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OpenAI embedding 需要设置 SOBKO_OPENAI_API_KEY 或 OPENAI_API_KEY。")
        base_url = (
            os.environ.get("SOBKO_EMBEDDING_API_BASE_URL")
            or os.environ.get("SOBKO_OPENAI_BASE_URL")
            or os.environ.get("OPENAI_BASE_URL")
            or self.config.embedding_api_base_url
            or "https://api.openai.com"
        ).rstrip("/")
        endpoint = os.environ.get("SOBKO_EMBEDDING_API_ENDPOINT") or self.config.embedding_api_endpoint or "/v1/embeddings"
        if endpoint.startswith(("http://", "https://")):
            url = endpoint
        else:
            normalized_endpoint = endpoint if endpoint.startswith("/") else f"/{endpoint}"
            if base_url.endswith("/v1") and normalized_endpoint.startswith("/v1/"):
                url = f"{base_url}{normalized_endpoint[3:]}"
            else:
                url = f"{base_url}{normalized_endpoint}"
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        if os.environ.get("OPENAI_ORG_ID"):
            headers["OpenAI-Organization"] = os.environ["OPENAI_ORG_ID"]
        if os.environ.get("OPENAI_PROJECT"):
            headers["OpenAI-Project"] = os.environ["OPENAI_PROJECT"]
        http_request = request.Request(url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                text = response.read().decode("utf-8")
            return json.loads(text)
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:240]
            raise RuntimeError(f"OpenAI embeddings HTTP {exc.code}: {detail}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"OpenAI embeddings 返回非法 JSON: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"调用 OpenAI embeddings 失败: {exc}") from exc

    def _post_daemon_embeddings(self, texts: Sequence[str], model_name: str) -> List[List[float]]:
        """Call the shared local embedding daemon."""

        body = json.dumps({"model": model_name, "input": list(texts)}).encode("utf-8")
        http_request = request.Request(
            self._daemon_url("/api/embed"),
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(http_request, timeout=self.timeout) as response:
                text = response.read().decode("utf-8")
            data = json.loads(text)
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:240]
            raise RuntimeError(f"embedding daemon HTTP {exc.code}: {detail}") from exc
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"embedding daemon 返回非法 JSON: {exc}") from exc
        except Exception as exc:
            raise RuntimeError(f"调用 embedding daemon 失败: {exc}") from exc
        if isinstance(data.get("embeddings"), list):
            return data["embeddings"]
        if isinstance(data.get("embedding"), list):
            return [data["embedding"]]
        raise RuntimeError("embedding daemon 返回格式不兼容，缺少 embeddings/embedding 字段。")

    def _embed_texts_local_hf(self, texts: Sequence[str], model_name: str) -> List[List[float]]:
        """使用本地 HuggingFace encoder 生成 embedding。

        功能目的：
            让没有 Ollama、没有 OpenAI API key 的环境仍可构建和查询 dense 索引。
        输入参数：
            texts：待编码文本列表。
            model_name：HuggingFace 模型名或本地模型目录。
        返回值：
            embedding 向量列表。
        关键流程：
            惰性加载 tokenizer/model -> tokenizer batch -> encoder forward -> CLS/mean pooling -> L2 normalize。
        可能报错或边界情况：
            模型未下载且无法访问 HuggingFace 时会抛出明确错误，上层自动降级 BM25。
        """

        try:
            import torch
            from transformers import AutoModel, AutoTokenizer
            from transformers.utils import logging as transformers_logging
        except Exception as exc:
            raise RuntimeError(f"local_hf embedding 需要安装 transformers 和 torch: {exc}") from exc

        if (
            self._local_embedding_tokenizer is None
            or self._local_embedding_model is None
            or self._local_embedding_model_name != model_name
        ):
            try:
                os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
                os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
                transformers_logging.set_verbosity_error()
                with open(os.devnull, "w", encoding="utf-8") as devnull:
                    with contextlib.redirect_stdout(devnull), contextlib.redirect_stderr(devnull):
                        self._local_embedding_tokenizer = AutoTokenizer.from_pretrained(model_name)
                        self._local_embedding_model = AutoModel.from_pretrained(model_name)
                        self._local_embedding_model_name = model_name
            except Exception as exc:
                raise RuntimeError(f"加载本地 embedding 模型失败：{model_name}: {exc}") from exc
            requested_device = os.environ.get("SOBKO_LOCAL_EMBEDDING_DEVICE")
            if requested_device:
                self._local_embedding_device = requested_device
            else:
                self._local_embedding_device = "cuda" if torch.cuda.is_available() else "cpu"
            self._local_embedding_model.to(self._local_embedding_device)
            self._local_embedding_model.eval()

        configured_max_length = self.config.local_embedding_max_length
        tokenizer_max_length = getattr(self._local_embedding_tokenizer, "model_max_length", None)
        if isinstance(tokenizer_max_length, int) and tokenizer_max_length > 100_000:
            tokenizer_max_length = None
        max_length = int(
            os.environ.get("SOBKO_LOCAL_EMBEDDING_MAX_LENGTH")
            or configured_max_length
            or tokenizer_max_length
            or 512
        )
        pooling = os.environ.get("SOBKO_LOCAL_EMBEDDING_POOLING", "cls").strip().lower()
        encoded = self._local_embedding_tokenizer(
            list(texts),
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        encoded = {key: value.to(self._local_embedding_device) for key, value in encoded.items()}
        with torch.no_grad():
            output = self._local_embedding_model(**encoded)
            hidden = output.last_hidden_state
            if pooling == "mean":
                mask = encoded["attention_mask"].unsqueeze(-1).expand(hidden.size()).float()
                pooled = (hidden * mask).sum(dim=1) / mask.sum(dim=1).clamp(min=1e-12)
            else:
                pooled = hidden[:, 0]
            pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
        return [[float(value) for value in row] for row in pooled.cpu().tolist()]

    def embed_texts(self, texts: Sequence[str], model: Optional[str] = None) -> List[List[float]]:
        """批量获取文本 embedding。

        功能目的：
            支持构建 dense 索引和实时 query embedding。
        输入参数：
            texts：待编码文本列表。
            model：可选模型名；为空时使用配置中的 `embedding_model`。
        返回值：
            embedding 向量列表。
        关键流程：
            POST 到配置的 embedding endpoint，并兼容 `embeddings` 与单条 `embedding` 字段。
        可能报错或边界情况：
            返回条数与输入条数不一致时由调用方在构建阶段发现。
        """

        provider = self._embedding_provider()
        if provider in {"local_hf", "local"}:
            model_name = self._embedding_model(model)
            if self._embedding_daemon_enabled():
                ok, reason = self._embedding_daemon_available()
                if ok:
                    try:
                        return self._post_daemon_embeddings(texts, model_name)
                    except Exception as exc:
                        self._embedding_daemon_status = None
                        if self._embedding_daemon_required():
                            raise RuntimeError(f"共享 embedding daemon 不可用: {exc}") from exc
                elif self._embedding_daemon_required():
                    raise RuntimeError(f"共享 embedding daemon 不可用: {reason}")
            return self._embed_texts_local_hf(texts, model_name)
        if provider == "openai":
            payload: Dict[str, Any] = {
                "model": self._embedding_model(model),
                "input": list(texts),
                "encoding_format": "float",
            }
            dimensions = self._embedding_dimensions()
            if dimensions:
                payload["dimensions"] = dimensions
            data = self._post_openai_embeddings(payload)
            records = data.get("data")
            if not isinstance(records, list):
                raise RuntimeError("OpenAI embeddings 返回格式不兼容，缺少 data 列表。")
            ordered = sorted(records, key=lambda item: int(item.get("index", 0)))
            embeddings = [item.get("embedding") for item in ordered]
            if not all(isinstance(item, list) for item in embeddings):
                raise RuntimeError("OpenAI embeddings 返回格式不兼容，缺少 embedding 向量。")
            return embeddings

        if provider != "ollama":
            raise RuntimeError(f"暂不支持 embedding_provider={provider}")
        data = self._post_json(
            "embedding",
            self.config.embedding_api_endpoint,
            {"model": self._embedding_model(model), "input": list(texts)},
        )
        if isinstance(data.get("embeddings"), list):
            return data["embeddings"]
        if isinstance(data.get("embedding"), list):
            return [data["embedding"]]
        raise RuntimeError("embedding API 返回格式不兼容，缺少 embeddings/embedding 字段。")

    def rerank(self, query: str, documents: Sequence[str], model: Optional[str] = None) -> List[float]:
        """调用 rerank API。

        功能目的：
            对初筛候选 chunk 做相关性重排。
        输入参数：
            query：用户查询。
            documents：候选 chunk 文本。
            model：可选 rerank 模型名。
        返回值：
            与 documents 等长的分数列表。
        关键流程：
            POST 到配置的 rerank endpoint，并解析常见 `results[index, score]` 形状。
        可能报错或边界情况：
            Ollama 当前版本可能没有 `/api/rerank`，调用方会自动降级。
        """

        if self.config.rerank_provider.lower() != "ollama":
            raise RuntimeError(f"暂不支持 rerank_provider={self.config.rerank_provider}")
        payload = {
            "model": model or self.config.rerank_model,
            "query": query,
            "documents": list(documents),
            "top_n": len(documents),
        }
        data = self._post_json("rerank", self.config.rerank_api_endpoint, payload)
        results = data.get("results")
        if not isinstance(results, list):
            raise RuntimeError("rerank API 返回格式不兼容，缺少 results 列表。")
        scores = [0.0] * len(documents)
        for item in results:
            index = int(item.get("index", -1))
            if 0 <= index < len(scores):
                scores[index] = float(item.get("relevance_score", item.get("score", 0.0)))
        return scores


class FlagEmbeddingReranker:
    """本地 FlagEmbedding reranker 封装。

    功能目的：
        在本机依赖和模型可用时优先使用本地 reranker，减少对远程 `/api/rerank` 的依赖。
    输入参数：
        config：Sobko RAG 配置。
    返回值：
        `FlagEmbeddingReranker` 实例。
    关键流程：
        首次使用时惰性加载模型，失败原因会缓存，避免每次查询重复加载。
    可能报错或边界情况：
        设置 `SOBKO_DISABLE_LOCAL_RERANKER=1` 可跳过本地模型，便于测试远程 rerank 降级。
    """

    def __init__(self, config: RagConfig):
        self.config = config
        self._model = None
        self._load_error: Optional[str] = None

    def available(self) -> tuple[bool, str]:
        """尝试加载本地 reranker。

        功能目的：
            判断本地 reranker 是否可用于当前查询。
        输入参数：
            无。
        返回值：
            `(是否可用, 原因)`。
        关键流程：
            先检查环境变量禁用开关，再尝试导入并初始化 `FlagReranker`。
        可能报错或边界情况：
            包未安装、模型未缓存、设备不可用都会返回 False，不阻断检索。
        """

        if os.environ.get("SOBKO_DISABLE_LOCAL_RERANKER") == "1":
            return False, "SOBKO_DISABLE_LOCAL_RERANKER=1"
        if self._model is not None:
            return True, "ok"
        if self._load_error is not None:
            return False, self._load_error
        try:
            from FlagEmbedding import FlagReranker

            self._model = FlagReranker(
                self.config.flag_reranker_model_name,
                use_fp16=self.config.flag_reranker_use_fp16,
            )
            return True, "ok"
        except Exception as exc:  # pragma: no cover - 依赖和模型状态取决于用户环境
            self._load_error = str(exc)
            return False, self._load_error

    def score(self, query: str, documents: Sequence[str]) -> List[float]:
        """对候选文档打 rerank 分数。

        功能目的：
            将 query-document pairs 转成可融合的相关性分数。
        输入参数：
            query：用户查询。
            documents：候选 chunk 文本。
        返回值：
            分数列表。
        关键流程：
            调用 FlagEmbedding 的 `compute_score`，并按配置决定是否 normalize。
        可能报错或边界情况：
            模型不可用时抛出 `RuntimeError`，上层会尝试 Ollama rerank 或降级。
        """

        ok, reason = self.available()
        if not ok or self._model is None:
            raise RuntimeError(f"本地 FlagEmbedding reranker 不可用: {reason}")
        pairs = [[query, document] for document in documents]
        scores = self._model.compute_score(pairs, normalize=self.config.flag_reranker_normalize)
        if isinstance(scores, float):
            return [float(scores)]
        return [float(value) for value in scores]


class LexicalIndex:
    """BM25 词法索引。"""

    def __init__(self, payload: Dict[str, Any]):
        """初始化 BM25 索引。

        功能目的：
            将磁盘 JSON 索引转成可查询对象。
        输入参数：
            payload：`indexes/bm25/lexical_index.json` 内容。
        返回值：
            `LexicalIndex` 实例。
        关键流程：
            保存文档频次、平均长度和每个 chunk 的 term frequency。
        可能报错或边界情况：
            索引字段缺失会抛出 KeyError，提示需要重新构建索引。
        """

        self.doc_count = int(payload["doc_count"])
        self.avg_doc_len = float(payload["avg_doc_len"])
        self.doc_freqs = {key: int(value) for key, value in payload["doc_freqs"].items()}
        self.doc_stats = payload["doc_stats"]
        self.k1 = 1.5
        self.b = 0.75

    @classmethod
    def from_path(cls, path: Path) -> "LexicalIndex":
        """从文件加载 BM25 索引。

        功能目的：
            给检索引擎提供简洁加载入口。
        输入参数：
            path：BM25 JSON 文件路径。
        返回值：
            `LexicalIndex` 实例。
        关键流程：
            读取 JSON 并传给构造函数。
        可能报错或边界情况：
            文件不存在时说明尚未执行 `scripts/build_indexes.py`。
        """

        return cls(read_json(path))

    def score(self, query_tokens: Sequence[str], candidate_ids: Optional[Iterable[str]] = None) -> Dict[str, float]:
        """计算候选 chunk 的 BM25 分数。

        功能目的：
            提供无需模型的稳定基础检索。
        输入参数：
            query_tokens：查询 token。
            candidate_ids：可选候选 chunk ID 集合。
        返回值：
            `chunk_id -> BM25 分数`。
        关键流程：
            对每个候选文档累计标准 BM25 项分数。
        可能报错或边界情况：
            查询 token 没有命中任何文档时返回空字典。
        """

        scores: Dict[str, float] = {}
        candidate_set = set(candidate_ids) if candidate_ids is not None else None
        token_counts = Counter(query_tokens)
        for chunk_id, stats in self.doc_stats.items():
            if candidate_set is not None and chunk_id not in candidate_set:
                continue
            doc_len = stats["length"]
            term_freqs = stats["term_freqs"]
            score = 0.0
            for token, qf in token_counts.items():
                tf = term_freqs.get(token, 0)
                if tf <= 0:
                    continue
                df = self.doc_freqs.get(token, 0)
                idf = math.log(1 + (self.doc_count - df + 0.5) / (df + 0.5))
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * doc_len / max(self.avg_doc_len, 1.0))
                score += qf * idf * numerator / max(denominator, 1e-9)
            if score > 0:
                scores[chunk_id] = score
        return scores


class DenseIndex:
    """dense embedding 索引，优先使用 float32 二进制矩阵。"""

    def __init__(self, layout: ProjectLayout):
        """加载 dense 索引元数据。

        功能目的：
            优先用 mmap 加载 `vectors.f32`，避免把向量展开成 Python list；兼容旧 JSONL 分片。
        输入参数：
            layout：项目目录布局。
        返回值：
            `DenseIndex` 实例。
        关键流程：
            优先读取二进制矩阵；若不存在则读取 `shards/*.jsonl`；兼容旧式 `chunk_embeddings.json`。
        可能报错或边界情况：
            没有 dense 索引时 `available=False`，检索层自动退回 BM25。
        """

        self.layout = layout
        self.metadata: Dict[str, Any] = {}
        self.vectors: Dict[str, List[float]] = {}
        self.binary_vectors: Any = None
        self.chunk_to_row: Dict[str, int] = {}
        self.available = False
        metadata_path = layout.dense_dir / "metadata.json"
        old_path = layout.dense_dir / "chunk_embeddings.json"
        if metadata_path.exists():
            self.metadata = read_json(metadata_path)
            self.available = bool(self.metadata.get("available"))
            if self.available:
                if isinstance(self.metadata.get("binary"), dict):
                    self._load_binary()
                elif self.metadata.get("shards"):
                    self._load_shards()
        elif old_path.exists():
            payload = read_json(old_path)
            self.metadata = {key: value for key, value in payload.items() if key != "vectors"}
            self.vectors = payload.get("vectors", {})
            self.available = bool(self.vectors)
        else:
            status_path = layout.dense_dir / "status.json"
            self.metadata = read_json(status_path) if status_path.exists() else {"available": False, "reason": "dense 索引不存在。"}

    def has_vectors(self) -> bool:
        """Return whether any dense vector backend is loaded."""

        return self.binary_vectors is not None or bool(self.vectors)

    def _load_binary(self) -> None:
        """加载 float32 二进制 dense 矩阵。

        功能目的：
            用 numpy memmap 延迟映射 `vectors.f32`，显著降低 MCP 进程常驻内存。
        输入参数：
            无，使用 metadata 中的 binary 描述。
        返回值：
            无。
        关键流程：
            读取 `chunk_records.json` 建立 `chunk_id -> row` 映射；向量矩阵以只读 memmap 打开。
        可能报错或边界情况：
            numpy 不可用或二进制产物缺失会抛出错误，提示迁移包不完整。
        """

        import numpy as np

        binary = self.metadata["binary"]
        records_path = self.layout.dense_dir / str(binary["records_path"])
        vectors_path = self.layout.dense_dir / str(binary["vectors_path"])
        records_payload = read_json(records_path)
        records = records_payload.get("records") if isinstance(records_payload, dict) else records_payload
        if not isinstance(records, list):
            raise RuntimeError(f"dense chunk records 格式不兼容：{records_path}")
        shape = binary.get("shape") or [len(records), self.metadata.get("dimension")]
        row_count = int(shape[0])
        dimension = int(shape[1])
        expected_bytes = row_count * dimension * 4
        actual_bytes = vectors_path.stat().st_size
        if actual_bytes != expected_bytes:
            raise RuntimeError(f"dense binary 大小不匹配：expected={expected_bytes} actual={actual_bytes}")
        self.binary_vectors = np.memmap(vectors_path, dtype="<f4", mode="r", shape=(row_count, dimension))
        self.chunk_to_row = {
            str(record["chunk_id"]): int(record.get("row", index))
            for index, record in enumerate(records)
            if record.get("chunk_id") is not None
        }
        self.available = bool(self.chunk_to_row)

    def _load_shards(self) -> None:
        """加载旧 dense JSONL 分片。

        功能目的：
            兼容旧迁移包；新索引默认不再使用 JSONL 分片。
        输入参数：
            无，使用实例 metadata。
        返回值：
            无。
        关键流程：
            按 metadata 中记录的相对路径顺序读取每个 shard。
        可能报错或边界情况：
            任一分片缺失会抛出文件错误，提示迁移包不完整。
        """

        for shard in self.metadata.get("shards", []):
            shard_path = self.layout.dense_dir / shard["path"]
            with shard_path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    line = line.strip()
                    if not line:
                        continue
                    record = json.loads(line)
                    self.vectors[record["chunk_id"]] = record["vector"]
        self.available = bool(self.vectors)

    def score(self, query_vector: Sequence[float], candidate_ids: Sequence[str]) -> Dict[str, float]:
        """计算 query 向量与候选 chunk 的 cosine 相似度。"""

        if self.binary_vectors is not None:
            return self._score_binary(query_vector, candidate_ids)
        scores: Dict[str, float] = {}
        for chunk_id in candidate_ids:
            vector = self.vectors.get(chunk_id)
            if vector:
                scores[chunk_id] = _cosine_similarity(query_vector, vector)
        return scores

    def _score_binary(self, query_vector: Sequence[float], candidate_ids: Sequence[str]) -> Dict[str, float]:
        """用 mmap 矩阵批量计算 cosine 相似度。"""

        import numpy as np

        pairs = [(chunk_id, self.chunk_to_row[chunk_id]) for chunk_id in candidate_ids if chunk_id in self.chunk_to_row]
        if not pairs:
            return {}
        query = np.asarray(query_vector, dtype="<f4")
        query_norm = float(np.linalg.norm(query))
        if query_norm <= 1e-12:
            return {}
        rows = np.asarray([row for _, row in pairs], dtype=np.int64)
        matrix = self.binary_vectors[rows]
        dots = matrix @ query
        row_norms = np.linalg.norm(matrix, axis=1)
        denominator = row_norms * query_norm
        values = np.divide(
            dots,
            denominator,
            out=np.zeros_like(dots, dtype=np.float32),
            where=denominator > 1e-12,
        )
        return {chunk_id: float(score) for (chunk_id, _), score in zip(pairs, values)}


class RetrievalEngine:
    """Sobko 统一检索引擎。"""

    def __init__(self, layout: ProjectLayout, config: RagConfig):
        """初始化检索引擎。

        功能目的：
            加载 source、chunk、image、BM25、dense 和后端客户端，供 MCP 工具复用。
        输入参数：
            layout：项目目录布局。
            config：运行配置。
        返回值：
            `RetrievalEngine` 实例。
        关键流程：
            构建 source/chunk/image 查找表，并按 source 聚合 chunk。
        可能报错或边界情况：
            normalized 或索引产物缺失时会抛出文件错误，提示先运行构建脚本。
        """

        self.layout = layout
        self.config = config
        self.sources = read_jsonl(layout.normalized_dir / "source_registry.jsonl")
        self.chunks = read_jsonl(layout.normalized_dir / "chunks.jsonl")
        self.images = read_jsonl(layout.normalized_dir / "images.jsonl")
        self.source_by_id = {item["source_id"]: item for item in self.sources}
        self.chunk_by_id = {item["chunk_id"]: item for item in self.chunks}
        self.image_by_id = {item["image_id"]: item for item in self.images}
        self.chunks_by_source: Dict[str, List[Dict[str, Any]]] = {}
        for chunk in self.chunks:
            self.chunks_by_source.setdefault(chunk["source_id"], []).append(chunk)
        self.lexical_index = LexicalIndex.from_path(layout.bm25_dir / "lexical_index.json")
        self.dense_index = DenseIndex(layout)
        self.image_index = read_json(layout.image_refs_dir / "image_lookup.json") if (layout.image_refs_dir / "image_lookup.json").exists() else {}
        self.ollama_client = OllamaClient(config)
        self.flag_reranker = FlagEmbeddingReranker(config)

    def _runtime_path(self, raw_path: Optional[str]) -> Optional[str]:
        """把记录中的路径解析为当前机器绝对路径。

        功能目的：
            让 JSON 产物可以保存项目相对路径，同时 MCP 返回值仍给出可直接访问的本地路径。
        输入参数：
            raw_path：source/chunk/image 记录中的路径字符串。
        返回值：
            当前项目根下解析得到的绝对路径；空值返回 None。
        关键流程：
            调用配置层 `resolve_portable_path`，统一处理相对路径和历史绝对路径。
        可能报错或边界情况：
            文件不存在不会在这里报错，调用方可用 `Path.exists()` 展示实际存在性。
        """

        if not raw_path:
            return None
        return str(resolve_portable_path(self.layout, raw_path))

    def _apply_filters(
        self,
        *,
        source_types: Optional[Sequence[str]],
        software: Optional[Sequence[str]],
        topics: Optional[Sequence[str]],
        authority_at_least: Optional[str],
    ) -> List[Dict[str, Any]]:
        """按元数据过滤候选 chunk。

        功能目的：
            支持 MCP 查询按 source 类型、软件、主题和权威等级缩小范围。
        输入参数：
            source_types/software/topics/authority_at_least：用户传入过滤条件。
        返回值：
            满足条件的 chunk 列表。
        关键流程：
            对每个 chunk 的标签集合做交集判断。
        可能报错或边界情况：
            空过滤条件表示不过滤。
        """

        results: List[Dict[str, Any]] = []
        source_type_set = set(source_types or [])
        software_set = set(software or [])
        topic_set = set(topics or [])
        for chunk in self.chunks:
            if source_type_set and chunk["source_type"] not in source_type_set:
                continue
            if software_set and not software_set.intersection(chunk.get("software_tags", [])):
                continue
            if topic_set and not topic_set.intersection(chunk.get("topic_tags", [])):
                continue
            if not authority_meets(chunk["authority_level"], authority_at_least):
                continue
            results.append(chunk)
        return results

    def _dense_scores(self, query: str, candidate_ids: Sequence[str]) -> tuple[Dict[str, float], bool, str | None]:
        """计算 dense 检索分数。

        功能目的：
            在 embedding 索引和 API 可用时补充语义检索能力。
        输入参数：
            query：用户查询。
            candidate_ids：候选 chunk ID 列表。
        返回值：
            `(分数字典, embedding 是否可用, 错误原因)`。
        关键流程：
            先实时生成 query embedding，再与候选 chunk 向量计算余弦相似度。
        可能报错或边界情况：
            配置关闭、索引缺失或 API 失败时返回错误原因，不抛出到上层。
        """

        if not self.config.rag_use_embedding:
            return {}, False, "配置关闭 embedding 检索。"
        if not self.dense_index.available or not self.dense_index.has_vectors():
            return {}, False, self.dense_index.metadata.get("reason", "dense 索引不可用。")
        configured_provider = self.ollama_client._embedding_provider()
        indexed_provider = str(self.dense_index.metadata.get("provider") or "").strip().lower()
        if indexed_provider and indexed_provider != configured_provider:
            return (
                {},
                False,
                f"dense 索引 provider={indexed_provider} 与当前 embedding_provider={configured_provider} 不一致；"
                "请设置匹配 provider 或运行 python scripts/build_indexes.py 重建 dense 索引。",
            )
        configured_model = self.ollama_client._embedding_model()
        indexed_model = str(self.dense_index.metadata.get("model_name") or "").strip()
        if indexed_model and indexed_model != configured_model:
            return (
                {},
                False,
                f"dense 索引 model_name={indexed_model} 与当前 embedding_model={configured_model} 不一致；"
                "请设置匹配模型或运行 python scripts/build_indexes.py 重建 dense 索引。",
            )
        try:
            model_name = self.dense_index.metadata.get("model_name") or configured_model
            query_vector = self.ollama_client.embed_texts([query], model=model_name)[0]
        except Exception as exc:
            return {}, False, str(exc)
        expected_dimension = int(self.dense_index.metadata.get("dimension") or 0)
        if expected_dimension and len(query_vector) != expected_dimension:
            return (
                {},
                False,
                f"query embedding 维度 {len(query_vector)} 与 dense 索引维度 {expected_dimension} 不一致；"
                "请用当前 embedding 配置重建 dense 索引。",
            )
        return self.dense_index.score(query_vector, candidate_ids), True, None

    def _rerank_scores(self, query: str, ordered_candidates: Sequence[Dict[str, Any]]) -> tuple[Dict[str, float], bool, str | None]:
        """计算 rerank 分数。

        功能目的：
            对融合检索的 top candidates 重新排序，提高结果相关性。
        输入参数：
            query：用户查询。
            ordered_candidates：初筛候选 chunk。
        返回值：
            `(分数字典, rerank 是否可用, 错误原因)`。
        关键流程：
            本地 FlagEmbedding 优先；失败后尝试 Ollama rerank；都失败时降级。
        可能报错或边界情况：
            候选为空或配置关闭时不执行 rerank。
        """

        if not ordered_candidates:
            return {}, False, "无候选 chunk 可 rerank。"
        if not self.config.rag_use_reranker:
            return {}, False, "配置关闭 rerank。"
        documents = [candidate["text"] for candidate in ordered_candidates]
        try:
            scores = self.flag_reranker.score(query, documents)
            return {candidate["chunk_id"]: score for candidate, score in zip(ordered_candidates, scores)}, True, None
        except Exception as local_exc:
            try:
                scores = self.ollama_client.rerank(query, documents)
                return {candidate["chunk_id"]: score for candidate, score in zip(ordered_candidates, scores)}, True, None
            except Exception as remote_exc:
                return {}, False, f"local={local_exc}; ollama={remote_exc}"

    def search(
        self,
        *,
        query: str,
        top_k: Optional[int] = None,
        source_types: Optional[Sequence[str]] = None,
        software: Optional[Sequence[str]] = None,
        topics: Optional[Sequence[str]] = None,
        authority_at_least: Optional[str] = None,
        include_images: bool = True,
    ) -> SearchResult:
        """执行 Sobko 检索。

        功能目的：
            为 MCP `sobko_search` 提供权威感知的 BM25/hybrid/rerank 检索。
        输入参数：
            query：用户查询。
            top_k：返回数量。
            source_types/software/topics/authority_at_least：过滤条件。
            include_images：是否返回相关 image_id。
        返回值：
            `SearchResult`。
        关键流程：
            metadata filter -> BM25 -> dense -> 融合 -> rerank -> authority bonus -> top_k。
        可能报错或边界情况：
            dense/rerank 后端失败时自动降级，并在 `backend_warnings` 中记录原因。
        """

        limited_top_k = int(top_k or self.config.rag_top_k)
        requested_mode = "hybrid" if self.config.rag_use_embedding else "lexical_only"
        backend_warnings: List[str] = []
        filtered_chunks = self._apply_filters(
            source_types=source_types,
            software=software,
            topics=topics,
            authority_at_least=authority_at_least,
        )
        candidate_ids = [chunk["chunk_id"] for chunk in filtered_chunks]
        lexical_scores = _normalize_scores(self.lexical_index.score(tokenize(query), candidate_ids=candidate_ids))

        dense_scores, embedding_available, embedding_error = self._dense_scores(query, candidate_ids)
        effective_mode = "hybrid" if embedding_available and dense_scores else "lexical_only"
        if embedding_error:
            backend_warnings.append(f"dense_fallback: {embedding_error}")
        dense_scores = _normalize_scores(dense_scores) if effective_mode == "hybrid" else {}

        combined_scores: Dict[str, float] = {}
        for chunk in filtered_chunks:
            chunk_id = chunk["chunk_id"]
            lexical = lexical_scores.get(chunk_id, 0.0)
            dense = dense_scores.get(chunk_id, 0.0)
            if effective_mode == "hybrid":
                combined_scores[chunk_id] = self.config.rag_bm25_weight * lexical + self.config.rag_embedding_weight * dense
            else:
                combined_scores[chunk_id] = lexical

        ordered_ids = [chunk_id for chunk_id, _ in sorted(combined_scores.items(), key=lambda item: item[1], reverse=True)]
        ordered_candidates = [self.chunk_by_id[chunk_id] for chunk_id in ordered_ids[: self.config.rag_rerank_candidate_k]]
        rerank_scores, rerank_available, rerank_error = self._rerank_scores(query, ordered_candidates)
        if rerank_error and self.config.rag_use_reranker:
            backend_warnings.append(f"rerank_fallback: {rerank_error}")
        rerank_scores = _normalize_scores(rerank_scores) if rerank_scores else {}

        scored_results: List[tuple[float, Dict[str, Any]]] = []
        for chunk_id, base_score in combined_scores.items():
            chunk = self.chunk_by_id[chunk_id]
            rerank_bonus = rerank_scores.get(chunk_id, 0.0) * 0.2
            authority_bonus = AUTHORITY_ORDER.get(chunk["authority_level"], 0) * 0.01
            final_score = base_score + rerank_bonus + authority_bonus
            scored_results.append((final_score, chunk))
        scored_results.sort(key=lambda item: item[0], reverse=True)

        results: List[Dict[str, Any]] = []
        for rank, (score, chunk) in enumerate(scored_results[:limited_top_k], start=1):
            results.append(
                {
                    "rank": rank,
                    "score": round(float(score), 6),
                    "chunk_id": chunk["chunk_id"],
                    "source_id": chunk["source_id"],
                    "title": chunk["title"],
                    "snippet": chunk["snippet"],
                    "authority_level": chunk["authority_level"],
                    "source_type": chunk["source_type"],
                    "software_tags": chunk["software_tags"],
                    "topic_tags": chunk["topic_tags"],
                    "method_tags": chunk["method_tags"],
                    "path": self._runtime_path(chunk["canonical_path"]),
                    "relative_path": chunk["canonical_path"],
                    "url": chunk["canonical_url"],
                    "page_range": chunk.get("page_range"),
                    "section_path": chunk["section_path"],
                    "image_ids": chunk["image_ids"] if include_images else [],
                }
            )

        return SearchResult(
            query=query,
            requested_mode=requested_mode,
            effective_mode=effective_mode,
            embedding_available=embedding_available and bool(dense_scores),
            rerank_available=bool(rerank_scores) if rerank_scores else rerank_available,
            backend_warnings=backend_warnings,
            results=results,
            index_version=self.config.index_version,
        )

    def fetch(
        self,
        *,
        chunk_id: Optional[str] = None,
        source_id: Optional[str] = None,
        expand_prev_next: int = 1,
        include_html_anchor: bool = True,
    ) -> Dict[str, Any]:
        """展开 source 或 chunk 原文上下文。

        功能目的：
            让用户从检索结果回到更完整的证据窗口。
        输入参数：
            chunk_id：目标 chunk ID。
            source_id：目标 source ID。
            expand_prev_next：围绕 chunk 展开的前后 chunk 数。
            include_html_anchor：是否返回手册页锚点。
        返回值：
            包含 source 信息和 context_chunks 的字典。
        关键流程：
            优先按 chunk 定位 source 和窗口；仅给 source_id 时返回 source 起始窗口。
        可能报错或边界情况：
            `chunk_id` 和 `source_id` 都为空会抛出 `ValueError`。
        """

        if not chunk_id and not source_id:
            raise ValueError("`chunk_id` 和 `source_id` 至少提供一个。")
        if chunk_id:
            chunk = self.chunk_by_id.get(chunk_id)
            if not chunk:
                raise KeyError(f"未找到 chunk_id={chunk_id}")
            source = self.source_by_id[chunk["source_id"]]
            source_chunks = self.chunks_by_source[source["source_id"]]
            chunk_index = next(index for index, item in enumerate(source_chunks) if item["chunk_id"] == chunk_id)
            start = max(0, chunk_index - expand_prev_next)
            end = min(len(source_chunks), chunk_index + expand_prev_next + 1)
            window = source_chunks[start:end]
        else:
            source = self.source_by_id.get(str(source_id))
            if not source:
                raise KeyError(f"未找到 source_id={source_id}")
            source_chunks = self.chunks_by_source[source["source_id"]]
            window = source_chunks[: max(3, expand_prev_next * 2 + 1)]
        return {
            "source_id": source["source_id"],
            "title": source["title"],
            "authority_level": source["authority_level"],
            "source_type": source["source_type"],
            "path": self._runtime_path(source["canonical_path"]),
            "relative_path": source["canonical_path"],
            "url": source["canonical_url"],
            "html_path": self._runtime_path(source.get("html_path")),
            "html_relative_path": source.get("html_path"),
            "context_chunks": [
                {
                    "chunk_id": item["chunk_id"],
                    "section_path": item["section_path"],
                    "page_range": item["page_range"],
                    "text": item["text"],
                    "snippet": item["snippet"],
                    "dom_anchor": item["dom_anchor"] if include_html_anchor else None,
                    "image_ids": item["image_ids"],
                }
                for item in window
            ],
            "index_version": self.config.index_version,
        }

    def get_image(self, *, image_id: str, return_mode: str = "path") -> Dict[str, Any]:
        """返回图片路径与邻近说明。

        功能目的：
            让用户从检索结果中的 image_id 找到本地图片资源。
        输入参数：
            image_id：图片 ID。
            return_mode：返回模式，v1 仅支持 `path`。
        返回值：
            图片路径、caption、nearby_text 等信息。
        关键流程：
            从 image lookup 中读取图片记录并原样返回关键字段。
        可能报错或边界情况：
            未知 image_id 抛出 `KeyError`；非 path 模式抛出 `ValueError`。
        """

        image = self.image_by_id.get(image_id)
        if not image:
            raise KeyError(f"未找到 image_id={image_id}")
        if return_mode != "path":
            raise ValueError("v1 仅支持 return_mode='path'。")
        runtime_path = self._runtime_path(image["path"])
        return {
            "image_id": image_id,
            "source_id": image["source_id"],
            "chunk_id": image.get("chunk_id"),
            "path": runtime_path,
            "relative_path": image["path"],
            "exists": Path(runtime_path).exists() if runtime_path else False,
            "caption": image.get("caption", ""),
            "nearby_text": image.get("nearby_text", ""),
            "section_path": image.get("section_path"),
            "return_mode": return_mode,
        }

    def trace_source(self, *, source_id: Optional[str] = None, chunk_id: Optional[str] = None) -> Dict[str, Any]:
        """追溯 source 或 chunk 的来源链路。

        功能目的：
            返回权威等级、本地路径、URL、source hash 和原始快照信息。
        输入参数：
            source_id：source ID。
            chunk_id：chunk ID。
        返回值：
            source trace 字典。
        关键流程：
            chunk_id 优先定位到所属 source；source_id 直接查 source 表。
        可能报错或边界情况：
            两个 ID 都为空或 ID 不存在时抛出明确异常。
        """

        source: Optional[Dict[str, Any]] = None
        chunk: Optional[Dict[str, Any]] = None
        if chunk_id:
            chunk = self.chunk_by_id.get(chunk_id)
            if not chunk:
                raise KeyError(f"未找到 chunk_id={chunk_id}")
            source = self.source_by_id[chunk["source_id"]]
        elif source_id:
            source = self.source_by_id.get(source_id)
            if not source:
                raise KeyError(f"未找到 source_id={source_id}")
        else:
            raise ValueError("`source_id` 和 `chunk_id` 至少提供一个。")
        payload = {
            "source_id": source["source_id"],
            "chunk_id": chunk["chunk_id"] if chunk else None,
            "title": source["title"],
            "authority_level": source["authority_level"],
            "source_type": source["source_type"],
            "canonical_path": self._runtime_path(source["canonical_path"]),
            "canonical_relative_path": source["canonical_path"],
            "canonical_url": source["canonical_url"],
            "raw_markdown_path": self._runtime_path(source.get("raw_markdown_path")),
            "raw_markdown_relative_path": source.get("raw_markdown_path"),
            "html_path": self._runtime_path(source.get("html_path")),
            "html_relative_path": source.get("html_path"),
            "manual_root_path": self._runtime_path(source.get("manual_root_path")),
            "manual_root_relative_path": source.get("manual_root_path"),
            "post_id": source.get("post_id"),
            "date": source.get("date"),
            "version_hint": source.get("version_hint"),
            "source_hash": source.get("source_hash"),
            "index_version": self.config.index_version,
        }
        return payload
