# GlobalFUN Multi-Agent System

LangGraph + MCP Protocol 驱动的跨境电商多 Agent 系统。

## Architecture

```
User Query
    │
    ▼
┌─────────────┐
│ Intent Parser│  ← 意图识别 + 实体提取
└──────┬──────┘
       │  Conditional Routing
       ▼
┌──────────────────────────────────────┐
│  ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │ Market   │ │ Product  │ │Compli-│ │  ← 并行执行
│  │ Analyst  │ │ Scout    │ │ance   │ │
│  └────┬─────┘ └────┬─────┘ └───┬───┘ │
│       └─────────────┼───────────┘     │
│                     ▼                 │
│              ┌────────────┐           │
│              │  Compiler  │           │  ← 汇总输出
│              └────────────┘           │
└──────────────────────────────────────┘
```

## Agents

| Agent | Role | Icon | Tools Used |
|-------|------|------|------------|
| Intent Parser | 意图识别 | 🔍 | LLM + keyword fallback |
| Market Analyst | 市场调研 | 📊 | product_search, currency |
| Product Scout | 选品分析 | 🛍️ | price_compare, review_analyze |
| Compliance | 合规审核 | 🛡️ | compliance_check |
| Copywriter | 文案生成 | ✍️ | LLM generation |
| Strategy | 运营策略 | 📈 | LLM + market data |

## MCP Tools

| Tool | Description |
|------|-------------|
| `price_compare` | 多平台比价 |
| `product_search` | 商品搜索 |
| `logistics` | 物流 & 关税查询 |
| `compliance_check` | 合规校验 |
| `currency` | 实时汇率 |
| `review_analyze` | 评价分析 |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your API key

# 3. Run CLI demo
python examples/run_demo.py
python examples/run_demo.py "帮我比价SK-II神仙水"

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

## License

MIT
