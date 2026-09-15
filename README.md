# GlobalFUN — Cross-Border E-Commerce Multi-Agent System

> © 2026 王天娇（anlan-dev）· GPL-3.0 开源 · 使用时保留作者署名与版权声明 / keep attribution


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

## Known Limitations（2026-09 现状）

**当前是架构 Demo，不是可上线系统。** 公开这一节是为了让能力边界可核对：

| 部分 | 状态 |
|---|---|
| 意图路由 / 结构化输出解析 | **真实可复现**：`python tests/test_intent_utils.py`（明确 10/10、边界 4/4、JSON 容错 7/7；样本 14 条，自建集，非第三方基准） |
| LangGraph DAG 编排 + MCP 工具路由 | 真实实现（`src/graph/`、`src/mcp/`） |
| 商品 / 价格 / 评价 / 物流数据 | **模拟数据**：`price_compare.py`、`product_search.py` 用随机数与静态数组生成（文件内已标注 `Mock data`），`src/data/scenarios.py` 为 3 个固定场景 |
| 多平台真实数据接入 | **未实现** |
| 向量检索 | **未实现**（当前场景规模不需要，见下） |
| 支付 / 结算、真实用户数据 | **未实现** |

### 为什么不接真实平台数据

「接入四个平台」是需求描述，不是方案。四条路径差异很大：**官方开放平台 API**（天猫/京东开放平台、Amazon SP-API）合规稳定，但价格类字段多数不对外开放、需商家资质；**第三方数据服务商采买**按调用量付费，海外覆盖弱；**联盟 / CPS 接口**合规但只覆盖联盟内商品；**爬虫**违反平台 ToS、反爬成本高，已划为红线。

**取舍**：v1 不承诺接入四个平台，只接一个有官方授权的源把「到手价」算准，其余用可降级占位数据并明确标注。

### 高频商品为什么不"全量重新向量化"

价格/库存/销量是高频结构化字段，应走 KV + 精确查询；向量库只放低频语义字段（标题、卖点、类目、评论摘要），并用 `content_hash + updated_at` 做增量变更检测，hash 未变则复用旧向量。当前 Demo 只有 3 个固定场景，技术上用不着向量库，因此未引入。

### 为什么没有 agent loop

任务边界收敛（8 类意图、固定编排）时，DAG 更合适：可测、延迟可控、Token 成本可预算。只有开放式的多轮工具试错才需要 loop；loop 留作 v2 的显式开关，不做默认。

## Tech Stack

- **LangGraph** — Multi-agent orchestration
- **MCP Protocol** — Tool abstraction layer
- **Python 3.11+** — Runtime
- **FastAPI** — API server
- **React + TypeScript** — Frontend UI

## License

GNU General Public License v3.0（保留作者署名权）

见 [LICENSE](./LICENSE)。
