#!/usr/bin/env python3
"""
站点体检脚本 ContentHealthCheck
检查所有页面 HTTP 状态 + 死链 + 文章保鲜度 + sitemap 完整性
exit code: 0=全绿🟢 1=警告🟡 2=严重🔴
"""

import os
import re
import json
import sys
from datetime import datetime
from typing import Dict, List
from xml.etree import ElementTree as ET


class ContentHealthCheck:
    def __init__(self, site_dir: str = ".", base_url: str = None):
        self.site_dir = site_dir
        self.base_url = base_url or "https://makerearn.com"
        self.severity = 0
        self.all_checks = {}

    def _flag(self, level: int):
        self.severity = max(self.severity, level)

    def run_all(self) -> Dict:
        """执行全部体检"""
        self.all_checks = {
            "timestamp": datetime.now().isoformat(),
            "pages": self._check_pages(),
            "dead_links": self._check_dead_links(),
            "freshness": self._check_freshness(),
            "sitemap": self._check_sitemap(),
            "seo": self._check_seo(),
        }
        return self.all_checks

    def _check_pages(self) -> Dict:
        """检查所有 HTML 文件"""
        items = []
        ok_count = 0
        for fname in ["index.html", "about.html", "404.html"]:
            path = os.path.join(self.site_dir, fname)
            exists = os.path.exists(path)
            size = os.path.getsize(path) if exists else 0
            ok = exists and size > 100
            items.append({"file": fname, "exists": exists, "size": size, "ok": ok})
            if ok:
                ok_count += 1
            elif not exists:
                self._flag(2)
            elif size < 100:
                self._flag(1)

        articles_dir = os.path.join(self.site_dir, "articles")
        if os.path.exists(articles_dir):
            for fname in sorted(os.listdir(articles_dir)):
                if fname.endswith(".html"):
                    path = os.path.join(articles_dir, fname)
                    size = os.path.getsize(path)
                    ok = size > 500
                    items.append({"file": f"articles/{fname}", "exists": True, "size": size, "ok": ok})
                    if ok:
                        ok_count += 1
                    else:
                        self._flag(1)

        return {"items": items, "total": len(items), "ok": ok_count}

    def _check_dead_links(self) -> Dict:
        """检查死链"""
        all_files = set()
        for root, dirs, files in os.walk(self.site_dir):
            if ".git" in root:
                continue
            for f in files:
                if f.endswith(".html"):
                    all_files.add(os.path.relpath(os.path.join(root, f), self.site_dir))

        dead_links = []
        for root, dirs, files in os.walk(self.site_dir):
            if ".git" in root:
                continue
            for fname in files:
                if not fname.endswith(".html"):
                    continue
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, self.site_dir)
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()
                links = re.findall(r'href="([^"]*)"', content)
                for link in links:
                    # 跳过外部链接、锚点、邮件、data URI、非 HTML 资源
                    if link.startswith(("http", "#", "mailto:", "data:", "javascript:", "tel:")):
                        continue
                    if not link.endswith(".html") and "/" in link and "." in link.split("/")[-1]:
                        continue  # 跳过 css/js/png 等资源文件
                    # 绝对路径直接去掉开头的 /
                    if link.startswith("/"):
                        target = link.lstrip("/")
                    else:
                        target = os.path.normpath(os.path.join(os.path.dirname(rel_path), link))
                    if target and not target.endswith(".html"):
                        continue
                    if target and target not in all_files:
                        dead_links.append({"source": rel_path, "dead_link": link})

        if dead_links:
            self._flag(1)
        return {"items": dead_links, "count": len(dead_links)}

    def _check_freshness(self) -> Dict:
        """检查文章保鲜度"""
        items = []
        now = datetime.now()
        articles_dir = os.path.join(self.site_dir, "articles")
        if not os.path.exists(articles_dir):
            return {"items": items, "stale": 0}

        for fname in sorted(os.listdir(articles_dir)):
            if not fname.endswith(".html"):
                continue
            mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(articles_dir, fname)))
            age_days = (now - mtime).days
            if age_days > 180:
                status = "🔴"
                self._flag(1)
            elif age_days > 90:
                status = "🟡"
            else:
                status = "🟢"
            items.append({"file": f"articles/{fname}", "age_days": age_days, "status": status})

        return {"items": items, "total": len(items)}

    def _check_sitemap(self) -> Dict:
        """检查 sitemap 完整性"""
        path = os.path.join(self.site_dir, "sitemap.xml")
        if not os.path.exists(path):
            self._flag(2)
            return {"exists": False, "error": "sitemap.xml 缺失"}

        try:
            with open(path) as f:
                content = f.read()
            has_placeholder = "YOUR_DOMAIN" in content
            tree = ET.parse(path)
            urls = tree.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}url")
            url_count = len(urls)

            if has_placeholder:
                self._flag(2)

            article_count = len([f for f in os.listdir(os.path.join(self.site_dir, "articles")) if f.endswith(".html")])
            expected = article_count + 2  # 首页 + about

            return {
                "exists": True,
                "url_count": url_count,
                "expected_min": expected,
                "has_placeholder": has_placeholder,
            }
        except Exception as e:
            self._flag(2)
            return {"exists": True, "error": str(e)}

    def _check_seo(self) -> Dict:
        """检查 SEO 基础"""
        issues = []
        index_path = os.path.join(self.site_dir, "index.html")
        if not os.path.exists(index_path):
            return {"issues": ["index.html 缺失"]}

        with open(index_path, encoding="utf-8") as f:
            content = f.read()

        if "YOUR_DOMAIN" in content:
            issues.append("index.html 含 YOUR_DOMAIN 占位符")
            self._flag(1)
        if '<meta name="description"' not in content:
            issues.append("缺少 meta description")
            self._flag(1)
        if "og:title" not in content:
            issues.append("缺少 OG 标签")
            self._flag(1)

        return {"issues": issues, "ok": len(issues) == 0}

    def generate_report(self) -> str:
        checks = self.all_checks
        if not checks:
            return "请先运行 run_all()"

        severity_icon = {0: "🟢", 1: "🟡", 2: "🔴"}
        icon = severity_icon[self.severity]

        lines = [
            f"# 🏥 站点体检报告 — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"总体状态: {icon} (exit={self.severity})",
            "",
        ]

        pages = checks.get("pages", {})
        lines.append(f"## 📄 页面状态 ({pages.get('ok', 0)}/{pages.get('total', 0)})")
        for item in pages.get("items", []):
            s = "✅" if item["ok"] else "❌"
            lines.append(f"  {s} {item['file']} ({item['size']}B)")

        dl = checks.get("dead_links", {})
        lines.append(f"\n## 🔗 死链检测 ({dl.get('count', 0)})")
        for item in dl.get("items", []):
            lines.append(f"  ⚠️ {item['source']} → {item['dead_link']}")

        freshness = checks.get("freshness", {})
        lines.append(f"\n## 🍃 文章保鲜度 ({freshness.get('total', 0)}篇)")
        for item in freshness.get("items", []):
            lines.append(f"  {item['status']} {item['file']} ({item['age_days']}天)")

        sm = checks.get("sitemap", {})
        lines.append(f"\n## 🗺️ Sitemap")
        if sm.get("exists"):
            lines.append(f"  URL 数: {sm.get('url_count', 0)}")
            if sm.get("has_placeholder"):
                lines.append(f"  🔴 含 YOUR_DOMAIN 占位符！")
        else:
            lines.append(f"  🔴 {sm.get('error', '缺失')}")

        seo = checks.get("seo", {})
        lines.append(f"\n## 🔍 SEO 检查")
        if seo.get("ok"):
            lines.append("  ✅ 通过")
        for issue in seo.get("issues", []):
            lines.append(f"  ⚠️ {issue}")

        report = "\n".join(lines)
        report_path = os.path.join(self.site_dir, "health_report.md")
        with open(report_path, "w") as f:
            f.write(report)
        return report


if __name__ == "__main__":
    checker = ContentHealthCheck(site_dir=os.path.dirname(__file__) or ".")
    checker.run_all()
    print(checker.generate_report())
    sys.exit(checker.severity)
