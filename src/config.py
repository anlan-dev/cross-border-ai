"""Global configuration with real API and scene mode support."""

from __future__ import annotations
import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class LLMConfig:
    api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    base_url: str = field(default_factory=lambda: os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
    model: str = field(default_factory=lambda: os.getenv("MODEL_NAME", "gpt-4o-mini"))
    temperature: float = 0.3
    max_tokens: int = 2048


@dataclass(frozen=True)
class AgentConfig:
    max_parallel_agents: int = 6
    tool_timeout_seconds: int = 30
    max_retries: int = 2
    use_real_api: bool = field(default_factory=lambda: os.getenv("USE_REAL_API", "false").lower() == "true")
    exchangerate_api_key: str = field(default_factory=lambda: os.getenv("EXCHANGERATE_API_KEY", ""))
    scene_mode: bool = True


@dataclass(frozen=True)
class Settings:
    llm: LLMConfig = field(default_factory=LLMConfig)
    agent: AgentConfig = field(default_factory=AgentConfig)


settings = Settings()

# Centralized agent output key mapping
AGENT_OUTPUT_KEYS = {
    "intent_parser": "intent_parser",
    "market_analyst": "market_analysis",
    "product_scout": "product_analysis",
    "compliance": "compliance_report",
    "copywriter": "copywriting_output",
    "strategy": "strategy_output",
    "compiler": "compiler",
}
