"""MCP (Model Context Protocol) implementation.

This module implements a lightweight MCP-compatible protocol for
tool discovery, invocation, and result formatting.
"""

from src.mcp.protocol import MCPMessage, MCPToolSpec
from src.mcp.router import MCPRouter

__all__ = ["MCPMessage", "MCPToolSpec", "MCPRouter"]
