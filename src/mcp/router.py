"""MCP Router — dispatches tool calls to registered tool implementations.

The router acts as the central bus that agents use to invoke tools.
It handles tool discovery, invocation, and error handling.
"""

from __future__ import annotations

import time
from typing import Any

from src.mcp.protocol import MCPMessage, MCPToolSpec
from src.tools.price_compare import PriceCompareTool
from src.tools.product_search import ProductSearchTool
from src.tools.logistics import LogisticsTool
from src.tools.compliance_check import ComplianceCheckTool
from src.tools.currency import CurrencyTool
from src.tools.review_analyze import ReviewAnalyzeTool


class MCPRouter:
    """Central router for MCP tool invocations.

    Usage:
        router = MCPRouter()
        tools = router.list_tools()          # discover available tools
        result = await router.call("price_compare", product_name="SK-II")
    """

    def __init__(self):
        self._tools: dict[str, Any] = {}
        self._register_defaults()

    def _register_defaults(self):
        """Register all built-in tools."""
        for tool_cls in [
            PriceCompareTool,
            ProductSearchTool,
            LogisticsTool,
            ComplianceCheckTool,
            CurrencyTool,
            ReviewAnalyzeTool,
        ]:
            tool = tool_cls()
            self._tools[tool.name] = tool

    def register(self, tool: Any) -> None:
        """Register a custom tool."""
        self._tools[tool.name] = tool

    def list_tools(self) -> list[MCPToolSpec]:
        """Return specs for all registered tools (MCP discovery)."""
        return [
            MCPToolSpec(
                name=t.name,
                description=t.description,
                input_schema=t.input_schema,
            )
            for t in self._tools.values()
        ]

    async def handle_message(self, message: MCPMessage) -> MCPMessage:
        """Handle an incoming MCP message."""
        if message.method == "tools/list":
            specs = [s.to_dict() for s in self.list_tools()]
            return message.success(specs)

        if message.method == "tools/call":
            tool_name = message.params.get("name")
            args = message.params.get("arguments", {})
            result = await self.call(tool_name, **args)
            if "error" in result:
                return message.fail(result["error"])
            return message.success(result)

        return message.fail(f"Unknown method: {message.method}")

    async def call(self, tool_name: str, **kwargs) -> dict[str, Any]:
        """Call a tool by name and return its result."""
        tool = self._tools.get(tool_name)
        if not tool:
            return {
                "tool": tool_name,
                "status": "error",
                "error": f"Tool not found: {tool_name}",
            }

        start = time.time()
        try:
            result = await tool.execute(**kwargs)
            result["latency_ms"] = int((time.time() - start) * 1000)
            return result
        except Exception as e:
            return {
                "tool": tool_name,
                "status": "error",
                "error": str(e),
                "latency_ms": int((time.time() - start) * 1000),
            }
