"""Global configuration for the agent system."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class LLMConfig:
    """LLM provider settings."""
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    model: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "gpt-4o-mini"))
    temperature: float = 0.3
    max_tokens: int = 2048


@dataclass(frozen=True)
class AgentConfig:
    """Agent system settings."""
    max_parallel_agents: int = 3
    tool_timeout_seconds: int = 30
    max_retries: int = 2


@dataclass(frozen=True)
class Settings:
    """Top-level settings container."""
    llm: LLMConfig = field(default_factory=LLMConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)


settings = Settings()
