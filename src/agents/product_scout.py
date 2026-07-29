"""Product Scout Agent — MCP router + scenario-driven decisions."""

from __future__ import annotations
import time
from typing import Any, Optional


class ProductScoutAgent:
    name = "product_scout"
    role = "选品分析"
    icon = "🛍️"

    def __init__(self, mcp: Optional[Any] = None):
        self.mcp = mcp

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        start = time.time()
        entities = state.get("entities", {})
        query = state.get("query", "")
        product = entities.get("product", "白桃精华")

        if self.mcp:
            price_result = await self.mcp.call("price_compare", product_name=product)
            review_result = await self.mcp.call("review_analyze", product_name=product)
        else:
            from src.tools.price_compare import PriceCompareTool
            from src.tools.review_analyze import ReviewAnalyzeTool
            price_result = await PriceCompareTool().execute(product_name=product)
            review_result = await ReviewAnalyzeTool().execute(product_name=product)

        latency = int((time.time() - start) * 1000)
        price_data = price_result.get("data", {})
        review_data = review_result.get("data", {})
        review_score = review_data.get("positive_rate", 0)
        recommendation = "推荐购买" if review_score > 90 else "建议观望" if review_score > 80 else "风险较高"

        from src.data.scenarios import ScenarioStore
        scenario = ScenarioStore.find(query)
        decision = ""
        if scenario:
            dc = scenario.get("decision_chain", {})
            decision = f"[价差: {dc.get('price', '')}] → {recommendation}"

        return {
            "product_analysis": {
                "agent": self.name, "status": "success",
                "data": {"product": product, "lowest_price": price_data.get("lowest_price"),
                         "lowest_platform": price_data.get("lowest_platform"),
                         "price_spread": price_data.get("price_range", {}).get("spread"),
                         "review_score": review_score, "total_reviews": review_data.get("total_reviews"),
                         "recommendation": recommendation},
                "latency_ms": latency, "tokens_used": 0, "decision": decision,
            },
            "price_comparison": price_result,
            "agent_trace": state.get("agent_trace", []) + [{"agent": self.name, "latency_ms": latency, "status": "success"}],
        }
