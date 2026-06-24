# coding=utf-8
"""
知识内容获取器

策略：搜索引擎搜知乎/V2EX/掘金等高质量平台，避免公众号低质内容
"""

import hashlib
import re
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import quote, urlparse

import feedparser
import requests
from bs4 import BeautifulSoup


class KnowledgeFetcher:
    """知识内容获取器"""

    DEFAULT_TIMEOUT = 15
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": self.USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "zh-CN,zh;q=0.9",
        })
        if proxy_url:
            self.session.proxies = {"http": proxy_url, "https": proxy_url}

    # --- 搜索引擎 + 高质量站点搜索 ---

    def search_bing(self, query: str, site: str = "", max_items: int = 5) -> List[Dict]:
        """通过 Bing 搜索指定站点的高质量内容"""
        try:
            search_q = f"site:{site} {query}" if site else query
            url = f"https://www.bing.com/search?q={quote(search_q)}&setlang=zh-cn&cc=cn"
            resp = self.session.get(url, timeout=self.DEFAULT_TIMEOUT)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, "html.parser")
            items = []

            for result in soup.select("li.b_algo"):
                if len(items) >= max_items:
                    break
                title_tag = result.select_one("h2 a")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")
                snippet_tag = result.select_one(".b_caption p")
                snippet = snippet_tag.get_text(strip=True)[:250] if snippet_tag else ""

                if title and link:
                    items.append({
                        "title": title,
                        "url": link,
                        "summary": snippet,
                        "source": urlparse(link).netloc or "web",
                    })
            return items
        except Exception as e:
            print(f"  [!] Bing 搜索失败 [{query}]: {e}")
            return []

    def search_quality(self, queries: List[Dict], max_workers: int = 5) -> List[Dict]:
        """搜索关键词（Bing 搜知乎优先，微信兜底），按板块组织"""
        results = []

        for group in queries:
            section_items = []
            seen_urls = set()

            # 是否有指定平台（如房源走贝壳/链家）
            platforms = group.get("platforms", [])
            for kw in group["keywords"]:
                items = []
                if platforms:
                    # 在指定专业平台搜索
                    for plat in platforms:
                        site_items = self.search_bing(kw, site=plat, max_items=2)
                        items += site_items
                # 通用搜索兜底
                if not items:
                    items = self.search_weixin(kw, max_items=3)
                for item in items:
                    url_hash = hashlib.md5(item["url"].encode()).hexdigest()
                    if url_hash not in seen_urls:
                        seen_urls.add(url_hash)
                        section_items.append(item)

            section_items = section_items[:group.get("max_items", 3)]

            if section_items:
                results.append({
                    "name": group["name"],
                    "category": group.get("category", ""),
                    "items": section_items,
                })

        return results

    # --- RSS 抓取 ---

    def fetch_feed(self, url: str, timeout: int = None) -> List[Dict]:
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT
        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)
            items = []
            for entry in feed.entries[:10]:
                title = entry.get("title", "").strip()
                if not title:
                    continue
                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                summary = self._strip_html(summary)[:200]
                items.append({
                    "title": title,
                    "url": link,
                    "summary": summary,
                    "source": urlparse(url).netloc,
                })
            return items
        except Exception as e:
            print(f"  [!] RSS 失败 [{url}]: {e}")
            return []

    def fetch_all(self, sources: List[Dict], max_workers: int = 5) -> List[Dict]:
        feed_map = {}
        all_urls = []
        for idx, source in enumerate(sources):
            for feed_url in source["feeds"]:
                all_urls.append(feed_url)
                feed_map.setdefault(idx, []).append(feed_url)

        url_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self.fetch_feed, url): url for url in all_urls}
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    url_results[url] = future.result()
                except Exception as e:
                    print(f"  [!] 并发异常 [{url}]: {e}")
                    url_results[url] = []

        results = []
        for idx, source in enumerate(sources):
            section_items = []
            seen_titles = set()
            for feed_url in source["feeds"]:
                for item in url_results.get(feed_url, []):
                    th = hashlib.md5(item["title"].encode()).hexdigest()
                    if th not in seen_titles:
                        seen_titles.add(th)
                        section_items.append(item)
            section_items = section_items[:source.get("max_items", 3)]
            if section_items:
                results.append({
                    "name": source["name"],
                    "category": source.get("category", ""),
                    "items": section_items,
                })
        return results

    # --- 搜狗微信搜索（兜底） ---

    LOW_QUALITY_PATTERNS = [
        "什么是", "如何入门", "新手必看", "小白", "一文读懂",
        "你必须知道", "惊人", "秒懂", "三分钟", "五分钟",
        "你应该", "每个人都", "99%", "揭秘", "原来",
    ]

    def _is_quality_title(self, title: str) -> bool:
        for pattern in self.LOW_QUALITY_PATTERNS:
            if pattern in title:
                return False
        return len(title) >= 8

    def search_weixin(self, keyword: str, max_items: int = 5) -> List[Dict]:
        try:
            url = f"https://weixin.sogou.com/weixin?type=2&query={quote(keyword)}&ie=utf8"
            resp = self.session.get(url, timeout=self.DEFAULT_TIMEOUT)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, "html.parser")
            items = []
            for li in soup.select("ul.news-list li"):
                if len(items) >= max_items:
                    break
                title_tag = li.select_one("a[id*=_title_]")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                if not self._is_quality_title(title):
                    continue
                link = title_tag.get("href", "")
                if link and link.startswith("/"):
                    link = "https://weixin.sogou.com" + link
                summary_tag = li.select_one("p.txt-info")
                summary = summary_tag.get_text(strip=True)[:200] if summary_tag else ""
                if title:
                    items.append({
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "source": "微信公众号",
                    })
            return items
        except Exception as e:
            print(f"  [!] 微信搜索失败 [{keyword}]: {e}")
            return []

    @staticmethod
    def _strip_html(text: str) -> str:
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
