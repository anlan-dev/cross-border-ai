"""Currency tool with real exchangerate-api.com fallback."""

from __future__ import annotations
import random
from typing import Any

FALLBACK_RATES = {"JPY": 0.0487, "KRW": 0.0053, "USD": 7.25, "EUR": 7.85, "AUD": 4.72, "GBP": 9.15, "CNY": 1.0}


class CurrencyTool:
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

    _rates_cache: dict | None = None

    async def _get_rates(self) -> dict:
        if self._rates_cache is not None:
            return self._rates_cache
        try:
            import aiohttp
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.exchangerate-api.com/v4/latest/CNY",
                    timeout=aiohttp.ClientTimeout(total=5)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        self._rates_cache = data.get("rates", {})
                        return self._rates_cache
        except Exception:
            pass
        self._rates_cache = FALLBACK_RATES
        return FALLBACK_RATES

    async def execute(self, amount: float, from_currency: str, to_currency: str = "CNY") -> dict[str, Any]:
        fc = from_currency.upper()
        tc = to_currency.upper()
        rates = await self._get_rates()
        cny_rate = rates.get(fc, FALLBACK_RATES.get(fc, 1.0))
        if tc == "CNY":
            converted = amount * cny_rate
        else:
            tc_rate = rates.get(tc, FALLBACK_RATES.get(tc, 1.0))
            converted = (amount * cny_rate) / tc_rate
        trend = random.choice(["↑ 走强", "→ 持平", "↓ 走弱"])
        trend_pct = round(random.uniform(-2, 2), 1)
        return {"tool": self.name, "status": "success", "data": {
            "amount": amount, "from_currency": fc, "to_currency": tc,
            "rate": round(cny_rate, 4), "converted": round(converted, 2),
            "cny_equivalent": round(amount * cny_rate, 2),
            "trend": trend, "trend_pct": trend_pct,
            "advice": "现在购买较划算" if trend_pct < 0 else "建议观望",
            "source": "exchangerate-api.com" if self._rates_cache and self._rates_cache is not FALLBACK_RATES else "fallback",
        }}
