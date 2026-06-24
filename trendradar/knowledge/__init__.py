# coding=utf-8
"""
知识日报模块

通过搜狗微信搜索 + 国内 RSS 获取知识内容。
"""

from .fetcher import KnowledgeFetcher
from .renderer import render_knowledge_html
from .sources import KNOWLEDGE_QUERIES, RSS_SOURCES
