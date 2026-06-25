"""Market Analyst Agent — analyzes market trends and demand data."""

from __future__ import annotations

import time
from typing import Any

from src.tools.product_search import ProductSearchTool
from src.tools.currency import CurrencyTool


class MarketAnalystAgent:
    """Analyze market trends, demand, and competition for a product category."""

    name = "market_analyst"
    role = "市场调研"
    icon = "📊"

    def __init__(self):
        self.product_search = ProductSearchTool()
        self.currency = CurrencyTool()

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Run market analysis based on parsed intent and entities."""
        start = time.time()
        entities = state.get("entities", {})
        product = entities.get("product", "")
        category = entities.get("category", "")

        # Search for products in the category
        search_result = await self.product_search.execute(
            query=product, category=category
        )

        # Get currency info for common markets
        fx_result = await self.currency.execute(amount=1000, from_currency="JPY")

        latency = int((time.time() - start) * 1000)

        products = search_result.get("data", {}).get("products", [])
        avg_opportunity = (
            sum(p.get("opportunity_score", 0) for p in products) / len(products)
            if products else 0
        )

        return {
            "market_analysis": {
                "agent": self.name,
                "status": "success",
                "data": {
                    "products_found": len(products),
                    "avg_opportunity_score": round(avg_opportunity, 1),
                    "market_trend": "↑ 上升" if avg_opportunity > 75 else "→ 平稳",
                    "fx_rate": fx_result.get("data", {}),
                    "top_products": products[:3],
                },
                "latency_ms": latency,
                "tokens_used": 0,
            },
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
            }],
        }
