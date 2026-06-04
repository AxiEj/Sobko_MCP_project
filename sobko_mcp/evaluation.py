"""Sobko 检索评测逻辑。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .common import read_json, write_json
from .config import ProjectLayout
from .retriever import RetrievalEngine


@dataclass
class EvalCase:
    """单条检索评测样本。

    功能目的：
        用固定 query 验证 Sobko 的已知命中、标签过滤和权威优先行为。
    输入参数：
        由 `load_eval_cases` 从 JSON 读入。
    返回值：
        dataclass 实例。
    关键流程：
        保存 expected_source_ids、required_tags、required_source_types 和 expected_authority。
    可能报错或边界情况：
        字段为空表示不启用对应检查。
    """

    query: str
    expected_source_ids: List[str]
    required_tags: List[str]
    required_source_types: List[str]
    expected_authority: str | None
    note: str


def load_eval_cases(layout: ProjectLayout) -> List[EvalCase]:
    """加载评测集。

    功能目的：
        从 `metadata/eval_cases.json` 读取固定回归样本。
    输入参数：
        layout：项目目录布局。
    返回值：
        `EvalCase` 列表。
    关键流程：
        将 JSON 字典字段映射到 dataclass。
    可能报错或边界情况：
        文件缺失表示项目尚未包含评测集，应先检查迁移包。
    """

    payload = read_json(layout.metadata_dir / "eval_cases.json")
    return [
        EvalCase(
            query=item["query"],
            expected_source_ids=item.get("expected_source_ids", []),
            required_tags=item.get("required_tags", []),
            required_source_types=item.get("required_source_types", []),
            expected_authority=item.get("expected_authority"),
            note=item.get("note", ""),
        )
        for item in payload
    ]


def _matches_case(result: Dict[str, Any], case: EvalCase) -> bool:
    """判断单条结果是否满足评测期望。

    功能目的：
        支持 source_id 精确命中和标签/source_type 宽松命中两类检查。
    输入参数：
        result：单条检索结果。
        case：评测样本。
    返回值：
        满足期望返回 True。
    关键流程：
        expected_source_ids 优先；否则检查标签、source_type 和 authority。
    可能报错或边界情况：
        如果样本没有任何期望字段，则不会误判为命中。
    """

    if case.expected_source_ids and result["source_id"] in case.expected_source_ids:
        return True
    result_tags = set(result.get("software_tags", []) + result.get("topic_tags", []) + result.get("method_tags", []))
    if case.required_tags and not set(case.required_tags).intersection(result_tags):
        return False
    if case.required_source_types and result["source_type"] not in case.required_source_types:
        return False
    if case.expected_authority and result["authority_level"] != case.expected_authority:
        return False
    return bool(case.required_tags or case.required_source_types or case.expected_authority)


def _portable_top_result(result: Dict[str, Any] | None) -> Dict[str, Any] | None:
    """清理评测报告中的运行时绝对路径。

    功能目的：
        评测 JSON 是要随项目迁移和发布的构建产物，不应保存当前机器的绝对路径。
    输入参数：
        result：单条检索 top result，可能为空。
    返回值：
        复制后的结果字典；如果存在 `relative_path`，则用它覆盖 `path`。
    关键流程：
        不修改原始检索结果，只在写报告前做轻量脱敏和可迁移化。
    可能报错或边界情况：
        无结果时返回 None，保持评测 miss 的表达方式不变。
    """

    if result is None:
        return None
    portable = dict(result)
    if portable.get("relative_path"):
        portable["path"] = portable["relative_path"]
    return portable


def evaluate(layout: ProjectLayout, engine: RetrievalEngine) -> Dict[str, Any]:
    """运行固定检索评测。

    功能目的：
        快速验证 Sobko 构建产物是否能命中关键帖子和手册内容。
    输入参数：
        layout：项目目录布局。
        engine：检索引擎。
    返回值：
        结构化评测结果。
    关键流程：
        逐条查询 top5，统计 top1/top3/top5、权威优先和 lexical-only 比例。
    可能报错或边界情况：
        单条 query 无结果记为 miss，不中断整体评测。
    """

    cases = load_eval_cases(layout)
    case_results: List[Dict[str, Any]] = []
    top1_hits = 0
    top3_hits = 0
    top5_hits = 0
    authority_correct = 0
    lexical_only_count = 0

    for case in cases:
        search_result = engine.search(query=case.query, top_k=5)
        matched_ranks = [item["rank"] for item in search_result.results if _matches_case(item, case)]
        top1_hit = 1 in matched_ranks
        top3_hit = any(rank <= 3 for rank in matched_ranks)
        top5_hit = any(rank <= 5 for rank in matched_ranks)
        if top1_hit:
            top1_hits += 1
        if top3_hit:
            top3_hits += 1
        if top5_hit:
            top5_hits += 1
        if case.expected_authority and search_result.results and search_result.results[0]["authority_level"] == case.expected_authority:
            authority_correct += 1
        if search_result.effective_mode == "lexical_only":
            lexical_only_count += 1
        case_results.append(
            {
                "query": case.query,
                "note": case.note,
                "top1_hit": top1_hit,
                "top3_hit": top3_hit,
                "top5_hit": top5_hit,
                "matched_ranks": matched_ranks,
                "expected_authority": case.expected_authority,
                "effective_mode": search_result.effective_mode,
                "backend_warnings": search_result.backend_warnings,
                "top_result": _portable_top_result(search_result.results[0] if search_result.results else None),
            }
        )

    total = len(cases)
    authority_case_count = sum(1 for case in cases if case.expected_authority)
    summary = {
        "case_count": total,
        "top1_hit_rate": round(top1_hits / total, 4) if total else 0.0,
        "top3_hit_rate": round(top3_hits / total, 4) if total else 0.0,
        "top5_hit_rate": round(top5_hits / total, 4) if total else 0.0,
        "authority_preference_rate": round(authority_correct / max(1, authority_case_count), 4),
        "lexical_only_rate": round(lexical_only_count / total, 4) if total else 0.0,
    }
    payload = {"summary": summary, "cases": case_results}
    write_json(layout.reports_dir / "retrieval_evaluation.json", payload)
    return payload


def render_markdown_report(payload: Dict[str, Any]) -> str:
    """将评测结果渲染为 Markdown。

    功能目的：
        生成便于迁移包审阅的评测报告。
    输入参数：
        payload：`evaluate` 返回的结构化结果。
    返回值：
        Markdown 字符串。
    关键流程：
        先写摘要指标，再逐条列出 query、命中情况、后端模式和 top result。
    可能报错或边界情况：
        top_result 为空时写 `NONE`。
    """

    summary = payload["summary"]
    lines = [
        "# Sobko 检索评测报告",
        "",
        f'- 样本数：{summary["case_count"]}',
        f'- top-1 命中率：{summary["top1_hit_rate"]:.2%}',
        f'- top-3 命中率：{summary["top3_hit_rate"]:.2%}',
        f'- top-5 命中率：{summary["top5_hit_rate"]:.2%}',
        f'- authority 优先正确率：{summary["authority_preference_rate"]:.2%}',
        f'- lexical only 比例：{summary["lexical_only_rate"]:.2%}',
        "",
        "## 逐条样本",
        "",
    ]
    for index, case in enumerate(payload["cases"], start=1):
        top_result = case["top_result"]["source_id"] if case["top_result"] else "NONE"
        lines.extend(
            [
                f"### {index}. {case['query']}",
                f'- 说明：{case["note"] or "无"}',
                f'- top1/top3/top5：{case["top1_hit"]}/{case["top3_hit"]}/{case["top5_hit"]}',
                f'- matched_ranks：{case["matched_ranks"]}',
                f'- effective_mode：{case["effective_mode"]}',
                f'- backend_warnings：{case["backend_warnings"]}',
                f"- top_result：{top_result}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
