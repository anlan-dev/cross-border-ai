"""Tests for the multi-agent pipeline.

Run with: python -m pytest tests/ -v
"""

from __future__ import annotations

import asyncio
import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ── Tool Tests ──────────────────────────────────────────

@pytest.mark.asyncio
async def test_price_compare():
    from src.tools.price_compare import PriceCompareTool
    tool = PriceCompareTool()
    result = await tool.execute(product_name="SK-II")
    assert result["status"] == "success"
    assert "prices" in result["data"]
    assert len(result["data"]["prices"]) > 0


@pytest.mark.asyncio
async def test_product_search():
    from src.tools.product_search import ProductSearchTool
    tool = ProductSearchTool()
    result = await tool.execute(query="精华")
    assert result["status"] == "success"
    assert result["data"]["total_results"] > 0


@pytest.mark.asyncio
async def test_logistics():
    from src.tools.logistics import LogisticsTool
    tool = LogisticsTool()
    result = await tool.execute(origin_country="JP")
    assert result["status"] == "success"
    assert "transit_days" in result["data"]


@pytest.mark.asyncio
async def test_compliance():
    from src.tools.compliance_check import ComplianceCheckTool
    tool = ComplianceCheckTool()
    result = await tool.execute(product_name="白桃精华", category="美妆")
    assert result["status"] == "success"
    assert result["data"]["overall_pass"] is True


@pytest.mark.asyncio
async def test_currency():
    from src.tools.currency import CurrencyTool
    tool = CurrencyTool()
    result = await tool.execute(amount=1000, from_currency="JPY")
    assert result["status"] == "success"
    assert result["data"]["converted"] > 0


@pytest.mark.asyncio
async def test_review_analyze():
    from src.tools.review_analyze import ReviewAnalyzeTool
    tool = ReviewAnalyzeTool()
    result = await tool.execute(product_name="白桃精华")
    assert result["status"] == "success"
    assert result["data"]["positive_rate"] > 0


# ── MCP Router Tests ────────────────────────────────────

@pytest.mark.asyncio
async def test_mcp_router_list():
    from src.mcp.router import MCPRouter
    router = MCPRouter()
    tools = router.list_tools()
    assert len(tools) == 6
    names = {t.name for t in tools}
    assert "price_compare" in names
    assert "logistics" in names


@pytest.mark.asyncio
async def test_mcp_router_call():
    from src.mcp.router import MCPRouter
    router = MCPRouter()
    result = await router.call("currency", amount=100, from_currency="USD")
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_mcp_router_unknown_tool():
    from src.mcp.router import MCPRouter
    router = MCPRouter()
    result = await router.call("nonexistent_tool")
    assert result["status"] == "error"


# ── Agent Tests ─────────────────────────────────────────

@pytest.mark.asyncio
async def test_intent_parser_keyword():
    from src.agents.intent_parser import IntentParserAgent
    agent = IntentParserAgent.__new__(IntentParserAgent)
    # Test keyword parsing directly
    intent, conf, entities = agent._keyword_parse("帮我比价SK-II神仙水")
    assert intent == "price_compare"
    assert conf > 0.5


# ── Workflow Tests ──────────────────────────────────────

@pytest.mark.asyncio
async def test_build_graph():
    from src.graph.workflow import build_graph
    graph = build_graph()
    assert graph is not None
    # Verify graph compiles
    app = graph.compile()
    assert app is not None
