"""Shared state definition for the multi-agent workflow.

This module defines the TypedDict that flows through every node in the
LangGraph graph.  Each agent reads from and writes to this state, enabling
loose coupling between agents while maintaining a single source of truth.
"""

from __future__ import annotations

from typing import Annotated, Any, TypedDict

from langgraph.graph import add_messages


class AgentResult(TypedDict, total=False):
    """Structured output from a single agent."""
    agent: str
    status: str          # "success" | "error" | "skipped"
    data: dict[str, Any]
    latency_ms: int
    tokens_used: int


class PipelineState(TypedDict, total=False):
    """The global state that flows through the LangGraph pipeline.

    Fields are grouped by lifecycle stage:
    - Input: raw user query and parsed intent
    - Processing: intermediate results from each agent
    - Output: final structured response
    - Meta: observability and debugging
    """

    # ── Input ──────────────────────────────────────────────
    query: str
    user_locale: str                   # e.g. "zh-CN", "en-US"
    target_market: str                 # e.g. "CN", "US", "EU"

    # ── Intent Parsing ─────────────────────────────────────
    intent: str                        # "price_compare" | "logistics" | "compliance" | ...
    intent_confidence: float
    entities: dict[str, Any]           # extracted product name, category, etc.

    # ── Agent Results ──────────────────────────────────────
    market_analysis: AgentResult
    product_analysis: AgentResult
    price_comparison: AgentResult
    logistics_info: AgentResult
    compliance_report: AgentResult
    copywriting_output: AgentResult
    strategy_output: AgentResult

    # ── Final Output ───────────────────────────────────────
    response_cards: list[dict[str, Any]]   # structured cards for UI rendering
    summary: str                           # human-readable summary

    # ── Observability ──────────────────────────────────────
    messages: Annotated[list, add_messages]
    agent_trace: list[dict[str, Any]]      # ordered execution trace
    total_tokens: int
    total_latency_ms: int
