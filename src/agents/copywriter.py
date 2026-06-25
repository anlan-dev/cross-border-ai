"""Copywriter Agent — generates multilingual marketing copy."""

from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.config import settings


SYSTEM_PROMPT = """你是一个跨境电商文案生成Agent。

根据商品信息生成以下营销素材（中文）：
1. 商品标题（含关键词，≤30字）
2. 社交媒体种草文案（含emoji，≤100字）
3. EDM邮件标题（A/B两个版本）

输出JSON格式：
{
  "title": "商品标题",
  "social_copy": "种草文案",
  "email_subjects": ["A版本", "B版本"]
}
"""


class CopywriterAgent:
    """Generate multilingual marketing copy for products."""

    name = "copywriter"
    role = "文案生成"
    icon = "✍️"

    def __init__(self, llm=None):
        if llm:
            self.llm = llm
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=settings.llm.model,
                temperature=0.7,
                api_key=settings.llm.api_key,
                base_url=settings.llm.base_url,
            )

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate marketing copy based on product analysis."""
        start = time.time()
        entities = state.get("entities", {})
        product = entities.get("product", "跨境好物")

        product_info = state.get("product_analysis", {}).get("data", {})
        price = product_info.get("lowest_price", "N/A")

        prompt = f"商品: {product}\n价格: ¥{price}\n评分: {product_info.get('review_score', 'N/A')}"

        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=prompt),
            ]
            resp = await self.llm.ainvoke(messages)
            import json
            copy_data = json.loads(resp.content)
        except Exception:
            # Fallback template
            copy_data = {
                "title": f"{product} · 跨境直邮 · 正品保障",
                "social_copy": f"🍑 发现宝藏好物！{product}跨境拼团价只要¥{price}，比国内省超多！限时开团中～ #跨境好物 #正品直邮",
                "email_subjects": [
                    f"🔥 限时拼团 | {product} ¥{price}，跨境直邮",
                    f"🍑 你的购物车里少了它！{product}拼团价揭晓",
                ],
            }

        latency = int((time.time() - start) * 1000)

        return {
            "copywriting_output": {
                "agent": self.name,
                "status": "success",
                "data": copy_data,
                "latency_ms": latency,
                "tokens_used": 0,
            },
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
            }],
        }
