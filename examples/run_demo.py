"""CLI demo — run the multi-agent pipeline from the command line.

Usage:
    python examples/run_demo.py
    python examples/run_demo.py "帮我比价SK-II神仙水"
    python examples/run_demo.py "日本直邮要多久？关税怎么算？"
"""

from __future__ import annotations

import asyncio
import json
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text

console = Console()

DEMO_QUERIES = [
    "帮我比价SK-II神仙水，看看哪个平台最便宜",
    "日本直邮到中国要多久？关税怎么算？",
    "推荐一些跨境好物",
    "这款商品合规吗？能寄到中国吗？",
    "帮我写一段推广文案",
    "给我一些运营策略建议",
]


async def run_pipeline(query: str) -> dict:
    """Run the full agent pipeline and return results."""
    from src.graph.workflow import create_app

    app = create_app()

    # Stream execution with live display
    console.print(f"\n[bold cyan]━━━ 用户查询 ━━━[/bold cyan]")
    console.print(f"  [white]{query}[/white]\n")

    initial_state = {
        "query": query,
        "user_locale": "zh-CN",
        "target_market": "CN",
        "agent_trace": [],
    }

    # Execute pipeline
    console.print("[dim]⏳ Pipeline executing...[/dim]\n")
    result = await app.ainvoke(initial_state)
    return result


def display_results(result: dict) -> None:
    """Pretty-print the pipeline results."""
    # ── Agent Trace ──
    trace = result.get("agent_trace", [])
    if trace:
        table = Table(title="Agent Execution Trace", show_lines=True)
        table.add_column("Agent", style="cyan", width=15)
        table.add_column("Status", style="green", width=10)
        table.add_column("Latency", style="yellow", width=10)
        for t in trace:
            table.add_row(
                t.get("agent", "?"),
                t.get("status", "?"),
                f"{t.get('latency_ms', 0)}ms",
            )
        console.print(table)

    # ── Intent ──
    intent = result.get("intent", "?")
    confidence = result.get("intent_confidence", 0)
    console.print(f"\n[bold]Intent:[/bold] {intent} (confidence: {confidence:.0%})")

    # ── Response Cards ──
    cards = result.get("response_cards", [])
    for card in cards:
        card_type = card.get("type", "?")
        title = card.get("title", "?")
        data = card.get("data", {})

        console.print(f"\n[bold cyan]━━━ {title} ━━━[/bold cyan]")

        if card_type == "price_compare":
            prices = data.get("prices", [])
            for p in prices:
                marker = "🏆" if p.get("platform") == data.get("lowest_platform") else "  "
                console.print(f"  {marker} {p.get('icon', '')} {p.get('platform', '')}: ¥{p.get('price', 0):.2f}")
            console.print(f"\n  [green]最低价: ¥{data.get('lowest_price', 0):.2f} ({data.get('lowest_platform', '')})[/green]")

        elif card_type == "compliance":
            checks = data.get("checks", [])
            for c in checks:
                console.print(f"  {c.get('icon', '')} {c.get('label', '')} — {c.get('regulation', '')}")
            status = "✅ 全部通过" if data.get("overall_pass") else "❌ 未通过"
            console.print(f"\n  [bold]{status}[/bold]")

        elif card_type == "copywriting":
            console.print(f"  📝 标题: {data.get('title', '')}")
            console.print(f"  📱 种草: {data.get('social_copy', '')}")
            subjects = data.get("email_subjects", [])
            for i, s in enumerate(subjects):
                console.print(f"  📧 {'AB'[i]}: {s}")

        elif card_type == "strategy":
            insights = data.get("market_insights", [])
            if insights:
                console.print("  [bold]市场洞察:[/bold]")
                for ins in insights:
                    console.print(f"    • {ins.get('metric', '')}: {ins.get('value', '')} — {ins.get('insight', '')}")
            strategies = data.get("strategies", [])
            if strategies:
                console.print("  [bold]推荐策略:[/bold]")
                for s in strategies:
                    console.print(f"    {s.get('priority', '')}. {s.get('action', '')} (ROI: {s.get('expected_roi', '')})")

        elif card_type == "product_analysis":
            console.print(f"  🛍️ 商品: {data.get('product', '')}")
            console.print(f"  💰 最低价: ¥{data.get('lowest_price', 0):.2f} ({data.get('lowest_platform', '')})")
            console.print(f"  ⭐ 好评率: {data.get('review_score', 0)}%")
            console.print(f"  📊 推荐: {data.get('recommendation', '')}")

    # ── Summary ──
    console.print(f"\n[dim]Total latency: {result.get('total_latency_ms', 0)}ms | "
                   f"Tokens: {result.get('total_tokens', 0)} | "
                   f"Agents: {len(trace)}[/dim]")


async def main():
    """Main entry point."""
    console.print(Panel.fit(
        "[bold]GlobalFUN Multi-Agent System[/bold]\n"
        "[dim]LangGraph + MCP Protocol · Cross-Border E-Commerce[/dim]",
        border_style="cyan",
    ))

    # Get query from CLI args or use default
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
    else:
        console.print("\n[bold]Demo queries:[/bold]")
        for i, q in enumerate(DEMO_QUERIES, 1):
            console.print(f"  [cyan]{i}.[/cyan] {q}")
        console.print(f"\n[dim]Using default: {DEMO_QUERIES[0]}[/dim]")
        query = DEMO_QUERIES[0]

    result = await run_pipeline(query)
    display_results(result)


if __name__ == "__main__":
    asyncio.run(main())
