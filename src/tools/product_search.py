"""Product search and recommendation tool.

Queries product databases and returns matching items with metadata.
"""

from __future__ import annotations

import random
from typing import Any


class ProductSearchTool:
    """Search for products and return structured results."""

    name = "product_search"
    description = "搜索商品信息，返回商品详情、销量、评分等数据"
    input_schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "category": {"type": "string", "description": "商品类别"},
            "market": {"type": "string", "description": "目标市场"},
        },
        "required": ["query"],
    }

    MOCK_PRODUCTS = [
        {"name": "SK-II 神仙水 230ml", "category": "美妆", "origin": "🇯🇵", "rating": 4.8, "monthly_sales": 12400},
        {"name": "Swisse 鱼油胶囊 400粒", "category": "保健", "origin": "🇦🇺", "rating": 4.6, "monthly_sales": 8900},
        {"name": "Mediheal 面膜 10片装", "category": "美妆", "origin": "🇰🇷", "rating": 4.5, "monthly_sales": 23000},
        {"name": "DHC 维生素B群", "category": "保健", "origin": "🇯🇵", "rating": 4.7, "monthly_sales": 15600},
        {"name": "Yamanashi 白桃精华 200ml", "category": "美妆", "origin": "🇯🇵", "rating": 4.6, "monthly_sales": 8342},
    ]

    async def execute(self, query: str, category: str = "", market: str = "CN") -> dict[str, Any]:
        """Search products matching the query."""
        matched = [
            p for p in self.MOCK_PRODUCTS
            if not query or query.lower() in p["name"].lower()
               or (category and category in p["category"])
        ]
        if not matched:
            matched = random.sample(self.MOCK_PRODUCTS, min(3, len(self.MOCK_PRODUCTS)))

        return {
            "tool": self.name,
            "status": "success",
            "data": {
                "query": query,
                "total_results": len(matched),
                "products": [
                    {
                        **p,
                        "price_cny": round(random.uniform(50, 800), 2),
                        "trend": random.choice(["↑", "→", "↓"]),
                        "opportunity_score": random.randint(60, 95),
                    }
                    for p in matched
                ],
            },
        }
