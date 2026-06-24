# coding=utf-8
"""
知识内容获取器

从 RSS/Atom 源抓取知识类内容，支持：
- 多源并发抓取
- 自动去重
- 数量限制
"""

import concurrent.futures
import hashlib
from datetime import datetime
from typing import Dict, List, Optional
from urllib.parse import urlparse

import feedparser
import requests


class KnowledgeFetcher:
    """知识内容获取器"""

    DEFAULT_TIMEOUT = 15
    DEFAULT_USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    def __init__(self, proxy_url: Optional[str] = None):
        self.proxy_url = proxy_url
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.DEFAULT_USER_AGENT})
        if proxy_url:
            self.session.proxies = {"http": proxy_url, "https": proxy_url}

    def fetch_feed(self, url: str, timeout: int = None) -> List[Dict]:
        """抓取单个 RSS 源"""
        if timeout is None:
            timeout = self.DEFAULT_TIMEOUT

        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            feed = feedparser.parse(resp.content)

            items = []
            for entry in feed.entries[:10]:  # 每个源最多取 10 条
                title = entry.get("title", "").strip()
                if not title:
                    continue

                link = entry.get("link", "")
                summary = entry.get("summary", "") or entry.get("description", "")
                published = entry.get("published", "") or entry.get("updated", "")

                # 去掉 HTML 标签获取纯文本摘要
                summary_text = self._strip_html(summary)[:200]

                items.append({
                    "title": title,
                    "url": link,
                    "summary": summary_text,
                    "published": published,
                    "source": urlparse(url).netloc,
                })

            return items

        except Exception as e:
            print(f"  [!] 知识源抓取失败 [{url}]: {e}")
            return []

    def fetch_all(self, sources: List[Dict], max_workers: int = 5) -> List[Dict]:
        """并发抓取所有知识源，返回按板块组织的结果"""
        feed_map = {}  # source_index -> [(feed_url, category_name)]
        all_urls = []

        for idx, source in enumerate(sources):
            for feed_url in source["feeds"]:
                all_urls.append(feed_url)
                if idx not in feed_map:
                    feed_map[idx] = []
                feed_map[idx].append(feed_url)

        # 并发抓取
        url_results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.fetch_feed, url): url for url in all_urls
            }
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    url_results[url] = future.result()
                except Exception as e:
                    print(f"  [!] 并发抓取异常 [{url}]: {e}")
                    url_results[url] = []

        # 按板块组织结果
        results = []
        for idx, source in enumerate(sources):
            section_items = []
            seen_titles = set()

            for feed_url in source["feeds"]:
                items = url_results.get(feed_url, [])
                for item in items:
                    # 用标题 hash 去重
                    title_hash = hashlib.md5(item["title"].encode()).hexdigest()
                    if title_hash not in seen_titles:
                        seen_titles.add(title_hash)
                        section_items.append(item)

            # 限制每个板块的条数
            max_items = source.get("max_items", 3)
            section_items = section_items[:max_items]

            if section_items:
                results.append({
                    "name": source["name"],
                    "category": source.get("category", ""),
                    "items": section_items,
                })

        return results

    @staticmethod
    def _strip_html(text: str) -> str:
        """简单去除 HTML 标签"""
        import re
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
