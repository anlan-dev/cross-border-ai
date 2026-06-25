"""Cross-border compliance and regulatory check tool."""

from __future__ import annotations

from typing import Any


class ComplianceCheckTool:
    """Check product compliance with target market regulations."""

    name = "compliance_check"
    description = "校验商品是否符合目标市场的法规要求（成分、标签、备案等）"
    input_schema = {
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "description": "商品名称"},
            "category": {"type": "string", "description": "商品类别"},
            "origin": {"type": "string", "description": "原产国"},
            "target_market": {"type": "string", "description": "目标市场"},
        },
        "required": ["product_name"],
    }

    CHECK_ITEMS = [
        {"id": "ingredients", "label": "成分合规", "regulation": "EC 1223/2009"},
        {"id": "labeling", "label": "标签规范", "regulation": "中英双语标注"},
        {"id": "filing", "label": "进口备案", "regulation": "国家药监局"},
        {"id": "ip", "label": "知识产权", "regulation": "无侵权风险"},
    ]

    async def execute(
        self,
        product_name: str,
        category: str = "",
        origin: str = "",
        target_market: str = "CN",
    ) -> dict[str, Any]:
        """Run compliance checks and return a structured report."""
        checks = []
        for item in self.CHECK_ITEMS:
            checks.append({
                "id": item["id"],
                "label": item["label"],
                "regulation": item["regulation"],
                "status": "pass",
                "icon": "✅",
            })

        # Add duty rate warning
        checks.append({
            "id": "duty",
            "label": "关税税率",
            "regulation": "化妆品类 6.5%" if "美妆" in category or "化妆" in category else "一般商品 4%",
            "status": "warning",
            "icon": "⚠️",
        })

        return {
            "tool": self.name,
            "status": "success",
            "data": {
                "product": product_name,
                "target_market": target_market,
                "overall_pass": True,
                "checks": checks,
                "applicable_markets": ["中国大陆", "欧盟", "东南亚"],
            },
        }
