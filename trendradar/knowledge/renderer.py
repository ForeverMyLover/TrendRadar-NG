# coding=utf-8
"""
知识日报 HTML 渲染器
"""

from datetime import datetime
from typing import Dict, List, Optional


def render_knowledge_html(
    results: List[Dict],
    title: str = "知识日报",
    update_time: Optional[str] = None,
) -> str:
    """
    渲染知识日报 HTML

    Args:
        results: 按板块组织的知识内容
        title: 报告标题
        update_time: 更新时间

    Returns:
        str: 完整 HTML
    """
    if update_time is None:
        update_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    sections_html = ""
    for section in results:
        items_html = ""
        for item in section["items"]:
            summary_html = ""
            if item.get("summary"):
                summary_html = (
                    f'<div class="item-summary">{_escape(item["summary"])}</div>'
                )
            items_html += f"""
                <div class="knowledge-item">
                    <div class="item-title">
                        <a href="{_escape(item['url'])}" target="_blank">{_escape(item['title'])}</a>
                    </div>
                    {summary_html}
                    <div class="item-source">{_escape(item.get('source', ''))}</div>
                </div>
            """

        sections_html += f"""
            <div class="knowledge-section">
                <h2 class="section-header">{_escape(section['name'])}</h2>
                {items_html}
            </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: -apple-system, "Microsoft YaHei", "PingFang SC", sans-serif;
        background: #f5f5f5;
        color: #333;
        line-height: 1.6;
    }}
    .container {{
        max-width: 680px;
        margin: 0 auto;
        padding: 20px;
    }}
    .header {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px 24px;
        border-radius: 12px;
        margin-bottom: 24px;
        text-align: center;
    }}
    .header h1 {{
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 6px;
    }}
    .header .time {{
        font-size: 13px;
        opacity: 0.85;
    }}
    .knowledge-section {{
        background: white;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}
    .section-header {{
        font-size: 17px;
        font-weight: 700;
        color: #333;
        margin-bottom: 14px;
        padding-bottom: 10px;
        border-bottom: 2px solid #667eea;
    }}
    .knowledge-item {{
        padding: 10px 0;
        border-bottom: 1px solid #f0f0f0;
    }}
    .knowledge-item:last-child {{
        border-bottom: none;
    }}
    .item-title {{
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 4px;
    }}
    .item-title a {{
        color: #333;
        text-decoration: none;
    }}
    .item-title a:hover {{
        color: #667eea;
    }}
    .item-summary {{
        font-size: 13px;
        color: #888;
        margin-bottom: 4px;
        line-height: 1.5;
    }}
    .item-source {{
        font-size: 11px;
        color: #bbb;
    }}
    .footer {{
        text-align: center;
        padding: 20px;
        color: #bbb;
        font-size: 12px;
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📚 {title}</h1>
        <div class="time">{update_time}</div>
    </div>
    {sections_html}
    <div class="footer">
        TrendRadar 知识日报 · 自动生成
    </div>
</div>
</body>
</html>"""

    return html


def _escape(text: str) -> str:
    """HTML 转义"""
    if not isinstance(text, str):
        text = str(text)
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )
