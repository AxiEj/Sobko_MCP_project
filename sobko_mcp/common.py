"""Sobko MCP 的通用工具函数与标签词表。"""

from __future__ import annotations

import json
import re
from hashlib import sha256
from pathlib import Path
from typing import Any, Dict, Iterable, List, Sequence, Tuple

SOFTWARE_TAGS: List[str] = [
    "Multiwfn",
    "Gaussian",
    "GROMACS",
    "CP2K",
    "ORCA",
    "VMD",
    "Dalton",
    "NBO",
    "AMBER",
    "xTB",
    "CREST",
    "Psi4",
    "Molpro",
    "NWChem",
    "VASP",
    "MOPAC",
]

TOPIC_TAGS: List[str] = [
    "波函数分析",
    "量子化学",
    "分子动力学",
    "第一性原理",
    "AIMD",
    "周期性DFT",
    "赝势",
    "可视化",
    "激发态与光谱",
    "芳香性",
    "弱相互作用",
    "静电势与电荷",
    "结构与文件格式",
    "综述/教程/投稿经验",
    "增强采样",
    "自由能计算",
    "输运性质",
    "电解质",
    "机器学习势",
    "Monte Carlo",
    "轨迹后处理",
    "QM/MM",
    "催化",
    "可重复性",
]

SOFTWARE_SYNONYMS: Dict[str, Sequence[str]] = {
    "Multiwfn": ["multiwfn"],
    "Gaussian": ["gaussian", "g16", "g09", "g03"],
    "GROMACS": ["gromacs"],
    "CP2K": ["cp2k"],
    "ORCA": ["orca"],
    "VMD": ["vmd"],
    "Dalton": ["dalton"],
    "NBO": ["nbo"],
    "AMBER": ["amber"],
    "xTB": ["xtb"],
    "CREST": ["crest"],
    "Psi4": ["psi4"],
    "Molpro": ["molpro"],
    "NWChem": ["nwchem"],
    "VASP": ["vasp"],
    "MOPAC": ["mopac"],
}

TOPIC_SYNONYMS: Dict[str, Sequence[str]] = {
    "波函数分析": ["波函数分析", "wavefunction analysis", "wfn analysis"],
    "量子化学": ["量子化学", "quantum chemistry", "理论计算化学"],
    "分子动力学": ["分子动力学", "molecular dynamics", "md模拟", "系综", "npt", "nvt"],
    "第一性原理": ["第一性原理", "first-principles", "ab initio"],
    "AIMD": ["aimd", "ab initio molecular dynamics", "第一性原理分子动力学"],
    "周期性DFT": ["周期性第一性原理", "周期性 dft", "solid-state dft", "periodic dft", "固体 dft"],
    "赝势": ["赝势", "pseudopotential", "pseudo"],
    "可视化": ["可视化", "visualization", "isosurface", "等值面"],
    "激发态与光谱": ["激发态", "光谱", "excited state", "spectrum", "tddft", "nto"],
    "芳香性": ["芳香性", "aromaticity", "nics"],
    "弱相互作用": ["弱相互作用", "noncovalent", "nci", "igm", "igmh", "iri"],
    "静电势与电荷": ["静电势", "电荷", "esp", "hirshfeld", "resp"],
    "结构与文件格式": ["文件格式", "结构文件", "molden", "fchk", "cub", "cube", "xyz"],
    "综述/教程/投稿经验": ["教程", "综述", "投稿经验", "faq", "tips", "best practice", "best practices"],
    "增强采样": ["增强采样", "enhanced sampling", "metadynamics", "umbrella sampling", "replica exchange"],
    "自由能计算": ["自由能", "free energy", "alchemical", "mbar", "bar"],
    "输运性质": ["输运", "自扩散", "黏度", "电导率", "transport", "diffusion", "viscosity", "conductivity"],
    "电解质": ["电解质", "离子液体", "ionic liquid", "electrolyte"],
    "机器学习势": ["机器学习势", "神经网络势", "mlip", "machine learning potential"],
    "Monte Carlo": ["monte carlo", "蒙特卡罗"],
    "轨迹后处理": ["轨迹后处理", "markov state model", "msm", "pyemma"],
    "QM/MM": ["qm/mm", "qmmm"],
    "催化": ["催化", "catalysis"],
    "可重复性": ["可重复性", "复现", "reproducibility", "reproducible"],
}

