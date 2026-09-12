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
from src.agents.intent_utils import (
    INTENT_CATEGORIES,
    keyword_parse,
    parse_llm_json,
)

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

        # keyword fallback 作为兜底（确定性、可评测）
        intent, confidence, entities = keyword_parse(query)
        llm_status = "fallback"

        try:
            # 尝试 LLM 解析（更高准确率）；解析失败自动回退 keyword
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=f"用户输入: {query}"),
            ]
            resp = await self.llm.ainvoke(messages)
            parsed = parse_llm_json(resp.content)
            if parsed:
                intent = parsed.get("intent", intent)
                confidence = parsed.get("confidence", confidence)
                entities = parsed.get("entities", entities)
                llm_status = "llm"
        except Exception:
            # LLM 不可用 / 输出非 JSON → 保持 keyword 兜底结果
            pass

        latency = int((time.time() - start) * 1000)

        return {
            "intent": intent,
            "intent_confidence": confidence,
            "entities": entities,
            "llm_status": llm_status,
            "agent_trace": [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
                "llm_status": llm_status,
            }],
        }

    def _keyword_parse(self, query: str) -> tuple[str, float, dict]:
        """Keyword-based intent parsing（委托到 intent_utils，保留向后兼容）。"""
        return keyword_parse(query)
