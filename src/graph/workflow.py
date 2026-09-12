# (c)2026 WangTianJiao anlan-dev | GPL-3.0 | 保留作者署名 attribution required
"""LangGraph workflow v2 — true parallel agents + MCP + error recovery + decision chains."""

from __future__ import annotations
import time
from typing import Any
from langgraph.graph import END, StateGraph, Send
from src.graph.state import PipelineState
from src.mcp.router import MCPRouter
from src.agents.intent_parser import IntentParserAgent
from src.data.scenarios import ScenarioStore

mcp_router = MCPRouter()
intent_parser = IntentParserAgent()
_agent_cache = {}

def _get_agent(name: str):
    if name not in _agent_cache:
        if name == "market_analyst":
            from src.agents.market_analyst import MarketAnalystAgent
            _agent_cache[name] = MarketAnalystAgent(mcp=mcp_router)
        elif name == "product_scout":
            from src.agents.product_scout import ProductScoutAgent
            _agent_cache[name] = ProductScoutAgent(mcp=mcp_router)
        elif name == "compliance":
            from src.agents.compliance import ComplianceAgent
            _agent_cache[name] = ComplianceAgent(mcp=mcp_router)
        elif name == "copywriter":
            from src.agents.copywriter import CopywriterAgent
            _agent_cache[name] = CopywriterAgent()
        elif name == "strategy":
            from src.agents.strategy import StrategyAgent
            _agent_cache[name] = StrategyAgent()
    return _agent_cache[name]

INTENT_ROUTES = {
    "price_compare": ["market_analyst", "product_scout"],
    "product_search": ["market_analyst", "product_scout"],
    "logistics": ["market_analyst", "compliance"],
    "compliance": ["compliance"],
    "review_analysis": ["product_scout"],
    "copywriting": ["product_scout", "copywriter"],
    "strategy": ["market_analyst", "product_scout", "compliance", "strategy"],
    "currency": ["market_analyst"],
}

async def _run_agent_safe(agent_name: str, state: dict) -> dict:
    try:
        agent = _get_agent(agent_name)
        return await agent.run(state)
    except Exception as e:
        trace_entry = {"agent": agent_name, "latency_ms": 0, "status": "error", "error": str(e)}
        trace = state.get("agent_trace", []) + [trace_entry]
        return {"agent_trace": trace, "agent_errors": state.get("agent_errors", []) + [trace_entry]}

async def node_intent_parser(state): return await intent_parser.run(state)
async def node_market_analyst(state): return await _run_agent_safe("market_analyst", state)
async def node_product_scout(state): return await _run_agent_safe("product_scout", state)
async def node_compliance(state): return await _run_agent_safe("compliance", state)
async def node_copywriter(state): return await _run_agent_safe("copywriter", state)
async def node_strategy(state): return await _run_agent_safe("strategy", state)

async def node_compiler(state: PipelineState) -> dict[str, Any]:
    cards = []
    def _add_card(ct, title, sk):
        d = state.get(sk, {})
        if d and d.get("status") != "error":
            cards.append({"type": ct, "title": title, "data": d.get("data", {}), "decision": d.get("decision", "")})

    _add_card("price_compare", "多平台比价", "price_comparison")
    _add_card("product_analysis", "选品分析", "product_analysis")
    _add_card("compliance", "合规审核", "compliance_report")
    _add_card("copywriting", "AI 文案", "copywriting_output")
    _add_card("strategy", "运营策略", "strategy_output")

    scenario = ScenarioStore.find(state.get("query", ""))
    decision_summary = ""
    if scenario and "decision_chain" in scenario:
        dc = scenario["decision_chain"]
        decision_summary = f"比价: {dc.get('price', '')} | 关税: {dc.get('tariff', '')} | 合规: {dc.get('compliance', '')}"
        cards.append({"type": "decision_chain", "title": "PM 决策链", "data": {"steps": [
            {"label": "比价", "detail": dc.get("price", "")},
            {"label": "关税", "detail": dc.get("tariff", "")},
            {"label": "合规", "detail": dc.get("compliance", "")},
            {"label": "综合建议", "detail": dc.get("recommendation", "")},
        ]}})

    trace = state.get("agent_trace", [])
    errors = state.get("agent_errors", [])
    total_latency = sum(t.get("latency_ms", 0) for t in trace)
    total_tokens = sum(state.get(k, {}).get("tokens_used", 0) for k in [
        "market_analysis", "product_analysis", "compliance_report", "copywriting_output", "strategy_output"])
    status = "partial" if errors else "success"

    # 结构化可观测性指标（供评测对比：延迟 / 错误 / LLM 命中率 / 每 Agent 明细）
    llm_hits = sum(1 for t in trace if t.get("llm_status") == "llm")
    metrics = {
        "status": status,
        "total_agents": len(trace),
        "success_agents": len(trace) - len(errors),
        "error_agents": len(errors),
        "total_latency_ms": total_latency,
        "total_tokens": total_tokens,
        "llm_hit_count": llm_hits,
        "llm_hit_rate": round(llm_hits / len(trace), 3) if trace else 0,
        "per_agent_latency_ms": {t.get("agent"): t.get("latency_ms", 0) for t in trace},
    }

    return {"response_cards": cards,
            "summary": decision_summary or f"Pipeline {status}: {len(cards)} cards, {len(trace)} agents, {len(errors)} errors.",
            "total_latency_ms": total_latency, "total_tokens": total_tokens,
            "metrics": metrics}

def route_after_intent(state: PipelineState):
    intent = state.get("intent", "product_search")
    targets = INTENT_ROUTES.get(intent, ["market_analyst", "product_scout"])
    return [Send(target, state) for target in targets]

def build_graph() -> StateGraph:
    graph = StateGraph(PipelineState)
    nodes = {"intent_parser": node_intent_parser, "market_analyst": node_market_analyst,
             "product_scout": node_product_scout, "compliance": node_compliance,
             "copywriter": node_copywriter, "strategy": node_strategy, "compiler": node_compiler}
    for name, fn in nodes.items():
        graph.add_node(name, fn)
    graph.set_entry_point("intent_parser")
    graph.add_conditional_edges("intent_parser", route_after_intent,
        {t: t for t in ["market_analyst", "product_scout", "compliance", "copywriter", "strategy"]})
    for name in ["market_analyst", "product_scout", "compliance", "copywriter", "strategy"]:
        graph.add_edge(name, "compiler")
    graph.add_edge("compiler", END)
    return graph

def create_app():
    return build_graph().compile()
