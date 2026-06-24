# coding=utf-8
"""
知识日报模块

从 RSS/Atom 源抓取知识类内容，生成知识日报。
"""

from .fetcher import KnowledgeFetcher
from .renderer import render_knowledge_html
from .sources import KNOWLEDGE_SOURCES
