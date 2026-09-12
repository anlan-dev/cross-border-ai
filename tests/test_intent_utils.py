# (c)2026 WangTianJiao anlan-dev | GPL-3.0 | 保留作者署名 attribution required
"""意图路由评测集 + LLM JSON 解析健壮性测试（零外部依赖，可重复运行）。

用法：
    python tests/test_intent_utils.py           # 打印评测报告
    python -m unittest tests.test_intent_utils  # 跑单元测试（assert）

评测对象：
    1. keyword_parse   —— 意图路由准确率（无 LLM 时的确定性 fallback，是基线）
    2. parse_llm_json  —— 结构化输出健壮性（markdown 代码块 / 夹带文字 / 非 JSON）
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.intent_utils import (  # noqa: E402
    INTENT_CATEGORIES,
    KEYWORDS_MAP,
    keyword_parse,
    parse_llm_json,
)

# ─────────────────────────────────────────────────────────────
# 意图路由评测集
#   category="明确"   → 期望 keyword fallback 正确分类（基线正确率）
#   category="边界"   → 暴露 keyword 短板（衡量优化空间，不作为基线失败）
# ─────────────────────────────────────────────────────────────
EVAL_CASES: list[tuple[str, str, str]] = [
    # —— 明确 case（覆盖全部 8 类意图）——
    ("帮我比价SK-II神仙水，看看哪个平台最便宜", "price_compare", "明确"),
    ("日本直邮到中国要多久？关税怎么算？", "logistics", "明确"),
    ("这款商品关税怎么算", "logistics", "明确"),
    ("推荐一些跨境好物", "product_search", "明确"),
    ("这款商品合规吗？能寄到中国吗？", "compliance", "明确"),
    ("成分表有没有违禁添加", "compliance", "明确"),
    ("帮我写一段推广文案", "copywriting", "明确"),
    ("给我一些运营策略建议", "strategy", "明确"),
    ("日元汇率是多少", "currency", "明确"),
    ("这款商品口碑怎么样", "review_analysis", "明确"),
    # —— 边界 case（暴露 keyword 弱点）——
    ("欧元兑换人民币", "currency", "边界"),        # KEYWORDS_MAP 缺「欧元/人民币/兑换」→ 预期误判
    ("帮我看看日本面膜", "product_search", "边界"),  # 「日本/面膜」无 keyword → 默认兜底，confidence 低
    ("这个贵不贵，值不值得买", "price_compare", "边界"),
    ("运费包邮吗", "logistics", "边界"),
]


def run_intent_eval() -> dict:
    """跑 keyword_parse 评测，返回结构化结果。"""
    rows = []
    clear_correct = clear_total = 0
    edge_correct = edge_total = 0

    for query, expected, category in EVAL_CASES:
        intent, confidence, entities = keyword_parse(query)
        ok = intent == expected
        rows.append({
            "query": query,
            "expected": expected,
            "actual": intent,
            "confidence": round(confidence, 2),
            "ok": ok,
            "category": category,
        })
        if category == "明确":
            clear_total += 1
            clear_correct += ok
        else:
            edge_total += 1
            edge_correct += ok

    return {
        "rows": rows,
        "clear_correct": clear_correct,
        "clear_total": clear_total,
        "clear_acc": round(clear_correct / clear_total, 3) if clear_total else 0,
        "edge_correct": edge_correct,
        "edge_total": edge_total,
        "edge_acc": round(edge_correct / edge_total, 3) if edge_total else 0,
    }


# ─────────────────────────────────────────────────────────────
# parse_llm_json 健壮性测试
# ─────────────────────────────────────────────────────────────
LLM_JSON_CASES = [
    # (输入, 期望意图, 说明)
    ('{"intent": "price_compare", "confidence": 0.9, "entities": {}}', "price_compare", "正常 JSON"),
    ('```json\n{"intent": "currency", "confidence": 0.8, "entities": {}}\n```', "currency", "markdown 代码块"),
    ('好的，结果如下：{"intent": "compliance", "confidence": 0.7, "entities": {}}', "compliance", "夹带前后文字"),
    ('{"intent": "logistics", "confidence": 0.6, "entities": {"product": "面膜"}}', "logistics", "带实体"),
    ("不是 JSON 的输出", None, "非 JSON → None"),
    (None, None, "None 输入"),
    ([{"intent": "x"}], None, "list 输入 → None"),
]


def run_json_eval() -> list[dict]:
    rows = []
    for content, expected_intent, note in LLM_JSON_CASES:
        parsed = parse_llm_json(content)
        actual = parsed.get("intent") if parsed else None
        ok = actual == expected_intent
        rows.append({"note": note, "ok": ok, "actual": actual})
    return rows


# ─────────────────────────────────────────────────────────────
# 报告输出
# ─────────────────────────────────────────────────────────────
def print_report():
    eval_res = run_intent_eval()
    json_rows = run_json_eval()

    print("\n" + "=" * 70)
    print("跨境电商 Agent · 意图路由基线评测（keyword fallback，零 LLM 依赖）")
    print("=" * 70)

    print(f"\n意图类别：{len(INTENT_CATEGORIES)} 类 | 关键词映射：{sum(len(v) for v in KEYWORDS_MAP.values())} 条")
    print(f"评测集：{len(EVAL_CASES)} 条（明确 {eval_res['clear_total']} / 边界 {eval_res['edge_total']}）\n")

    for r in eval_res["rows"]:
        mark = "✓" if r["ok"] else "✗"
        flag = "" if r["category"] == "明确" else "  [边界]"
        print(f"  {mark} {r['query']:<30} 期望={r['expected']:<15} 实际={r['actual']:<15} conf={r['confidence']}{flag}")

    print(f"\n── 结果 ──")
    print(f"  明确 case 准确率：{eval_res['clear_correct']}/{eval_res['clear_total']} = {eval_res['clear_acc']:.1%}")
    print(f"  边界 case 命中率：{eval_res['edge_correct']}/{eval_res['edge_total']} = {eval_res['edge_acc']:.1%}  ← 优化空间所在")

    print(f"\n── parse_llm_json 健壮性 ──")
    for r in json_rows:
        mark = "✓" if r["ok"] else "✗"
        print(f"  {mark} {r['note']:<20} → {r['actual']}")

    total_json_ok = sum(1 for r in json_rows if r["ok"])
    print(f"\n  JSON 解析通过：{total_json_ok}/{len(json_rows)}")

    # 边界 case 的失败项（= 明确的优化线索）
    failed_edge = [r for r in eval_res["rows"] if r["category"] == "边界" and not r["ok"]]
    if failed_edge:
        print(f"\n── 暴露的 keyword 弱点（优化线索）──")
        for r in failed_edge:
            print(f"  · 「{r['query']}」期望 {r['expected']}，实际 {r['actual']}")

    print()


if __name__ == "__main__":
    print_report()
