"""Compliance Agent — MCP router + scenario-driven decisions."""

from __future__ import annotations
import time
from typing import Any, Optional


class ComplianceAgent:
    name = "compliance"
    role = "合规审核"
    icon = "🛡️"

    def __init__(self, mcp: Optional[Any] = None):
        self.mcp = mcp

    async def run(self, state: dict[str, Any]) -> dict[str, Any]:
        start = time.time()
        entities = state.get("entities", {})
        query = state.get("query", "")

        if self.mcp:
            result = await self.mcp.call("compliance_check",
                product_name=entities.get("product", ""),
                category=entities.get("category", ""),
                origin=entities.get("origin", ""),
                target_market=entities.get("market", "CN"))
        else:
            from src.tools.compliance_check import ComplianceCheckTool
            result = await ComplianceCheckTool().execute(
                product_name=entities.get("product", ""),
                category=entities.get("category", ""),
                origin=entities.get("origin", ""),
                target_market=entities.get("market", "CN"))

        from src.data.scenarios import ScenarioStore
        scenario = ScenarioStore.find(query)
        decision = ""
        if scenario:
            dc = scenario.get("decision_chain", {})
            decision = f"[{dc.get('compliance', '')}] → {dc.get('recommendation', '')}"

        latency = int((time.time() - start) * 1000)
        result["latency_ms"] = latency
        result["tokens_used"] = 0
        result["decision"] = decision

        return {
            "compliance_report": result,
            "agent_trace": state.get("agent_trace", []) + [{"agent": self.name, "latency_ms": latency, "status": "success"}],
        }
