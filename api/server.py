# (c)2026 WangTianJiao anlan-dev | GPL-3.0 | 保留作者署名 attribution required
"""FastAPI server v2 — centralized key mapping + decision chain streaming."""

from __future__ import annotations
import asyncio, json, os, sys
from typing import Any
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.graph.workflow import create_app
from src.config import AGENT_OUTPUT_KEYS
from api.api_keys import router as api_keys_router

app = FastAPI(title="GlobalFUN Multi-Agent API v2", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_keys_router)

class QueryRequest(BaseModel):
    query: str; user_locale: str = "zh-CN"; target_market: str = "CN"

DEMO_QUERIES = [
    {"id": "price_compare", "query": "帮我比价SK-II神仙水", "icon": "💰", "category": "比价"},
    {"id": "logistics", "query": "日本直邮到中国要多久？关税怎么算？", "icon": "🚢", "category": "物流"},
    {"id": "product_search", "query": "推荐一些跨境好物", "icon": "🛍️", "category": "选品"},
    {"id": "compliance", "query": "面膜合规吗？能寄到中国吗？", "icon": "🛡️", "category": "合规"},
    {"id": "copywriting", "query": "帮我写一段推广文案", "icon": "✍️", "category": "文案"},
    {"id": "strategy", "query": "给我一些运营策略建议", "icon": "📈", "category": "策略"},
]

AGENT_META = {
    "intent_parser": {"role": "需求解析", "icon": "🔍"},
    "market_analyst": {"role": "市场调研", "icon": "📊"},
    "product_scout": {"role": "选品分析", "icon": "🛍️"},
    "compliance": {"role": "合规审核", "icon": "🛡️"},
    "copywriter": {"role": "文案生成", "icon": "✍️"},
    "strategy": {"role": "运营策略", "icon": "📈"},
    "compiler": {"role": "结果汇总", "icon": "📋"},
}

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "GlobalFUN v2", "features": ["true-parallel", "mcp-integration", "decision-chain", "scene-mode"]}

@app.get("/api/demo-queries")
async def get_demo_queries():
    return {"queries": DEMO_QUERIES}

@app.post("/api/query")
async def run_query(req: QueryRequest):
    pipeline = create_app()
    initial = {"query": req.query, "user_locale": req.user_locale, "target_market": req.target_market, "agent_trace": [], "agent_errors": []}
    return await pipeline.ainvoke(initial)

@app.websocket("/ws/query")
async def ws_query(ws: WebSocket):
    await ws.accept()
    try:
        data = await ws.receive_json()
        query = data.get("query", "")
        initial = {"query": query, "user_locale": data.get("user_locale", "zh-CN"),
                   "target_market": data.get("target_market", "CN"), "agent_trace": [], "agent_errors": []}
        await ws.send_json({"type": "start", "query": query})
        pipeline = create_app()
        async for event in pipeline.astream(initial):
            for node_name, node_output in event.items():
                meta = AGENT_META.get(node_name, {"role": node_name, "icon": "⚙️"})
                if node_name == "intent_parser":
                    await ws.send_json({"type": "agent_start", "agent": node_name, **meta})
                    await asyncio.sleep(0.1)
                    trace = node_output.get("agent_trace", [])
                    lat = trace[0].get("latency_ms", 0) if trace else 0
                    await ws.send_json({"type": "agent_done", "agent": node_name, **meta, "latency_ms": lat, "status": "success",
                        "output": {"intent": node_output.get("intent"), "confidence": node_output.get("intent_confidence"), "entities": node_output.get("entities")}})
                elif node_name == "compiler":
                    for card in node_output.get("response_cards", []):
                        await ws.send_json({"type": "card", "card": card})
                    await ws.send_json({"type": "summary", "summary": node_output.get("summary", ""),
                        "total_latency_ms": node_output.get("total_latency_ms", 0), "total_tokens": node_output.get("total_tokens", 0)})
                else:
                    await ws.send_json({"type": "agent_start", "agent": node_name, **meta})
                    await asyncio.sleep(0.05)
                    out_key = AGENT_OUTPUT_KEYS.get(node_name, node_name)
                    ar = node_output.get(out_key, {})
                    lat = ar.get("latency_ms", 0) if isinstance(ar, dict) else 0
                    dec = ar.get("decision", "") if isinstance(ar, dict) else ""
                    await ws.send_json({"type": "agent_done", "agent": node_name, **meta, "latency_ms": lat, "status": "success", "decision": dec})
        await ws.send_json({"type": "done", "result": {"summary": "Pipeline completed."}})
    except WebSocketDisconnect: pass
    except Exception as e: await ws.send_json({"type": "error", "message": str(e)})
    finally:
        try: await ws.close()
        except: pass

if __name__ == "__main__":
    import uvicorn; uvicorn.run(app, host="0.0.0.0", port=8000)
