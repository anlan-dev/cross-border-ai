"""PipelineState with error tracking and decision chain support."""

from __future__ import annotations
from typing import Annotated, Any, TypedDict
from langgraph.graph import add_messages


class AgentResult(TypedDict, total=False):
    agent: str
    status: str
    data: dict[str, Any]
    latency_ms: int
    tokens_used: int
    decision: str


class PipelineState(TypedDict, total=False):
    query: str
    user_locale: str
    target_market: str
    intent: str
    intent_confidence: float
    entities: dict[str, Any]
    market_analysis: AgentResult
    product_analysis: AgentResult
    price_comparison: AgentResult
    logistics_info: AgentResult
    compliance_report: AgentResult
    copywriting_output: AgentResult
    strategy_output: AgentResult
    response_cards: list[dict[str, Any]]
    summary: str
    messages: Annotated[list, add_messages]
    agent_trace: list[dict[str, Any]]
    agent_errors: list[dict[str, Any]]
    total_tokens: int
    total_latency_ms: int
