# coding=utf-8
"""
知识源配置

GitHub Actions 中使用自建 RSSHub (localhost:1200)
"""

import os

RSSHUB_BASE = os.environ.get("RSSHUB_BASE_URL", "http://localhost:1200")

KNOWLEDGE_SOURCES = [
    {
        "name": "🔧 机务与民航",
        "category": "机务",
        "feeds": [
            f"{RSSHUB_BASE}/zhihu/search/机务",
            f"{RSSHUB_BASE}/zhihu/search/民航",
        ],
        "max_items": 3,
    },
    {
        "name": "💼 转岗与职场",
        "category": "转岗",
        "feeds": [
            f"{RSSHUB_BASE}/zhihu/search/转行",
            f"{RSSHUB_BASE}/zhihu/search/跳槽",
        ],
        "max_items": 3,
    },
    {
        "name": "📖 社会知识",
        "category": "社会",
        "feeds": [
            f"{RSSHUB_BASE}/zhihu/daily",
        ],
        "max_items": 4,
    },
    {
        "name": "💪 健身与体态",
        "category": "健身",
        "feeds": [
            f"{RSSHUB_BASE}/zhihu/search/健身",
            f"{RSSHUB_BASE}/zhihu/search/体态矫正",
        ],
        "max_items": 3,
    },
    {
        "name": "🏥 医学常识",
        "category": "医学",
        "feeds": [
            f"{RSSHUB_BASE}/dxy/todays/health",
            f"{RSSHUB_BASE}/zhihu/search/医学科普",
        ],
        "max_items": 3,
    },
    {
        "name": "🚗 汽车知识",
        "category": "汽车",
        "feeds": [
            f"{RSSHUB_BASE}/autohome/latest",
            f"{RSSHUB_BASE}/zhihu/search/汽车选购",
        ],
        "max_items": 3,
    },
    {
        "name": "🏠 成都双流房源",
        "category": "房源",
        "feeds": [
            f"{RSSHUB_BASE}/ke/zufang/cd/shuangliu",
        ],
        "max_items": 3,
    },
    {
        "name": "💰 赚钱思路",
        "category": "赚钱",
        "feeds": [
            f"{RSSHUB_BASE}/zhihu/search/副业",
            f"{RSSHUB_BASE}/zhihu/search/自由职业",
        ],
        "max_items": 3,
    },
    # 国内直连源（不需要 RSSHub）
    {
        "name": "💡 科技与效率",
        "category": "科技",
        "feeds": [
            "https://sspai.com/feed",
            "https://www.ifanr.com/feed",
        ],
        "max_items": 4,
    },
    {
        "name": "💼 商业与创投",
        "category": "商业",
        "feeds": [
            "https://36kr.com/feed",
            "https://www.tmtpost.com/rss.xml",
        ],
        "max_items": 4,
    },
    {
        "name": "📝 深度思考",
        "category": "思考",
        "feeds": [
            "https://www.ruanyifeng.com/blog/atom.xml",
        ],
        "max_items": 2,
    },
]
