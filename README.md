# GlobalFUN — Cross-Border E-Commerce Multi-Agent System

A LangGraph + MCP Protocol powered multi-agent system for cross-border e-commerce operations.

## Overview

GlobalFUN is an AI-powered platform that automates the full lifecycle of cross-border e-commerce — from demand analysis and market research to product selection, content generation, compliance checking, and operations strategy. Unlike traditional chatbots, it uses a **6-agent collaboration architecture** with structured card-based output.

## Architecture

```
User Query
    │
    ▼
┌─────────────┐
│ Intent Parser│  ← Intent classification + Entity extraction
└──────┬──────┘
       │  Conditional Routing
       ▼
┌──────────────────────────────────────┐
│  ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │ Market   │ │ Product  │ │Compli-│ │  ← Parallel execution
│  │ Analyst  │ │ Scout    │ │ance   │ │
│  └────┬─────┘ └────┬─────┘ └───┬───┘ │
│       └─────────────┼───────────┘     │
│                     ▼                 │
│  ┌──────────┐ ┌──────────┐           │
│  │Copywriter│ │ Strategy │           │  ← Content & Strategy
│  └────┬─────┘ └────┬─────┘           │
│       └─────────────┼───────────┘     │
│                     ▼                 │
│              ┌────────────┐           │
│              │  Compiler  │           │  ← Structured output
│              └────────────┘           │
└──────────────────────────────────────┘
```

## Agents

| Agent | Role | Icon | Tools Used |
|-------|------|------|------------|
| Intent Parser | Intent Recognition | 🔍 | LLM + keyword fallback |
| Market Analyst | Market Research | 📊 | product_search, currency |
| Product Scout | Product Selection | 🛍️ | price_compare, review_analyze |
| Compliance | Regulatory Check | 🛡️ | compliance_check |
| Copywriter | Content Generation | ✍️ | LLM generation |
| Strategy | Operations Strategy | 📈 | LLM + market data |

## MCP Tools

| Tool | Description |
|------|-------------|
| `price_compare` | Multi-platform price comparison |
| `product_search` | Product search & discovery |
| `logistics` | Logistics & tariff calculation |
| `compliance_check` | Regulatory compliance verification |
| `currency` | Real-time currency conversion |
| `review_analyze` | Product review analysis |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your API key

# 3. Run CLI demo
python examples/run_demo.py
python examples/run_demo.py "Compare SK-II prices across platforms"

# 4. Run tests
python -m pytest tests/ -v
```

## Project Structure

```
cross-border-ai-agent/
├── src/
│   ├── config.py              # Global settings
│   ├── agents/                # 6 specialized agents
│   │   ├── intent_parser.py   # Intent classification
│   │   ├── market_analyst.py  # Market research
│   │   ├── product_scout.py   # Product evaluation
│   │   ├── copywriter.py      # Content generation
│   │   ├── compliance.py      # Regulatory checks
│   │   └── strategy.py        # Operations strategy
│   ├── tools/                 # MCP-compatible tools
│   │   ├── price_compare.py
│   │   ├── product_search.py
│   │   ├── logistics.py
│   │   ├── compliance_check.py
│   │   ├── currency.py
│   │   └── review_analyze.py
│   ├── graph/                 # LangGraph workflow
│   │   ├── state.py           # Shared state definition
│   │   └── workflow.py        # Graph construction
│   └── mcp/                   # MCP protocol layer
│       ├── protocol.py        # Message types
│       └── router.py          # Tool routing
├── tests/
│   └── test_pipeline.py
├── examples/
│   └── run_demo.py            # CLI demo
└── demo/
    └── work/
        └── cross-border-ai.html  # Interactive web demo
```

## Key Design Decisions

1. **LangGraph over LangChain chains** — StateGraph enables conditional routing and parallel execution, which is critical for multi-agent systems.

2. **MCP Protocol** — Tools are decoupled from agents via a protocol layer. Any agent can call any tool through the router, making the system extensible.

3. **Keyword fallback** — Intent parsing has a keyword-based fallback when LLM is unavailable, ensuring the system works offline.

4. **Structured state** — `PipelineState` TypedDict provides type safety and clear data flow between agents.

5. **Structured card output** — Results are delivered as structured cards (price comparison, compliance report, copywriting, strategy) rather than plain text.

## Tech Stack

- **LangGraph** — Multi-agent orchestration
- **MCP Protocol** — Tool abstraction layer
- **Python 3.11+** — Runtime
- **FastAPI** — API server
- **React + TypeScript** — Frontend UI

## License

GNU General Public License v3.0（保留作者署名权）

见 [LICENSE](./LICENSE)。
