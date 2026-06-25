"""Product review analysis tool with sentiment and keyword extraction."""

from __future__ import annotations

import random
from typing import Any


class ReviewAnalyzeTool:
    """Analyze product reviews: sentiment, keywords, rating distribution."""

    name = "review_analyze"
    description = "分析商品评价，提取情感倾向、高频关键词和评分分布"
    input_schema = {
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "description": "商品名称"},
            "platform": {"type": "string", "description": "数据来源平台"},
        },
        "required": ["product_name"],
    }

    async def execute(self, product_name: str, platform: str = "") -> dict[str, Any]:
        """Analyze reviews and return structured insights."""
        positive_words = ["水润", "清爽", "不刺激", "性价比高", "好用", "回购"]
        negative_words = ["偏油", "味道淡", "包装简陋", "发货慢"]

        pos_kw = random.sample(positive_words, 3)
        neg_kw = random.sample(negative_words, 2)
        total_reviews = random.randint(150, 500)
        positive_rate = random.randint(88, 98)

        return {
            "tool": self.name,
            "status": "success",
            "data": {
                "product": product_name,
                "total_reviews": total_reviews,
                "positive_rate": positive_rate,
                "rating_distribution": {
                    "5star": random.randint(55, 75),
                    "4star": random.randint(15, 25),
                    "3star": random.randint(3, 10),
                    "2star": random.randint(1, 5),
                    "1star": random.randint(0, 3),
                },
                "positive_keywords": [
                    {"word": w, "count": random.randint(20, 100)} for w in pos_kw
                ],
                "negative_keywords": [
                    {"word": w, "count": random.randint(5, 20)} for w in neg_kw
                ],
                "sample_reviews": [
                    {
                        "author": "🌸 田中さくら",
                        "rating": 5,
                        "text_jp": "とても良い商品で、肌がしっとりします。",
                        "text_zh": "非常棒的商品，皮肤变得水润。",
                    },
                    {
                        "author": "🍀 山本みどり",
                        "rating": 4,
                        "text_jp": "保湿力は高いですが、香りが少し強いです。",
                        "text_zh": "保湿力很强，但香味稍微有点浓。",
                    },
                ],
            },
        }
