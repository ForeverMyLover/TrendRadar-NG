# coding=utf-8
"""
知识源配置

基于搜狗微信搜索的关键词查询
"""

KNOWLEDGE_QUERIES = [
    {
        "name": "🔧 机务与民航",
        "category": "机务",
        "keywords": ["机务", "民航", "飞机维修"],
        "max_items": 3,
    },
    {
        "name": "💼 转岗与职场",
        "category": "转岗",
        "keywords": ["转行", "跳槽", "职业规划"],
        "max_items": 3,
    },
    {
        "name": "📖 社会知识",
        "category": "社会",
        "keywords": ["社会常识", "法律常识", "职场社交"],
        "max_items": 4,
    },
    {
        "name": "💪 健身与体态",
        "category": "健身",
        "keywords": ["健身", "体态矫正", "运动康复"],
        "max_items": 3,
    },
    {
        "name": "🏥 医学常识",
        "category": "医学",
        "keywords": ["医学常识", "健康科普", "养生"],
        "max_items": 3,
    },
    {
        "name": "🚗 汽车知识",
        "category": "汽车",
        "keywords": ["汽车选购", "新车评测", "汽车保养"],
        "max_items": 3,
    },
    {
        "name": "🏠 成都双流房源",
        "category": "房源",
        "keywords": ["成都租房", "双流租房", "成都买房"],
        "max_items": 3,
    },
    {
        "name": "💰 赚钱思路",
        "category": "赚钱",
        "keywords": ["副业", "自由职业", "创业经验"],
        "max_items": 3,
    },
]

# 国内直连 RSS 源（保留作为补充）
RSS_SOURCES = [
    {
        "name": "💡 科技与效率",
        "category": "科技",
        "feeds": ["https://sspai.com/feed", "https://www.ifanr.com/feed"],
        "max_items": 3,
    },
    {
        "name": "💼 商业与创投",
        "category": "商业",
        "feeds": ["https://36kr.com/feed", "https://www.tmtpost.com/rss.xml"],
        "max_items": 3,
    },
    {
        "name": "📝 深度思考",
        "category": "思考",
        "feeds": ["https://www.ruanyifeng.com/blog/atom.xml"],
        "max_items": 2,
    },
]
