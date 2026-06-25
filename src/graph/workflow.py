"""LangGraph workflow definition.

This module builds the StateGraph that orchestrates all agents.
The pipeline follows this pattern:

    User Query
        │
        ▼
    Intent Parser  ──── classify intent + extract entities
        │
        ▼
    Router  ──── select which agents to activate
        │
        ├──► Market Analyst (parallel)
        ├──► Product Scout  (parallel)
        ├──► Compliance     (parallel)
        │
        ▼
    Copywriter / Strategy  (depends on intent)
        │
        ▼
    Output Compiler  ──── assemble final response
"""

from __future__ import annotations

import time
from typing import Any, Literal

from langgraph.graph import END, StateGraph

from src.graph.state import PipelineState
from src.agents.intent_parser import IntentParserAgent
from src.agents.market_analyst import MarketAnalystAgent
from src.agents.product_scout import ProductScoutAgent
from src.agents.compliance import ComplianceAgent
from src.agents.copywriter import CopywriterAgent
from src.agents.strategy import StrategyAgent

# ── Agent instances ──────────────────────────────────────
intent_parser = IntentParserAgent()
market_analyst = MarketAnalystAgent()
product_scout = ProductScoutAgent()
compliance_agent = ComplianceAgent()
copywriter = CopywriterAgent()
strategy_agent = StrategyAgent()

# ── Intent → Agent routing map ───────────────────────────
# Each intent maps to a set of downstream agents.
INTENT_ROUTES: dict[str, list[str]] = {
    "price_compare":  ["market_analyst", "product_scout"],
    "product_search": ["market_analyst", "product_scout"],
    "logistics":      ["market_analyst", "compliance"],
    "compliance":     ["compliance"],
    "review_analysis":["product_scout"],
    "copywriting":    ["product_scout", "copywriter"],
    "strategy":       ["market_analyst", "product_scout", "compliance", "strategy"],
    "currency":       ["market_analyst"],
}


# ── Node functions ──────────────────────────────────────

async def node_intent_parser(state: PipelineState) -> dict[str, Any]:
    """Parse user intent."""
    return await intent_parser.run(state)


async def node_market_analyst(state: PipelineState) -> dict[str, Any]:
    """Run market analysis."""
    return await market_analyst.run(state)


async def node_product_scout(state: PipelineState) -> dict[str, Any]:
    """Search and evaluate products."""
    return await product_scout.run(state)


async def node_compliance(state: PipelineState) -> dict[str, Any]:
    """Run compliance checks."""
    return await compliance_agent.run(state)


async def node_copywriter(state: PipelineState) -> dict[str, Any]:
    """Generate marketing copy."""
    return await copywriter.run(state)


async def node_strategy(state: PipelineState) -> dict[str, Any]:
    """Generate strategy recommendations."""
    return await strategy_agent.run(state)


async def node_compiler(state: PipelineState) -> dict[str, Any]:
    """Compile all agent results into a structured output."""
    cards = []

    # Price comparison card
    price_data = state.get("price_comparison", {})
    if price_data:
        cards.append({
            "type": "price_compare",
            "title": "多平台比价",
            "data": price_data.get("data", {}),
        })

    # Product analysis card
    product_data = state.get("product_analysis", {})
    if product_data:
        cards.append({
            "type": "product_analysis",
            "title": "选品分析",
            "data": product_data.get("data", {}),
        })

    # Compliance card
    compliance_data = state.get("compliance_report", {})
    if compliance_data:
        cards.append({
            "type": "compliance",
            "title": "合规审核",
            "data": compliance_data.get("data", {}),
        })

    # Copywriting card
    copy_data = state.get("copywriting_output", {})
    if copy_data:
        cards.append({
            "type": "copywriting",
            "title": "AI 文案",
            "data": copy_data.get("data", {}),
        })

    # Strategy card
    strategy_data = state.get("strategy_output", {})
    if strategy_data:
        cards.append({
            "type": "strategy",
            "title": "运营策略",
            "data": strategy_data.get("data", {}),
        })

    # Compute totals
    trace = state.get("agent_trace", [])
    total_latency = sum(t.get("latency_ms", 0) for t in trace)
    total_tokens = sum(
        state.get(k, {}).get("tokens_used", 0)
        for k in ["market_analysis", "product_analysis", "compliance_report",
                   "copywriting_output", "strategy_output"]
    )

    return {
        "response_cards": cards,
        "summary": f"Pipeline completed: {len(cards)} cards generated, {len(trace)} agents executed.",
        "total_latency_ms": total_latency,
        "total_tokens": total_tokens,
    }


# ── Router function ─────────────────────────────────────

def route_after_intent(state: PipelineState) -> list[str]:
    """Determine which agents to activate based on parsed intent."""
    intent = state.get("intent", "product_search")
    targets = INTENT_ROUTES.get(intent, ["market_analyst", "product_scout"])

    # Always add compiler at the end
    return targets + ["compiler"]


# ── Graph construction ──────────────────────────────────

def build_graph() -> StateGraph:
    """Build and return the LangGraph StateGraph.

    The graph supports conditional routing: after intent parsing,
    only the relevant agents are activated (not all 6).
    """
    graph = StateGraph(PipelineState)

    # Add all nodes
    graph.add_node("intent_parser", node_intent_parser)
    graph.add_node("market_analyst", node_market_analyst)
    graph.add_node("product_scout", node_product_scout)
    graph.add_node("compliance", node_compliance)
    graph.add_node("copywriter", node_copywriter)
    graph.add_node("strategy", node_strategy)
    graph.add_node("compiler", node_compiler)

    # Entry point
    graph.set_entry_point("intent_parser")

    # Conditional routing after intent parsing
    graph.add_conditional_edges(
        "intent_parser",
        route_after_intent,
        {
            "market_analyst": "market_analyst",
            "product_scout": "product_scout",
            "compliance": "compliance",
            "copywriter": "copywriter",
            "strategy": "strategy",
            "compiler": "compiler",
        },
    )

    # All active agents feed into compiler
    for agent_name in ["market_analyst", "product_scout", "compliance",
                       "copywriter", "strategy"]:
        graph.add_edge(agent_name, "compiler")

    # Compiler is the end
    graph.add_edge("compiler", END)

    return graph


# ── Public API ──────────────────────────────────────────

def create_app():
    """Create a compiled LangGraph app ready for invocation."""
    graph = build_graph()
    return graph.compile()
