"""Intent Parser Agent — classifies user queries and extracts entities.

This is the first agent in the pipeline. It determines which downstream
agents need to be activated based on the user's intent.
"""

from __future__ import annotations

import json
import time
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.config import settings


INTENT_CATEGORIES = {
    "price_compare": "比价、价格差异、多少钱、便宜、贵",
    "logistics": "物流、运费、关税、直邮、多久到、清关",
    "compliance": "合规、法规、能不能寄、禁运、认证、成分",
    "product_search": "推荐、找商品、有什么好物、类似、替代",
    "review_analysis": "评价、口碑、好不好、用户反馈、评分",
    "copywriting": "文案、标题、描述、营销、推广素材",
    "strategy": "运营、策略、怎么做、市场分析、推广方案",
    "currency": "汇率、换算、日元、美元、欧元",
}

SYSTEM_PROMPT = f"""你是一个跨境电商平台的意图解析Agent。

你的职责：
1. 分析用户的自然语言输入
2. 识别用户意图（从以下类别中选择）
3. 提取关键实体（商品名、类别、国家等）

意图类别：
{json.dumps(INTENT_CATEGORIES, ensure_ascii=False, indent=2)}

输出JSON格式：
{{"intent": "类别名", "confidence": 0.0-1.0, "entities": {{"product": "", "category": "", "origin": "", "market": ""}}}}
"""


class IntentParserAgent:
    """Parse user intent and extract entities from natural language."""

    name = "intent_parser"
    role = "需求解析"
    icon = "🔍"

    def __init__(self, llm=None):
        from src.config import settings
        if llm:
            self.llm = llm
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=settings.llm.model,
                temperature=0.1,
                api_key=settings.llm.api_key,
                base_url=settings.llm.base_url,
            )

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Parse intent from the user query."""
        start = time.time()
        query = state.get("query", "")

        # Simple keyword-based fallback when no LLM available
        intent, confidence, entities = self._keyword_parse(query)

        try:
            # Try LLM-based parsing for higher accuracy
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"用户输入: {query}"),
            ]
            resp = await self.llm.ainvoke(messages)
            parsed = json.loads(resp.content)
            intent = parsed.get("intent", intent)
            confidence = parsed.get("confidence", confidence)
            entities = parsed.get("entities", entities)
        except Exception:
            pass  # Fall back to keyword parsing

        latency = int((time.time() - start) * 1000)

        return {
            "intent": intent,
            "intent_confidence": confidence,
            "entities": entities,
            "agent_trace": [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
            }],
        }

    def _keyword_parse(self, query: str) -> tuple[str, float, dict]:
        """Keyword-based intent parsing as fallback."""
        q = query.lower()
        best_intent = "product_search"
        best_score = 0.0

        keywords_map = {
            "price_compare": ["比价", "价格", "多少钱", "便宜", "贵", "差价", "省"],
            "logistics": ["物流", "运费", "关税", "直邮", "多久", "清关", "快递"],
            "compliance": ["合规", "法规", "禁运", "认证", "成分", "能不能寄"],
            "product_search": ["推荐", "找", "好物", "类似", "替代", "有什么"],
            "review_analysis": ["评价", "口碑", "好不好", "反馈", "评分"],
            "copywriting": ["文案", "标题", "描述", "营销"],
            "strategy": ["运营", "策略", "怎么做", "方案", "推广"],
            "currency": ["汇率", "换算", "日元", "美元"],
        }

        for intent, keywords in keywords_map.items():
            score = sum(1 for kw in keywords if kw in q)
            if score > best_score:
                best_score = score
                best_intent = intent

        confidence = min(0.5 + best_score * 0.15, 0.95) if best_score > 0 else 0.3

        # Extract product entity
        product = ""
        for kw in ["神仙水", "鱼油", "面膜", "精华", "白桃", "SK-II", "Swisse"]:
            if kw.lower() in q:
                product = kw
                break

        return best_intent, confidence, {
            "product": product,
            "category": "",
            "origin": "",
            "market": "CN",
        }
