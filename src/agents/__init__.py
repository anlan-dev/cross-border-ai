"""Agent definitions for the multi-agent system.

Each agent is a specialized LLM-powered node that:
1. Receives state from the LangGraph pipeline
2. Calls relevant tools via MCP
3. Produces structured output back to state
"""

__all__ = [
    "IntentParserAgent",
    "MarketAnalystAgent",
    "ProductScoutAgent",
    "CopywriterAgent",
    "ComplianceAgent",
    "StrategyAgent",
]

# 懒加载映射：仅在显式访问时 import，避免「无 langchain 环境」下
# import src.agents.intent_utils 这类纯函数子模块也被 intent_parser 的 langchain 依赖拖垮。
_AGENT_MODULES = {
    "IntentParserAgent": "src.agents.intent_parser",
    "MarketAnalystAgent": "src.agents.market_analyst",
    "ProductScoutAgent": "src.agents.product_scout",
    "CopywriterAgent": "src.agents.copywriter",
    "ComplianceAgent": "src.agents.compliance",
    "StrategyAgent": "src.agents.strategy",
}


def __getattr__(name: str):
    """PEP 562 懒加载：`from src.agents import X` 时才真正 import 对应模块。"""
    if name in _AGENT_MODULES:
        import importlib

        module = importlib.import_module(_AGENT_MODULES[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
