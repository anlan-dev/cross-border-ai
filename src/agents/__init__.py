"""Agent definitions for the multi-agent system.

Each agent is a specialized LLM-powered node that:
1. Receives state from the LangGraph pipeline
2. Calls relevant tools via MCP
3. Produces structured output back to state
"""

from src.agents.intent_parser import IntentParserAgent
from src.agents.market_analyst import MarketAnalystAgent
from src.agents.product_scout import ProductScoutAgent
from src.agents.copywriter import CopywriterAgent
from src.agents.compliance import ComplianceAgent
from src.agents.strategy import StrategyAgent

__all__ = [
    "IntentParserAgent",
    "MarketAnalystAgent",
    "ProductScoutAgent",
    "CopywriterAgent",
    "ComplianceAgent",
    "StrategyAgent",
]
