"""Product Scout Agent — finds and evaluates specific products."""

from __future__ import annotations

import time
from typing import Any

from src.tools.price_compare import PriceCompareTool
from src.tools.review_analyze import ReviewAnalyzeTool


class ProductScoutAgent:
    """Search for specific products, compare prices, and evaluate quality."""

    name = "product_scout"
    role = "选品分析"
    icon = "🛍️"

    def __init__(self):
        self.price_compare = PriceCompareTool()
        self.review_analyze = ReviewAnalyzeTool()

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Find products, compare prices, and analyze reviews."""
        start = time.time()
        entities = state.get("entities", {})
        product = entities.get("product", "白桃精华")

        # Run price comparison and review analysis in parallel
        price_result = await self.price_compare.execute(product_name=product)
        review_result = await self.review_analyze.execute(product_name=product)

        latency = int((time.time() - start) * 1000)

        price_data = price_result.get("data", {})
        review_data = review_result.get("data", {})

        return {
            "product_analysis": {
                "agent": self.name,
                "status": "success",
                "data": {
                    "product": product,
                    "lowest_price": price_data.get("lowest_price"),
                    "lowest_platform": price_data.get("lowest_platform"),
                    "price_spread": price_data.get("price_range", {}).get("spread"),
                    "review_score": review_data.get("positive_rate"),
                    "total_reviews": review_data.get("total_reviews"),
                    "recommendation": "推荐购买" if review_data.get("positive_rate", 0) > 90 else "建议观望",
                },
                "latency_ms": latency,
                "tokens_used": 0,
            },
            "price_comparison": price_result,
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
            }],
        }