METHOD_TAG_PATTERNS: Dict[str, Sequence[str]] = {
    "TDDFT": ["tddft", "tda-dft", "tda dft"],
    "NTO": ["nto", "自然跃迁轨道"],
    "IFCT": ["ifct"],
    "DFT": [" dft", "dft ", "dft/", "密度泛函"],
    "AIMD": ["aimd", "ab initio molecular dynamics"],
    "QM/MM": ["qm/mm", "qmmm"],
    "NPT": ["npt"],
    "NVT": ["nvt"],
    "NCI": ["nci", "noncovalent interaction", "弱相互作用"],
    "IRI": ["iri"],
    "IGMH": ["igmh"],
    "mIGM": ["migm"],
    "amIGM": ["amigm"],
    "ESP": ["esp", "静电势"],
    "Hirshfeld": ["hirshfeld"],
    "RESP": ["resp"],
    "NICS": ["nics"],
    "LEAE": ["leae", "局部电子附着能"],
    "ALIE": ["alie", "平均局部离子化能"],
    "双描述符": ["双描述符", "dual descriptor"],
    "键级": ["bond order", "键级"],
}

AUTHORITY_ORDER: Dict[str, int] = {"D": 0, "C": 1, "B": 2, "A": 3}


def stable_hash(text: str) -> str:
    """生成稳定 SHA256 哈希。

    功能目的：
        为 source、chunk 和索引版本比较提供稳定指纹。
    输入参数：
        text：待计算哈希的文本。
    返回值：
        十六进制 SHA256 字符串。
    关键流程：
        将文本以 UTF-8 编码后计算 SHA256。
    可能报错或边界情况：
        空字符串也会返回合法哈希，用于表示空内容的稳定指纹。
    """

    return sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    """读取 UTF-8 JSON 文件。

    功能目的：
        统一项目内 JSON 读取方式。
    输入参数：
        path：JSON 文件路径。
    返回值：
        `json.load` 得到的 Python 对象。
    关键流程：
        使用 UTF-8 编码打开文件并解析。
    可能报错或边界情况：
        文件缺失或 JSON 非法时抛出底层异常，避免吞掉构建错误。
    """

    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, payload: Any) -> None:
    """写入 UTF-8 JSON 文件。

    功能目的：
        统一项目内 JSON 产物格式。
    输入参数：
        path：输出路径。
        payload：可 JSON 序列化的数据。
    返回值：
        无。
    关键流程：
        自动创建父目录，使用 `ensure_ascii=False` 保留中文。
    可能报错或边界情况：
        不可序列化对象会抛出 `TypeError`。
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    """读取 UTF-8 JSONL 文件。

    功能目的：
        加载 source、chunk、image 等行式结构化数据。
    输入参数：
        path：JSONL 文件路径。
    返回值：
        每行 JSON 对象组成的列表。
    关键流程：
        跳过空行，逐行 `json.loads`。
    可能报错或边界情况：
        任一行 JSON 非法会抛出异常，并暴露原始行号附近的构建问题。
    """

    records: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def write_jsonl(path: Path, records: Iterable[Dict[str, Any]]) -> None:
    """写入 UTF-8 JSONL 文件。

    功能目的：
        为 normalized 数据和 dense 分片提供可流式读取的产物格式。
    输入参数：
        path：输出路径。
        records：字典记录迭代器。
    返回值：
        无。
    关键流程：
        自动创建父目录，每条记录写为紧凑 JSON 单行。
    可能报错或边界情况：
        某条记录不可序列化会抛出 `TypeError`，构建会停止。
    """

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n")


def detect_language(text: str) -> str:
    """粗略判断文本语言。

    功能目的：
        给 source/chunk 增加语言标签，便于结果展示和未来过滤。
    输入参数：
        text：待判断文本。
    返回值：
        `zh`、`en` 或 `mixed`。
    关键流程：
        统计中日韩统一表意文字和拉丁字母数量。
    可能报错或边界情况：
        纯数字、符号或极短文本返回 `mixed`。
    """

    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_count = len(re.findall(r"[A-Za-z]", text))
    if cjk_count and latin_count:
        return "mixed"
    if cjk_count:
        return "zh"
    if latin_count:
        return "en"
    return "mixed"


def tokenize(text: str) -> List[str]:
    """对中英文混合文本做轻量分词。

    功能目的：
        为 BM25 和查询过滤提供稳定 token，不依赖第三方中文分词包。
    输入参数：
        text：原始文本。
    返回值：
        token 列表。
    关键流程：
        提取英文/数字 token，并对连续中文串加入原串和二元切片。
    可能报错或边界情况：
        很短的中文词只会产生少量 token，这是轻量检索的正常表现。
    """

    lowered = text.lower()
    latin_tokens = re.findall(r"[a-z0-9_\-\./:+*]+", lowered)
    cjk_segments = re.findall(r"[\u4e00-\u9fff]+", lowered)
    cjk_tokens: List[str] = []
    for segment in cjk_segments:
        cjk_tokens.append(segment)
        if len(segment) > 1:
            cjk_tokens.extend(segment[index : index + 2] for index in range(len(segment) - 1))
    return [token for token in [*latin_tokens, *cjk_tokens] if token]


def normalize_whitespace(text: str) -> str:
    """压缩多余空白。

    功能目的：
        让 chunk 文本和 snippet 更稳定，同时保留基本段落语义。
    输入参数：
        text：原始文本。
    返回值：
        清理后的字符串。
    关键流程：
        替换不间断空格，压缩行内空白，限制连续空行数量。
    可能报错或边界情况：
        空字符串会返回空字符串。
    """

    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_frontmatter_markdown(text: str) -> Tuple[Dict[str, Any], str]:
    """解析 Markdown front matter。

    功能目的：
        从学术帖 Markdown 开头提取基础元数据键，同时让正文解析不受 front matter 干扰。
    输入参数：
        text：原始 Markdown 文本。
    返回值：
        `(metadata, body)`，metadata 只做轻量键值解析。
    关键流程：
        仅识别文件开头 `---` 包裹的 header；复杂 YAML 列表不强行完整解析。
    可能报错或边界情况：
        header 非标准时返回空 metadata 和原文，避免因单篇格式问题中断 normalizer。
    """

    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("\n---\n", 1)
    if len(parts) != 2:
        return {}, text
    metadata: Dict[str, Any] = {}
    for line in parts[0][4:].splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("-") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, parts[1]


def extract_tags(text: str, synonyms: Dict[str, Sequence[str]]) -> List[str]:
    """基于同义词表抽取标签。

    功能目的：
        从标题、摘要和正文片段中补充软件/主题标签。
    输入参数：
        text：待匹配文本。
        synonyms：`标签 -> 同义词列表`。
    返回值：
        去重排序后的标签列表。
    关键流程：
        将文本转为小写后做包含匹配，保持实现可解释且无需额外依赖。
    可能报错或边界情况：
        包含匹配可能略宽松，因此 registry 会优先保留 manifest 中已有高质量标签。
    """

    lowered = text.lower()
    results: List[str] = []
    for tag, patterns in synonyms.items():
        if any(pattern.lower() in lowered for pattern in patterns):
            results.append(tag)
    return sorted(set(results))


def extract_method_tags(text: str) -> List[str]:
    """抽取方法学标签。

    功能目的：
        给检索结果提供更细粒度的方法提示，例如 TDDFT、NCI、IGMH。
    输入参数：
        text：标题、小节路径和 chunk 正文拼接后的文本。
    返回值：
        去重排序后的方法标签。
    关键流程：
        使用固定关键词表做小写包含匹配。
    可能报错或边界情况：
        方法缩写可能有歧义，结果用于提示而不是硬性事实判断。
    """

    lowered = text.lower()
    results: List[str] = []
    for tag, patterns in METHOD_TAG_PATTERNS.items():
        if any(pattern.lower() in lowered for pattern in patterns):
            results.append(tag)
    return sorted(set(results))


def extract_version_hints(text: str) -> str | None:
    """抽取软件版本或日期提示。

    功能目的：
        为 trace_source 提供可追溯的版本线索。
    输入参数：
        text：标题、摘要或手册前几页文本。
    返回值：
        版本提示字符串；无命中时返回 `None`。
    关键流程：
        匹配常见软件名加版本、`Version x.y` 和日期化版本表达。
    可能报错或边界情况：
        多个版本会去重后用分号连接，不判断哪个版本最权威。
    """

    patterns = [
        r"(?:multiwfn|gaussian|orca|gromacs|cp2k|xtb)\s*[vV]?\d+(?:\.\d+){0,3}",
        r"version\s+\d+(?:\.\d+){0,3}",
        r"\d{4}-[A-Za-z]{3}-\d{1,2}",
        r"\d{4}-\d{2}-\d{2}",
    ]
    hits: List[str] = []
    for pattern in patterns:
        hits.extend(re.findall(pattern, text, flags=re.IGNORECASE))
    unique_hits = sorted({hit.strip() for hit in hits if hit.strip()})
    return "; ".join(unique_hits) if unique_hits else None


def split_paragraph_to_chunks(text: str, target_size: int = 700, max_size: int = 900) -> List[str]:
    """将长文本切成适合检索的 chunk。

    功能目的：
        避免单个 chunk 太长导致 BM25 稀释和 MCP 返回上下文过大。
    输入参数：
        text：待切分文本。
        target_size：自然切分目标长度。
        max_size：单 chunk 最大长度。
    返回值：
        chunk 文本列表。
    关键流程：
        优先按中英文句末标点切分；极端长句再按固定窗口兜底。
    可能报错或边界情况：
        无标点长文本会被硬切，但仍保持原文顺序。
    """

    cleaned = normalize_whitespace(text)
    if len(cleaned) <= max_size:
        return [cleaned] if cleaned else []
    sentences = re.split(r"(?<=[。！？；.;!?])", cleaned)
    chunks: List[str] = []
    buffer = ""
    for sentence in sentences:
        if not sentence:
            continue
        if len(buffer) + len(sentence) > max_size and buffer:
            chunks.append(buffer.strip())
            buffer = sentence
            continue
        buffer += sentence
        if len(buffer) >= target_size:
            chunks.append(buffer.strip())
            buffer = ""
    if buffer.strip():
        chunks.append(buffer.strip())
    refined: List[str] = []
    for chunk in chunks:
        if len(chunk) <= max_size:
            refined.append(chunk)
            continue
        for start in range(0, len(chunk), max_size):
            piece = chunk[start : start + max_size].strip()
            if piece:
                refined.append(piece)
    return refined


def authority_meets(level: str, threshold: str | None) -> bool:
    """判断 source 权威等级是否满足最低要求。

    功能目的：
        支持 `sobko_search` 的 `authority_at_least` 过滤参数。
    输入参数：
        level：当前 source/chunk 的权威等级。
        threshold：最低权威等级；为空表示不过滤。
    返回值：
        满足条件返回 True。
    关键流程：
        使用 `AUTHORITY_ORDER` 映射做数值比较。
    可能报错或边界情况：
        未知等级按最低等级以下处理，避免误判为高权威。
    """

    if not threshold:
        return True
    return AUTHORITY_ORDER.get(level, -1) >= AUTHORITY_ORDER.get(threshold, -1)


def make_snippet(text: str, limit: int = 260) -> str:
    """生成简洁 snippet。

    功能目的：
        控制 MCP 检索结果体积，避免一次返回大段原文。
    输入参数：
        text：原始文本。
        limit：最大字符数。
    返回值：
        截断后的片段。
    关键流程：
        先清理空白，再按字符数截断并加省略号。
    可能报错或边界情况：
        limit 太小时仍返回可读字符串；空文本返回空文本。
    """

    cleaned = normalize_whitespace(text)
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: max(1, limit - 1)].rstrip() + "…"
