# (c)2026 WangTianJiao anlan-dev | GPL-3.0 | 保留作者署名 attribution required
"""意图解析的纯函数工具层（不依赖 langchain，可独立评测）。

把 keyword fallback 与 LLM JSON 容错解析抽出来，目的：
1. 无 LLM 环境也能单测意图路由准确率（评测驱动开发的起点）
2. 单一来源维护意图类别定义，避免 intent_parser 内联逻辑膨胀
3. 结构化输出解析集中处理，LLM 输出格式漂移不再导致静默降级
"""

from __future__ import annotations

import json
import re
from typing import Any

# 意图类别定义（唯一权威来源）
INTENT_CATEGORIES: dict[str, str] = {
    "price_compare": "比价、价格差异、多少钱、便宜、贵",
    "logistics": "物流、运费、关税、直邮、多久到、清关",
    "compliance": "合规、法规、能不能寄、禁运、认证、成分",
    "product_search": "推荐、找商品、有什么好物、类似、替代",
    "review_analysis": "评价、口碑、好不好、用户反馈、评分",
    "copywriting": "文案、标题、描述、营销、推广素材",
    "strategy": "运营、策略、怎么做、市场分析、推广方案",
    "currency": "汇率、换算、日元、美元、欧元",
}

# keyword fallback 的关键词映射（确定性、可评测）
KEYWORDS_MAP: dict[str, list[str]] = {
    "price_compare": ["比价", "价格", "多少钱", "便宜", "贵", "差价", "省"],
    "logistics": ["物流", "运费", "关税", "直邮", "多久", "清关", "快递"],
    "compliance": ["合规", "法规", "禁运", "认证", "成分", "能不能寄"],
    "product_search": ["推荐", "找", "好物", "类似", "替代", "有什么"],
    "review_analysis": ["评价", "口碑", "好不好", "反馈", "评分"],
    "copywriting": ["文案", "标题", "描述", "营销"],
    "strategy": ["运营", "策略", "怎么做", "方案", "推广"],
    "currency": ["汇率", "换算", "日元", "美元", "欧元", "人民币", "兑换", "港币"],
}

# 商品实体提示（提取 product 字段用）
PRODUCT_HINTS: list[str] = [
    "神仙水", "鱼油", "面膜", "精华", "白桃", "SK-II", "Swisse",
    "白色恋人", "面霜", "眼霜", "口红", "粉底",
]


def keyword_parse(query: str) -> tuple[str, float, dict[str, Any]]:
    """Keyword-based intent parsing（确定性，用于无 LLM 时的 fallback 与评测）。

    Returns:
        (intent, confidence, entities)
    """
    q = query.lower()
    best_intent = "product_search"
    best_score = 0.0

    for intent, keywords in KEYWORDS_MAP.items():
        score = sum(1 for kw in keywords if kw in q)
        if score > best_score:
            best_score = score
            best_intent = intent

    confidence = min(0.5 + best_score * 0.15, 0.95) if best_score > 0 else 0.3

    product = ""
    for kw in PRODUCT_HINTS:
        if kw.lower() in q:
            product = kw
            break

    return best_intent, confidence, {
        "product": product,
        "category": "",
        "origin": "",
        "market": "CN",
    }


def parse_llm_json(content: Any) -> dict[str, Any] | None:
    """容错解析 LLM 输出的 JSON（结构化输出健壮性核心）。

    处理三类常见漂移：
    1. LLM 返回 dict/list（某些 provider 直接返回结构化对象）
    2. markdown 代码块包裹（```json ... ``` / ``` ... ```）
    3. JSON 前后夹带解释文字（"好的，结果如下：{...}"）

    Returns:
        解析成功的 dict；失败返回 None（由调用方回退 keyword）。
    """
    if content is None:
        return None

    # 1. 已经是 dict → 直接返回
    if isinstance(content, dict):
        return content

    if isinstance(content, list):
        return None

    text = str(content).strip()
    if not text:
        return None

    # 2. 剥离 markdown 代码块围栏
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)```", text, flags=re.IGNORECASE)
    if fenced:
        text = fenced.group(1).strip()

    # 3. 直接尝试
    try:
        obj = json.loads(text)
        return obj if isinstance(obj, dict) else None
    except (json.JSONDecodeError, TypeError):
        pass

    # 4. 提取第一个 { 到最后一个 } 之间的子串（夹带文字时）
    brace = re.search(r"\{[\s\S]*\}", text)
    if brace:
        try:
            obj = json.loads(brace.group(0))
            return obj if isinstance(obj, dict) else None
        except (json.JSONDecodeError, TypeError):
            pass

    return None
