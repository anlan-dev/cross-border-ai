"""Multi-platform price comparison tool.

Simulates querying prices from major cross-border e-commerce platforms.
In production, this would connect to real APIs or scraping services.
"""

from __future__ import annotations

import random
from typing import Any


class PriceCompareTool:
    """Compare product prices across multiple e-commerce platforms."""

    name = "price_compare"
    description = "查询商品在多个跨境电商平台的价格，返回比价结果"
    input_schema = {
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "description": "商品名称"},
            "category": {"type": "string", "description": "商品类别"},
        },
        "required": ["product_name"],
    }

    # ── Mock data (replace with real API calls in production) ──
    PLATFORMS = [
        {"name": "天猫国际", "icon": "🐱", "markup": 1.0},
        {"name": "京东国际", "icon": "🐶", "markup": 1.05},
        {"name": "考拉海购", "icon": "🐨", "markup": 0.95},
        {"name": "Amazon JP", "icon": "📦", "markup": 1.15},
    ]

    async def execute(self, product_name: str, category: str = "") -> dict[str, Any]:
        """Query prices across platforms and return comparison data."""
        base_price = random.uniform(150, 600)

        results = []
        for platform in self.PLATFORMS:
            price = round(base_price * platform["markup"] + random.uniform(-20, 20), 2)
            results.append({
                "platform": platform["name"],
                "icon": platform["icon"],
                "price": price,
                "currency": "CNY",
            })

        results.sort(key=lambda x: x["price"])

        return {
            "tool": self.name,
            "status": "success",
            "data": {
                "product": product_name,
                "lowest_price": results[0]["price"],
                "lowest_platform": results[0]["platform"],
                "prices": results,
                "price_range": {
                    "min": results[0]["price"],
                    "max": results[-1]["price"],
                    "spread": round(results[-1]["price"] - results[0]["price"], 2),
                },
            },
        }
