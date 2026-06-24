# coding=utf-8
"""
知识源配置

策略：精准搜索词 + 多源互补，追求干货而非科普
"""

# 搜狗微信搜索 — 用精准长尾词抓干货
KNOWLEDGE_QUERIES = [
    {
        "name": "🔧 机务与民航",
        "category": "机务",
        "keywords": [
            "机务维修 经验",
            "民航机务 职业发展",
            "飞机维修 技术",
            "机务工程师 工作",
        ],
        "max_items": 3,
    },
    {
        "name": "💼 转岗与职场",
        "category": "转岗",
        "keywords": [
            "转行 经验分享",
            "跳槽 涨薪 案例",
            "职业规划 中年",
            "面试 技巧 干货",
        ],
        "max_items": 3,
    },
    {
        "name": "📖 社会知识",
        "category": "社会",
        "keywords": [
            "法律常识 维权 案例",
            "社保 公积金 攻略",
            "租房 避坑 经验",
            "职场社交 情商",
        ],
        "max_items": 4,
    },
    {
        "name": "💪 健身与体态",
        "category": "健身",
        "keywords": [
            "健身 训练计划 干货",
            "体态矫正 方法",
            "运动解剖 肌肉",
            "营养 饮食 健身",
        ],
        "max_items": 3,
    },
    {
        "name": "🏥 医学常识",
        "category": "医学",
        "keywords": [
            "医学知识 普通人",
            "用药安全 常识",
            "急救 技能 科普",
            "体检报告 解读",
        ],
        "max_items": 3,
    },
    {
        "name": "🚗 汽车知识",
        "category": "汽车",
        "keywords": [
            "汽车评测 深度",
            "购车 避坑 经验",
            "汽车保养 省钱",
            "二手车 选购 技巧",
        ],
        "max_items": 3,
    },
    {
        "name": "🏠 成都双流房源",
        "category": "房源",
        "keywords": [
            "成都双流 租房 攻略",
            "成都 买房 地段分析",
            "成都 房价 走势",
        ],
        "max_items": 3,
    },
    {
        "name": "💰 赚钱思路",
        "category": "赚钱",
        "keywords": [
            "副业 实操 案例",
            "自由职业 经验",
            "创业 失败 教训",
            "搞钱 信息差",
        ],
        "max_items": 3,
    },
]

# 国内直连 RSS 源（高质量长文）
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
