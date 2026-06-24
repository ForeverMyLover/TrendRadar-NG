# coding=utf-8
"""
知识内容获取器

从搜狗微信搜索抓取公众号文章，覆盖所有知识领域。
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
    """知识内容获取器 — 基于搜狗微信搜索"""

    DEFAULT_TIMEOUT = 15
    BASE_URL = "https://weixin.sogou.com/weixin"
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

    def search_weixin(self, keyword: str, max_items: int = 5) -> List[Dict]:
        """搜索微信公众号文章"""
        try:
            url = f"{self.BASE_URL}?type=2&query={quote(keyword)}&ie=utf8"
            resp = self.session.get(url, timeout=self.DEFAULT_TIMEOUT)
            resp.raise_for_status()

            soup = BeautifulSoup(resp.content, "html.parser")
            items = []

            for li in soup.select("ul.news-list li"):
                if len(items) >= max_items:
                    break

                # 标题和链接
                title_tag = li.select_one("a[id*=_title_]")
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)

                # 链接（搜狗的是跳转链接）
                link = title_tag.get("href", "")
                if link and link.startswith("/"):
                    link = "https://weixin.sogou.com" + link

                # 摘要
                summary_tag = li.select_one("p.txt-info")
                summary = ""
                if summary_tag:
                    summary = summary_tag.get_text(strip=True)[:200]

                # 来源公众号名
                source_tag = li.select_one("a[id*=_account_]")
                source = ""
                if source_tag:
                    source = source_tag.get_text(strip=True)

                if title:
                    items.append({
                        "title": title,
                        "url": link,
                        "summary": summary,
                        "source": source or "微信公众号",
                    })

            return items

        except Exception as e:
            print(f"  [!] 微信搜索失败 [{keyword}]: {e}")
            return []

    def search_all(self, queries: List[Dict], max_workers: int = 5) -> List[Dict]:
        """并发搜索多个关键词，返回按板块组织的结果"""
        results = []

        for query_group in queries:
            section_items = []
            seen_titles = set()

            for kw in query_group["keywords"]:
                items = self.search_weixin(kw, max_items=5)
                for item in items:
                    title_hash = hashlib.md5(item["title"].encode()).hexdigest()
                    if title_hash not in seen_titles:
                        seen_titles.add(title_hash)
                        section_items.append(item)

            # 去重后限制数量
            section_items = section_items[:query_group.get("max_items", 3)]

            if section_items:
                results.append({
                    "name": query_group["name"],
                    "category": query_group.get("category", ""),
                    "items": section_items,
                })

        return results

    # --- RSS 抓取（保留国内直连源） ---

    def fetch_feed(self, url: str, timeout: int = None) -> List[Dict]:
        """抓取单个 RSS 源"""
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
            print(f"  [!] RSS 源失败 [{url}]: {e}")
            return []

    def fetch_all(self, sources: List[Dict], max_workers: int = 5) -> List[Dict]:
        """并发抓取 RSS 源"""
        feed_map = {}
        all_urls = []
        for idx, source in enumerate(sources):
            for feed_url in source["feeds"]:
                all_urls.append(feed_url)
                if idx not in feed_map:
                    feed_map[idx] = []
                feed_map[idx].append(feed_url)

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

    @staticmethod
    def _strip_html(text: str) -> str:
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()
