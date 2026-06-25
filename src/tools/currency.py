"""Real-time currency conversion tool."""

from __future__ import annotations

import random
from typing import Any


class CurrencyTool:
    """Convert currencies using (simulated) real-time exchange rates."""

    name = "currency"
    description = "查询实时汇率并进行货币换算"
    input_schema = {
        "type": "object",
        "properties": {
            "amount": {"type": "number", "description": "金额"},
            "from_currency": {"type": "string", "description": "源币种"},
            "to_currency": {"type": "string", "description": "目标币种"},
        },
        "required": ["amount", "from_currency"],
    }

    # Approximate rates (replace with real API in production)
    RATES_TO_CNY = {
        "JPY": 0.0487,
        "KRW": 0.0053,
        "USD": 7.25,
        "EUR": 7.85,
        "AUD": 4.72,
        "GBP": 9.15,
        "CNY": 1.0,
    }

    async def execute(
        self,
        amount: float,
        from_currency: str,
        to_currency: str = "CNY",
    ) -> dict[str, Any]:
        """Convert amount between currencies."""
        from_rate = self.RATES_TO_CNY.get(from_currency.upper(), 1.0)
        to_rate = self.RATES_TO_CNY.get(to_currency.upper(), 1.0)

        cny_amount = amount * from_rate
        converted = cny_amount / to_rate

        # Simulate slight fluctuation
        trend = random.choice(["↑ 走强", "→ 持平", "↓ 走弱"])
        trend_pct = random.uniform(-2, 2)

        return {
            "tool": self.name,
            "status": "success",
            "data": {
                "amount": amount,
                "from_currency": from_currency.upper(),
                "to_currency": to_currency.upper(),
                "rate": round(to_rate / from_rate, 4),
                "converted": round(converted, 2),
                "cny_equivalent": round(cny_amount, 2),
                "trend": trend,
                "trend_pct": round(trend_pct, 1),
                "advice": "现在购买较划算" if trend_pct < 0 else "建议观望",
            },
        }
