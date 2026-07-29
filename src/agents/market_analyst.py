"""Market Analyst Agent — MCP router + scenario-driven decisions."""

from __future__ import annotations
import time
from typing import Any, Optional


class MarketAnalystAgent:
    name = "market_analyst"
    role = "市场调研"
    icon = "📊"

    def __init__(self, mcp: Optional[Any] = None):
        self.mcp = mcp

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        start = time.time()
        entities = state.get("entities", {})
        query = state.get("query", "")
        product = entities.get("product", "")
        category = entities.get("category", "")

        if self.mcp:
            search_result = await self.mcp.call("product_search", query=product, category=category)
            fx_result = await self.mcp.call("currency", amount=1000, from_currency="JPY")
        else:
            from src.tools.product_search import ProductSearchTool
            from src.tools.currency import CurrencyTool
            search_result = await ProductSearchTool().execute(query=product, category=category)
            fx_result = await CurrencyTool().execute(amount=1000, from_currency="JPY")

        latency = int((time.time() - start) * 1000)
        products = search_result.get("data", {}).get("products", [])
        avg_opp = (sum(p.get("opportunity_score", 0) for p in products) / len(products)) if products else 0
        trend = "↑ 上升" if avg_opp > 75 else "→ 平稳" if avg_opp > 50 else "↓ 谨慎"

        from src.data.scenarios import ScenarioStore
        scenario = ScenarioStore.find(query)
        decision = ""
        if scenario:
            dc = scenario.get("decision_chain", {})
            decision = f"[{dc.get('price', '')}] → {dc.get('recommendation', '')}"

        return {
            "market_analysis": {
                "agent": self.name, "status": "success",
                "data": {"products_found": len(products), "avg_opportunity_score": round(avg_opp, 1),
                         "market_trend": trend, "fx_rate": fx_result.get("data", {}), "top_products": products[:3]},
                "latency_ms": latency, "tokens_used": 0, "decision": decision,
            },
            "agent_trace": state.get("agent_trace", []) + [{"agent": self.name, "latency_ms": latency, "status": "success"}],
        }
