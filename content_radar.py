#!/usr/bin/env python3
"""
需求雷达 + 选题引擎 ContentRadar
从 10 个水源抓取 → 闲聊过滤 → 意图分类 → 选题池
输出：topic_pool.json（选题池）+ radar_report.md（可读报告）
"""

import json
import hashlib
import time
import os
import re
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict, field

from content_filter import ChatterFilter
from content_classifier import ContentClassifier


@dataclass
class Topic:
    """选题数据结构"""
    id: str
    title: str
    keywords: List[str]
    outline: List[str]
    priority: int  # 1-10，越高越优先
    source: str
    source_url: str
    category: str
    created_at: str
    confidence: float
    search_volume_hint: str  # high / medium / low
    status: str = "pending"  # pending / writing / written / published / rejected


class ContentRadar:
    """需求雷达 + 选题引擎"""

    WATER_SOURCES = [
        {"name": "Hacker News", "url": "https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=20", "type": "api", "weight": 1.2},
        {"name": "V2EX", "url": "https://www.v2ex.com/api/topics/hot.json", "type": "api", "weight": 1.0},
        {"name": "GitHub Trending", "url": "https://api.github.com/search/repositories?q=stars:>100+pushed:>2026-06-01&sort=stars&per_page=10", "type": "api", "weight": 1.0},
        {"name": "Dev.to", "url": "https://dev.to/feed", "type": "rss", "weight": 0.8},
        {"name": "Reddit r/SideProject", "url": "https://www.reddit.com/r/SideProject/hot.json?limit=15", "type": "api", "weight": 1.0},
        {"name": "Reddit r/automation", "url": "https://www.reddit.com/r/automation/hot.json?limit=10", "type": "api", "weight": 0.8},
        {"name": "Reddit r/productivity", "url": "https://www.reddit.com/r/productivity/hot.json?limit=10", "type": "api", "weight": 0.7},
        {"name": "Reddit r/Python", "url": "https://www.reddit.com/r/Python/hot.json?limit=10", "type": "api", "weight": 0.6},
        {"name": "Reddit r/selfhosted", "url": "https://www.reddit.com/r/selfhosted/hot.json?limit=10", "type": "api", "weight": 0.6},
        {"name": "HackerNoon", "url": "https://hackernoon.com/feed", "type": "rss", "weight": 0.7},
    ]

    CATEGORY_MAP = {
        "数字产品": "digital-products",
        "AI": "ai-tools",
        "工具": "ai-tools",
        "副业": "side-hustle",
        "赚钱": "side-hustle",
        "效率": "productivity",
        "自动化": "productivity",
    }

    def __init__(self, data_dir: str = "."):
        self.filter = ChatterFilter()
        self.classifier = ContentClassifier()
        self.data_dir = data_dir
        self.seen_hashes: Dict[str, str] = {}
        self.topic_pool: List[Topic] = []
        self._ensure_data_files()
        self._load_state()

    def _ensure_data_files(self):
        os.makedirs(self.data_dir, exist_ok=True)
        for fname, default in [
            ("topic_pool.json", []),
            ("seen_hashes.json", {}),
            ("radar_log.json", []),
        ]:
            fpath = os.path.join(self.data_dir, fname)
            if not os.path.exists(fpath):
                with open(fpath, "w") as f:
                    json.dump(default, f, ensure_ascii=False, indent=2)

    def _load_state(self):
        try:
            with open(os.path.join(self.data_dir, "seen_hashes.json")) as f:
                self.seen_hashes = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.seen_hashes = {}

        try:
            with open(os.path.join(self.data_dir, "topic_pool.json")) as f:
                data = json.load(f)
                self.topic_pool = [Topic(**t) for t in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.topic_pool = []

    def _save_state(self):
        with open(os.path.join(self.data_dir, "seen_hashes.json"), "w") as f:
            json.dump(self.seen_hashes, f, ensure_ascii=False, indent=2)
        with open(os.path.join(self.data_dir, "topic_pool.json"), "w") as f:
            json.dump([asdict(t) for t in self.topic_pool], f, ensure_ascii=False, indent=2)

    def _make_hash(self, title: str) -> str:
        return hashlib.md5(title.strip().lower().encode()).hexdigest()[:12]

    def _is_duplicate(self, title: str) -> bool:
        h = self._make_hash(title)
        if h in self.seen_hashes:
            return True
        for t in self.topic_pool:
            if t.id == h:
                return True
        return False

    def _mark_seen(self, title: str, source: str):
        h = self._make_hash(title)
        self.seen_hashes[h] = f"{source}@{datetime.now().isoformat()}"

    def _categorize(self, text: str) -> str:
        text_lower = text.lower()
        for cn, en in self.CATEGORY_MAP.items():
            if cn in text_lower:
                return en
        return "ai-tools"  # 默认

    def _estimate_search_volume(self, title: str, score: float) -> str:
        if score > 5:
            return "high"
        elif score > 3:
            return "medium"
        return "low"

    def _calc_priority(self, confidence: float, weight: float, score: float) -> int:
        raw = confidence * 5 + weight * 2 + score * 0.5
        return max(1, min(10, round(raw)))

    def _suggest_outline(self, title: str) -> List[str]:
        return [
            f"1. 痛点引入：为什么{title[:20]}是个问题",
            "2. 方案对比：市面上有哪些做法",
            "3. 实操步骤：具体怎么做（分步骤）",
            "4. 避坑指南：常见错误和注意事项",
            "5. 推荐工具：哪些工具能帮上忙",
            "6. 延伸阅读：相关资源推荐",
        ]

    # ===== 水源抓取 =====

    def _fetch_json(self, url: str, headers: dict = None) -> Optional[dict]:
        req_headers = {"User-Agent": "MakerMoneyContentBot/1.0", **(headers or {})}
        try:
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"  ⚠️ 抓取失败 {url[:60]}: {e}")
            return None

    def _fetch_rss(self, url: str) -> List[dict]:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MakerMoneyContentBot/1.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read()
            root = ET.fromstring(content)
            items = []
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            for entry in root.findall(".//item"):
                title_el = entry.find("title")
                link_el = entry.find("link")
                desc_el = entry.find("description")
                title = title_el.text if title_el is not None else ""
                link = link_el.text if link_el is not None else ""
                desc = desc_el.text if desc_el is not None else ""
                items.append({"title": title, "url": link, "description": desc})
            if not items:
                for entry in root.findall(".//atom:entry", ns):
                    title_el = entry.find("atom:title", ns)
                    link_el = entry.find("atom:link", ns)
                    title = title_el.text if title_el is not None else ""
                    link = link_el.attrib.get("href", "") if link_el is not None else ""
                    items.append({"title": title, "url": link, "description": ""})
            return items
        except Exception as e:
            print(f"  ⚠️ RSS 抓取失败 {url[:60]}: {e}")
            return []

    def _scrape_source(self, source: dict) -> List[dict]:
        """从单个水源抓取原始数据"""
        items = []
        name = source["name"]
        url = source["url"]
        stype = source["type"]

        if stype == "api":
            data = self._fetch_json(url)
            if not data:
                return []

            if "hits" in data:  # Hacker News
                for hit in data.get("hits", [])[:15]:
                    items.append({
                        "title": hit.get("title", ""),
                        "url": hit.get("url", f"https://news.ycombinator.com/item?id={hit.get('objectID','')}"),
                        "description": hit.get("story_text", "")[:200],
                        "score": hit.get("points", 0),
                        "source": name,
                    })
            elif isinstance(data, list):  # V2EX
                for item in data[:15]:
                    items.append({
                        "title": item.get("title", ""),
                        "url": item.get("url", f"https://www.v2ex.com/t/{item.get('id','')}"),
                        "description": item.get("content", "")[:200],
                        "score": item.get("replies", 0),
                        "source": name,
                    })
            elif "data" in data and "children" in data.get("data", {}):  # Reddit
                for child in data["data"]["children"][:15]:
                    d = child["data"]
                    items.append({
                        "title": d.get("title", ""),
                        "url": f"https://www.reddit.com{d.get('permalink','')}",
                        "description": d.get("selftext", "")[:200],
                        "score": d.get("score", 0),
                        "source": name,
                    })
            elif "items" in data:  # GitHub Trending
                for item in data.get("items", [])[:10]:
                    items.append({
                        "title": item.get("full_name", item.get("name", "")),
                        "url": item.get("html_url", ""),
                        "description": item.get("description", "")[:200],
                        "score": item.get("stargazers_count", 0),
                        "source": name,
                    })

        elif stype == "rss":
            for entry in self._fetch_rss(url)[:15]:
                items.append({
                    "title": entry.get("title", ""),
                    "url": entry.get("url", ""),
                    "description": re.sub(r'<[^>]+>', '', entry.get("description", ""))[:200],
                    "score": 0,
                    "source": name,
                })

        return items

    # ===== 主流程 =====

    def run(self) -> List[Topic]:
        """执行一次完整的雷达扫描"""
        print(f"\n{'='*60}")
        print(f"🔭 需求雷达扫描开始 — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}")

        all_items = []
        for src in self.WATER_SOURCES:
            print(f"\n📡 扫描 {src['name']}...")
            items = self._scrape_source(src)
            print(f"   抓取 {len(items)} 条")
            for item in items:
                item["weight"] = src["weight"]
            all_items.extend(items)
            time.sleep(1)  # 礼貌间隔

        print(f"\n📊 总计抓取 {len(all_items)} 条原始信号")

        # 逐条处理：过滤 → 分类 → 选题池
        new_topics = []
        for item in all_items:
            title = item.get("title", "")
            desc = item.get("description", "")
            text = f"{title} {desc}".strip()

            if not text or len(text) < 10:
                continue

            # 第一道：闲聊过滤
            passed, reason, meta = self.filter.check(text)
            if not passed:
                continue

            # 第二道：意图分类
            result = self.classifier.classify(text, source=item["source"], meta=meta)
            if not self.classifier.should_enter_pool(result):
                continue

            # 去重
            if self._is_duplicate(title):
                continue

            # 生成选题
            self._mark_seen(title, item["source"])
            topic_id = self._make_hash(title)

            topic = Topic(
                id=topic_id,
                title=title[:120],
                keywords=result.get("keywords", []),
                outline=self._suggest_outline(title),
                priority=self._calc_priority(
                    result["confidence"], item["weight"], result["scores"]["content"]
                ),
                source=item["source"],
                source_url=item.get("url", ""),
                category=self._categorize(text),
                created_at=datetime.now().isoformat(),
                confidence=result["confidence"],
                search_volume_hint=self._estimate_search_volume(
                    title, result["scores"]["content"]
                ),
            )
            self.topic_pool.append(topic)
            new_topics.append(topic)

        # 去重 + 按优先级排序
        seen_ids = set()
        unique_pool = []
        for t in sorted(self.topic_pool, key=lambda x: x.priority, reverse=True):
            if t.id not in seen_ids:
                unique_pool.append(t)
                seen_ids.add(t.id)
        self.topic_pool = unique_pool

        self._save_state()
        self._log_run(new_topics)

        print(f"\n🎯 本次新增选题: {len(new_topics)}")
        print(f"📦 选题池总计: {len(self.topic_pool)}")
        print(f"🗑️ 过滤拦截: {self.filter.stats()['blocked']}")
        print(f"✅ 放行通过: {self.filter.stats()['passed']}")

        return new_topics

    def _log_run(self, new_topics: List[Topic]):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "new_topics": len(new_topics),
            "total_pool": len(self.topic_pool),
            "filter_stats": self.filter.stats(),
            "classifier_stats": self.classifier.get_stats(),
        }
        log_path = os.path.join(self.data_dir, "radar_log.json")
        try:
            with open(log_path) as f:
                log = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            log = []
        log.append(log_entry)
        with open(log_path, "w") as f:
            json.dump(log, f, ensure_ascii=False, indent=2)

    def get_report(self) -> str:
        """生成可读的选题报告"""
        lines = [
            f"# 🔭 选题雷达报告 — {datetime.now().strftime('%Y-%m-%d')}",
            "",
            f"选题池总数: {len(self.topic_pool)}",
            "",
            "## 🔥 高优先级选题 (priority ≥ 7)",
            "",
        ]

        high = [t for t in self.topic_pool if t.priority >= 7][:10]
        for t in high:
            lines.append(f"- **[{t.priority}] {t.title}**")
            lines.append(f"  来源: {t.source} | 分类: {t.category} | 搜索量: {t.search_volume_hint}")
            lines.append(f"  关键词: {', '.join(t.keywords[:5])}")
            lines.append("")

        lines.append("## 🟡 中等优先级选题 (4-6)")
        lines.append("")
        mid = [t for t in self.topic_pool if 4 <= t.priority < 7][:10]
        for t in mid:
            lines.append(f"- [{t.priority}] {t.title} ({t.source})")
        lines.append("")

        lines.append("## 📊 统计")
        lines.append("")
        lines.append(f"- 高优先级: {len(high)}")
        lines.append(f"- 中优先级: {len(mid)}")
        lines.append(f"- 低优先级: {len([t for t in self.topic_pool if t.priority < 4])}")
        lines.append(f"- 本次过滤: {self.filter.stats()['blocked']} 条被拦截")

        report = "\n".join(lines)
        report_path = os.path.join(self.data_dir, "radar_report.md")
        with open(report_path, "w") as f:
            f.write(report)

        return report

    def get_next_topic(self) -> Optional[Topic]:
        """获取下一个待写的选题（优先级最高）"""
        pending = [t for t in self.topic_pool if t.status == "pending"]
        if not pending:
            return None
        return max(pending, key=lambda t: t.priority)


# ===== 命令行 =====
if __name__ == "__main__":
    import sys

    radar = ContentRadar(data_dir=os.path.dirname(__file__) or ".")

    if "--report" in sys.argv:
        print(radar.get_report())
    elif "--next" in sys.argv:
        topic = radar.get_next_topic()
        if topic:
            print(json.dumps(asdict(topic), ensure_ascii=False, indent=2))
        else:
            print("选题池为空，请先运行雷达扫描")
    else:
        new = radar.run()
        if new:
            print("\n" + radar.get_report())
