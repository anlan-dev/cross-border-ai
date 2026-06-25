"""MCP-compatible tools for the agent system.

Each tool follows the MCP (Model Context Protocol) pattern:
- Declares a name, description, and input schema
- Implements an `execute` method that returns structured data
- Can be called by any agent through the orchestrator
"""

from src.tools.price_compare import PriceCompareTool
from src.tools.product_search import ProductSearchTool
from src.tools.logistics import LogisticsTool
from src.tools.compliance_check import ComplianceCheckTool
from src.tools.currency import CurrencyTool
from src.tools.review_analyze import ReviewAnalyzeTool

__all__ = [
    "PriceCompareTool",
    "ProductSearchTool",
    "LogisticsTool",
    "ComplianceCheckTool",
    "CurrencyTool",
    "ReviewAnalyzeTool",
]
