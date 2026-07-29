"""Scene-based mock data — each scenario has a complete "storyline".

Design principle: every scenario answers "what happened → what I decided → what the result was",
mirroring the PM decision-chain narrative used throughout the portfolio.
"""

from __future__ import annotations
from typing import Any

SCENARIOS: dict[str, dict[str, Any]] = {
    "japanese_snack": {
        "id": "japanese_snack",
        "query_hint": "帮我比价白色恋人饼干",
        "product": {"name": "白色恋人 18枚装", "category": "食品", "origin": "日本北海道", "weight": "360g"},
        "prices": {"tmall": 128, "jd": 135, "kaola": 118, "amazon_jp": 980},
        "reviews": {
            "positive_rate": 96, "total_reviews": 12860,
            "positive_keywords": ["入口即化", "送礼体面", "保质期长", "正品"],
            "negative_keywords": ["夏天容易化", "包装有压痕"],
            "samples": [
                {"rating": 5, "lang": "zh", "text": "和在日本买的一模一样，送朋友特别有面子"},
                {"rating": 4, "lang": "ja", "text": "お土産に喜ばれました。でも少し高め"},
            ],
        },
        "logistics": {"days": "5-7", "freight": 25, "free_threshold": 199, "carrier": "EMS/国际小包"},
        "tariff": {"rate": "10%", "category": "食品类", "note": "个人自用5000元以下免税"},
        "compliance": {
            "checks": [
                {"id": "ingredients", "label": "成分合规", "status": "pass", "detail": "小麦粉/黄油/砂糖，无违禁添加"},
                {"id": "labeling", "label": "中文标签", "status": "pass", "detail": "已加贴中文背标"},
                {"id": "shelf_life", "label": "保质期", "status": "warning", "detail": "剩余>6个月，建议前端提示消费者"},
                {"id": "filing", "label": "进口备案", "status": "pass", "detail": "已完成进口食品备案"},
            ],
            "overall_pass": True,
            "applicable_markets": ["中国大陆", "香港", "台湾"],
        },
        "decision_chain": {
            "price": "对比4平台，考拉最低¥118（低于均价15%），建议拼团渠道选考拉",
            "tariff": "食品关税10%，单品¥128→关税¥12.8，拼团10件可摊薄单件成本",
            "compliance": "4项全部通过，仅保质期需前端提示",
            "recommendation": "高毛利+高频复购，适合批量拼团，建议首单50件起"
        },
        "i18n": {
            "en": {"product_name": "Shiroi Koibito 18-piece", "category": "Food", "origin": "Hokkaido, Japan"},
            "ja": {"product_name": "白い恋人 18枚入り", "category": "食品", "origin": "日本・北海道"},
        },
    },
    "korean_cosmetics": {
        "id": "korean_cosmetics",
        "query_hint": "帮我看看韩国面膜的合规情况",
        "product": {"name": "MEDIHEAL 面膜 10片装", "category": "美妆", "origin": "韩国", "weight": "250g"},
        "prices": {"tmall": 89, "jd": 95, "kaola": 78, "amazon_jp": 0},
        "reviews": {
            "positive_rate": 91, "total_reviews": 8620,
            "positive_keywords": ["补水好", "敏感肌可用", "性价比高", "精华多"],
            "negative_keywords": ["假货多", "批次差异大"],
            "samples": [
                {"rating": 5, "lang": "zh", "text": "第三次回购了，比专柜便宜好多"},
                {"rating": 3, "lang": "zh", "text": "这次买的感觉和上次不太一样"},
            ],
        },
        "logistics": {"days": "4-6", "freight": 20, "free_threshold": 149, "carrier": "圆通国际"},
        "tariff": {"rate": "6.5%", "category": "化妆品类", "note": "需额外缴纳增值税13%"},
        "compliance": {
            "checks": [
                {"id": "ingredients", "label": "成分合规", "status": "warning", "detail": "含水杨酸（限用2%），需确认配方浓度"},
                {"id": "labeling", "label": "中文标签", "status": "pass", "detail": "已加贴中文成分表"},
                {"id": "fda_filing", "label": "药监局备案", "status": "warning", "detail": "韩国品牌需补充NMPA进口备案"},
                {"id": "animal_testing", "label": "动物测试豁免", "status": "pass", "detail": "符合《化妆品监督管理条例》"},
            ],
            "overall_pass": True,
            "applicable_markets": ["中国大陆"],
        },
        "decision_chain": {
            "price": "考拉¥78最高差价22%，但亚马逊无此SKU，跨境独家优势明显",
            "tariff": "化妆品关税6.5%+增值税13%，建议B2B方式降低税率",
            "compliance": "NMPA备案是关键阻塞点，需供应商配合提供材料",
            "recommendation": "先小批量测试NMPA备案周期，通过后大规模进货"
        },
        "i18n": {
            "en": {"product_name": "MEDIHEAL Mask 10-pack", "category": "Beauty", "origin": "Korea"},
            "ja": {"product_name": "メディヒール マスク 10枚入り", "category": "美容", "origin": "韓国"},
        },
    },
    "au_health": {
        "id": "au_health",
        "query_hint": "Swisse鱼油能寄到中国吗",
        "product": {"name": "Swisse 深海鱼油 400粒", "category": "保健品", "origin": "澳大利亚", "weight": "500g"},
        "prices": {"tmall": 168, "jd": 175, "kaola": 155, "amazon_jp": 0},
        "reviews": {
            "positive_rate": 88, "total_reviews": 5200,
            "positive_keywords": ["性价比高", "颗粒小好吞", "澳洲直邮"],
            "negative_keywords": ["包装简陋", "到货慢"],
            "samples": [
                {"rating": 4, "lang": "zh", "text": "给爸妈买的，他们觉得比国内品牌好"},
                {"rating": 2, "lang": "zh", "text": "半个月才到，等的太久了"},
            ],
        },
        "logistics": {"days": "10-15", "freight": 45, "free_threshold": 299, "carrier": "澳洲邮政/递四方"},
        "tariff": {"rate": "6%", "category": "保健品", "note": "需提供原产地证明+卫生证书"},
        "compliance": {
            "checks": [
                {"id": "import_license", "label": "进口许可", "status": "warning", "detail": "保健品需取得《保健食品注册证书》"},
                {"id": "labeling", "label": "中文标签", "status": "warning", "detail": "需标注'保健食品不是药物'"},
                {"id": "origin_doc", "label": "原产地证明", "status": "pass", "detail": "澳大利亚原产地证可申请"},
                {"id": "gmp", "label": "GMP认证", "status": "pass", "detail": "Swisse工厂通过TGA GMP认证"},
            ],
            "overall_pass": False,
            "applicable_markets": ["中国大陆（需备案）"],
        },
        "decision_chain": {
            "price": "考拉¥155最低，但运费¥45→综合成本¥200，利润空间有限",
            "tariff": "保健品关税6%+增值税13%，同类商品中偏低",
            "compliance": "保健品备案周期2-3个月，Swisse已有部分SKU获批，优先推已备案SKU",
            "recommendation": "先确认该SKU备案状态，未备案则不建议大规模进货"
        },
        "i18n": {
            "en": {"product_name": "Swisse Fish Oil 400 Caps", "category": "Supplement", "origin": "Australia"},
            "ja": {"product_name": "スワイス フィッシュオイル 400粒", "category": "サプリ", "origin": "オーストラリア"},
        },
    },
}


class ScenarioStore:
    """Store and retrieve scenarios for reproducible, narrative-driven demos."""

    @staticmethod
    def find(query: str) -> dict | None:
        q = query.lower()
        for sid, sc in SCENARIOS.items():
            hints = [sc["product"]["name"].lower(), sc["product"]["category"].lower(),
                     sc["product"]["origin"].lower(), sc.get("query_hint", "").lower()]
            if any(h and h in q for h in hints):
                return sc
        kw_map = {
            "日本": "japanese_snack", "零食": "japanese_snack", "白色恋人": "japanese_snack",
            "韩国": "korean_cosmetics", "面膜": "korean_cosmetics", "美妆": "korean_cosmetics",
            "澳洲": "au_health", "鱼油": "au_health", "保健": "au_health", "swisse": "au_health",
        }
        for kw, sid in kw_map.items():
            if kw.lower() in q:
                return SCENARIOS[sid]
        return None

    @staticmethod
    def get_default() -> dict:
        return SCENARIOS["japanese_snack"]
