"""Compliance Agent — checks regulatory requirements for cross-border trade."""

from __future__ import annotations

import time
from typing import Any

from src.tools.compliance_check import ComplianceCheckTool


class ComplianceAgent:
    """Verify product compliance with target market regulations."""

    name = "compliance"
    role = "合规审核"
    icon = "🛡️"

    def __init__(self):
        self.compliance_check = ComplianceCheckTool()

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        """Run compliance checks on the product."""
        start = time.time()
        entities = state.get("entities", {})

        result = await self.compliance_check.execute(
            product_name=entities.get("product", ""),
            category=entities.get("category", ""),
            origin=entities.get("origin", ""),
            target_market=entities.get("market", "CN"),
        )

        latency = int((time.time() - start) * 1000)
        result["latency_ms"] = latency
        result["tokens_used"] = 0

        return {
            "compliance_report": result,
            "agent_trace": state.get("agent_trace", []) + [{
                "agent": self.name,
                "latency_ms": latency,
                "status": "success",
            }],
        }
