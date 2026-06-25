"""MCP Protocol message types and tool specifications.

Implements the core MCP message format used for agent ↔ tool communication.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MCPToolSpec:
    """Describes a tool available via MCP.

    This mirrors the MCP tool specification format, making tools
    discoverable and invocable by any agent in the system.
    """
    name: str
    description: str
    input_schema: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema,
        }


@dataclass
class MCPMessage:
    """A message in the MCP protocol.

    Used for communication between orchestrator and tools.
    Each message has a unique ID, a method (like JSON-RPC),
    and optional params/result.
    """
    method: str                           # "tools/list", "tools/call", etc.
    params: dict[str, Any] = field(default_factory=dict)
    result: Any = None
    error: str | None = None
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])

    def to_dict(self) -> dict[str, Any]:
        msg = {"jsonrpc": "2.0", "method": self.method, "id": self.id}
        if self.params:
            msg["params"] = self.params
        if self.result is not None:
            msg["result"] = self.result
        if self.error:
            msg["error"] = self.error
        return msg

    @classmethod
    def tool_call(cls, tool_name: str, arguments: dict[str, Any]) -> MCPMessage:
        """Create a tool invocation message."""
        return cls(
            method="tools/call",
            params={"name": tool_name, "arguments": arguments},
        )

    @classmethod
    def tool_list(cls) -> MCPMessage:
        """Create a tool discovery message."""
        return cls(method="tools/list")

    def success(self, result: Any) -> MCPMessage:
        """Create a success response to this message."""
        return MCPMessage(method=self.method, id=self.id, result=result)

    def fail(self, error: str) -> MCPMessage:
        """Create an error response to this message."""
        return MCPMessage(method=self.method, id=self.id, error=error)
