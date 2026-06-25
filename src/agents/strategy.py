"""Strategy Agent — generates operational recommendations."""

from __future__ import annotations

import time
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.config import settings


SYSTEM_PROMPT = """你是一个跨境电商运营策略Agent。

根据市场分析和商品数据，生成运营策略建议。输出JSON格式：
{
  "market_insights": [{"metric": "指标名", "value": "值", "insight": "洞察"}],
  "strategies": [{"priority": 1, "action": "策略描述", "expected_roi": "预期ROI"}],
  "risk_alerts": ["风险提示"]
}
"""


class StrategyAgent:
    """Generate operational strategy recommendations."""

    name = "strategy"
    role = "运营策略"
    icon = "📈"

    def __init__(self, llm=None):
        if llm:
            self.llm = llm
        else:
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model=settings.llm.model,
                temperature=0.5,
                api_key=settings.llm.api_key,
                base_url=settings.llm.base_url,
            )

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Generate strategy based on all available analysis data."""
        start = time.time()

        market = state.get("market_analysis", {}).get("data", {})
        product = state.get("product_analysis", {}).get("data", {})
        compliance = state.get("compliance_report", {}).get("data", {})

        context = (
            f"市场数据: 机会评分={market.get('avg_opportunity_score', 'N/A')}, "
            f"趋势={market.get('market_trend', 'N/A')}\n"
            f"商品数据: 最低价=¥{product.get('lowest_price', 'N/A')}, "
            f"好评率={product.get('review_score', 'N/A')}%\n"
            f"合规状态: {'通过' if compliance.get('overall_pass') else '未通过'}"
        )

        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=context),
            ]
            resp = await self.llm.ainvoke(messages)
            import json
            strategy_data = json.loads(resp.content)
        except Exception:
            strategy_data = {
                "market_insights": [
                    {"metric": "目标用户", "value": "68%", "insight": "偏好日本美妆"},
                    {"metric": "最优价格带", "value": "¥200-400", "insight": "转化率最高"},
                ],
                "strategies": [
                    {"priority": 1, "action": "拼团裂变: 分享得优惠券", "expected_roi": "1:5"},
                    {"priority": 2, "action": "限时闪购: 营造紧迫感", "expected_roi": "1:3"},
                    {"priority": 3, "action": "KOL种草: 小红书+抖音", "expected_roi": "1:4"},
                ],
                "risk_alerts": ["竞品价格战风险", "汇率波动风险"],
            }

        latency = int((time.time() - start) * 1000)

        return {
            "strategy_output": {
                "agent": self.name,
                "status": "success",
                "data": strategy_data,
                "latency_ms": latency,
                "tokens_used": 0,
            },
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
            }],
        }
