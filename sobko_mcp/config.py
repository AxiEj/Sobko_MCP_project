"""Sobko 项目配置与目录布局。"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class RagConfig:
    """Sobko MCP 运行配置。

    功能目的：
        集中管理知识源快照路径、RAG 参数、embedding/rerank API 端口与 MCP server 名称。
    输入参数：
        通过 :meth:`from_dict` 从 JSON 字典构造。
    返回值：
        `RagConfig` 数据对象。
    关键流程：
        配置只保存可迁移的字符串路径和模型参数，实际路径解析由 `resolve_input_path` 完成。
    可能报错或边界情况：
        配置缺少必要字段时会在 dataclass 构造阶段抛出 `TypeError`，避免静默使用错误默认值。
    """

    project_name: str
    index_version: str
    posts_manifest_path: str
    posts_root_path: str
    manual_root_path: str
    manual_markdown_path: str
    manual_html_path: str
    manual_manifest_path: str
    software_docs_manifest_path: str
    blog_authority_level: str
    manual_authority_level: str
    rag_enabled: bool
    rag_top_k: int
    rag_max_context_chars: int
    rag_use_embedding: bool
    rag_use_reranker: bool
    rag_embedding_weight: float
    rag_bm25_weight: float
    rag_rerank_candidate_k: int
    dense_batch_size: int
    dense_shard_max_bytes: int
    request_timeout: int
    embedding_provider: str
    embedding_api_base_url: str
    embedding_fallback_base_urls: List[str]
    embedding_api_endpoint: str
    embedding_model: str
    embedding_dimensions: Optional[int]
    local_embedding_max_length: Optional[int]
    embedding_daemon_enabled: bool
    embedding_daemon_required: bool
    embedding_daemon_autostart: bool
    embedding_daemon_base_url: str
    embedding_daemon_bind_host: str
    embedding_daemon_bind_port: int
    rerank_provider: str
    rerank_api_base_url: str
    rerank_fallback_base_urls: List[str]
    rerank_api_endpoint: str
    rerank_model: str
    flag_reranker_model_name: str
    flag_reranker_use_fp16: bool
    flag_reranker_normalize: bool
    mcp_server_name: str
    mcp_transport: str
    mcp_bind_host: str
    mcp_bind_port: int

    @classmethod
    def from_dict(cls, payload: Dict[str, Any]) -> "RagConfig":
        """从 JSON 字典构造配置对象。

        功能目的：
            给配置加载入口保留一个稳定的构造点，后续如果需要校验字段可以集中添加。
        输入参数：
            payload：`configs/default.json` 解析得到的字典。
        返回值：
            `RagConfig` 实例。
        关键流程：
            直接展开字典到 dataclass，保持配置字段和代码字段一一对应。
        可能报错或边界情况：
            多余或缺失字段都会抛出 `TypeError`，提示配置与代码版本不匹配。
        """

        payload.setdefault("embedding_dimensions", None)
        payload.setdefault("software_docs_manifest_path", "data_sources/sobko_sources/software_docs_manifest.jsonl")
        payload.setdefault("local_embedding_max_length", None)
        payload.setdefault("embedding_daemon_enabled", True)
        payload.setdefault("embedding_daemon_required", False)
        payload.setdefault("embedding_daemon_autostart", True)
        payload.setdefault("embedding_daemon_base_url", "http://127.0.0.1:8769")
        payload.setdefault("embedding_daemon_bind_host", "127.0.0.1")
        payload.setdefault("embedding_daemon_bind_port", 8769)
        return cls(**payload)


@dataclass
class ProjectLayout:
    """项目目录布局。

    功能目的：
        避免在脚本和包代码中散落硬编码路径。
    输入参数：
        由 `build_layout` 传入项目根目录。
    返回值：
        保存各功能目录的 dataclass。
    关键流程：
        所有构建产物均写入项目内部目录，便于整体迁移。
    可能报错或边界情况：
        目录不存在不代表错误，创建由 `ensure_project_dirs` 负责。
    """

    root: Path
    configs_dir: Path
    data_sources_dir: Path
    normalized_dir: Path
    indexes_dir: Path
    bm25_dir: Path
    dense_dir: Path
    dense_shards_dir: Path
    image_refs_dir: Path
    rerank_cache_dir: Path
    metadata_dir: Path
    reports_dir: Path
    scripts_dir: Path
    tests_dir: Path
    docs_dir: Path
    server_dir: Path
    skills_dir: Path


def discover_project_root(start: Path | None = None) -> Path:
    """向上查找 Sobko 项目根目录。

    功能目的：
        让脚本、测试和 MCP server 在任意工作目录下都能定位项目根。
    输入参数：
        start：起始文件或目录；默认使用当前模块文件。
    返回值：
        包含 `configs/default.json` 和 `sobko_mcp` 包目录的项目根路径。
    关键流程：
        从起点逐级向父目录查找项目特征文件。
    可能报错或边界情况：
        如果目录结构被破坏，会抛出 `FileNotFoundError`，提示用户先检查迁移完整性。
    """

    current = (start or Path(__file__)).resolve()
    if current.is_file():
        current = current.parent
    for candidate in [current, *current.parents]:
        if (candidate / "configs" / "default.json").exists() and (candidate / "sobko_mcp").exists():
            return candidate
    raise FileNotFoundError("未找到 Sobko_MCP_project 项目根目录。")


def build_layout(root: Path | None = None) -> ProjectLayout:
    """构造目录布局对象。

    功能目的：
        提供统一的项目路径入口。
    输入参数：
        root：显式项目根；为空时自动发现。
    返回值：
        `ProjectLayout` 实例。
    关键流程：
        根据项目根拼接各个标准子目录。
    可能报错或边界情况：
        自动发现失败时会抛出 `FileNotFoundError`。
    """

    project_root = discover_project_root(root or Path(__file__))
    return ProjectLayout(
        root=project_root,
        configs_dir=project_root / "configs",
        data_sources_dir=project_root / "data_sources",
        normalized_dir=project_root / "normalized",
        indexes_dir=project_root / "indexes",
        bm25_dir=project_root / "indexes" / "bm25",
        dense_dir=project_root / "indexes" / "dense",
        dense_shards_dir=project_root / "indexes" / "dense" / "shards",
        image_refs_dir=project_root / "indexes" / "image_refs",
        rerank_cache_dir=project_root / "indexes" / "rerank_cache",
        metadata_dir=project_root / "metadata",
        reports_dir=project_root / "metadata" / "reports",
        scripts_dir=project_root / "scripts",
        tests_dir=project_root / "tests",
        docs_dir=project_root / "docs",
        server_dir=project_root / "server",
        skills_dir=project_root / "skills",
    )


def ensure_project_dirs(layout: ProjectLayout) -> None:
    """创建运行和构建所需目录。

    功能目的：
        让构建脚本可以在干净迁移后的目录中直接运行。
    输入参数：
        layout：项目目录布局。
    返回值：
        无。
    关键流程：
        对所有产物目录调用 `mkdir(parents=True, exist_ok=True)`。
    可能报错或边界情况：
        如果目录没有写权限，会保留底层 `OSError`，便于用户定位权限问题。
    """

    for path in [
        layout.data_sources_dir,
        layout.normalized_dir,
        layout.indexes_dir,
        layout.bm25_dir,
        layout.dense_dir,
        layout.dense_shards_dir,
        layout.image_refs_dir,
        layout.rerank_cache_dir,
        layout.metadata_dir,
        layout.reports_dir,
        layout.scripts_dir,
        layout.tests_dir,
        layout.docs_dir,
        layout.server_dir,
        layout.skills_dir,
    ]:
        path.mkdir(parents=True, exist_ok=True)


def load_config(config_path: Path | None = None) -> RagConfig:
    """加载 JSON 配置文件。

    功能目的：
        为脚本、测试和 MCP server 提供统一配置加载方式。
    输入参数：
        config_path：可选配置文件路径；为空时使用 `configs/default.json`。
    返回值：
        `RagConfig` 实例。
    关键流程：
        先定位项目根，再读取 UTF-8 JSON。
    可能报错或边界情况：
        JSON 格式错误、字段缺失或路径不存在都会直接抛出明确异常。
    """

    root = discover_project_root(config_path or Path(__file__))
    resolved_path = config_path or (root / "configs" / "default.json")
    with resolved_path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    return RagConfig.from_dict(payload)


def resolve_input_path(layout: ProjectLayout, raw_path: str) -> Path:
    """解析配置中的相对或绝对输入路径。

    功能目的：
        让配置既能使用项目内相对路径，也能使用用户机器上的绝对路径。
    输入参数：
        layout：项目目录布局。
        raw_path：配置文件中的路径字符串。
    返回值：
        解析后的绝对 `Path`。
    关键流程：
        绝对路径原样解析；相对路径以项目根为基准。
    可能报错或边界情况：
        本函数只负责解析，不检查文件是否存在；存在性由调用方按上下文校验。
    """

    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (layout.root / candidate).resolve()


def to_portable_path(layout: ProjectLayout, path: Path) -> str:
    """把项目内路径转为可迁移字符串。

    功能目的：
        避免 normalized/index 产物写入当前机器的绝对路径，提升 GitHub 发布后的可迁移性。
    输入参数：
        layout：项目目录布局。
        path：待保存的文件或目录路径。
    返回值：
        如果路径位于项目根目录内，返回 POSIX 风格相对路径；否则返回绝对路径。
    关键流程：
        先解析真实路径，再尝试相对化到 `layout.root`。
    可能报错或边界情况：
        外部路径无法相对化时会保留绝对路径，因为这种情况通常代表用户显式配置了项目外数据。
    """

    resolved = path.resolve()
    try:
        return resolved.relative_to(layout.root).as_posix()
    except ValueError:
        return str(resolved)


def resolve_portable_path(layout: ProjectLayout, raw_path: str) -> Path:
    """解析可迁移路径。

    功能目的：
        将 registry/chunk/image 中保存的相对路径恢复为当前机器上的绝对路径。
    输入参数：
        layout：项目目录布局。
        raw_path：JSON 记录中的路径字符串。
    返回值：
        当前机器可访问的绝对 `Path`。
    关键流程：
        绝对路径原样解析；相对路径以当前项目根为基准解析。
    可能报错或边界情况：
        空字符串会解析为项目根，调用方应在可选字段为空时先行判断。
    """

    candidate = Path(raw_path)
    if candidate.is_absolute():
        return candidate
    return (layout.root / candidate).resolve()
