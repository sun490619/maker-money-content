#!/usr/bin/env python3
"""
Playwright 真实浏览器健康检查
打开 makerearn.com 验证：页面加载、中英切换、图标渲染、文章完整性
exit code: 0=全绿🟢 1=警告🟡 2=严重🔴
"""

import subprocess
import sys
import os
import json
import time
from datetime import datetime

RESULTS = {"timestamp": datetime.now().isoformat(), "checks": [], "severity": 0}


def run_check(name: str, func):
    """执行单条检查"""
    try:
        result = func()
        RESULTS["checks"].append({"name": name, "status": "pass", "data": result})
        print(f"  ✅ {name}")
    except AssertionError as e:
        RESULTS["checks"].append({"name": name, "status": "fail", "error": str(e)})
        RESULTS["severity"] = max(RESULTS["severity"], 2)
        print(f"  🔴 {name}: {e}")
    except Exception as e:
        RESULTS["checks"].append({"name": name, "status": "error", "error": str(e)})
        RESULTS["severity"] = max(RESULTS["severity"], 1)
        print(f"  🟡 {name}: {e}")


def main():
    print("=" * 60)
    print(f"🏥 makerearn.com 浏览器健康检查 — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("安装 playwright...")
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)
        subprocess.run(["playwright", "install", "chromium", "--with-deps"], check=True)
        from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ========== 首页检查 ==========

        def check_homepage_loads():
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            try:
                resp = page.goto("https://makerearn.com", wait_until="networkidle", timeout=30000)
                assert resp.status == 200, f"HTTP {resp.status}"
                title = page.title()
                assert "Maker Earn" in title or "搞钱" in title, f"标题异常: {title}"
                # 检查导航栏
                nav = page.query_selector("nav")
                assert nav is not None, "导航栏缺失"
                # 检查语言切换按钮
                btn = page.query_selector("#lang-switch")
                assert btn is not None, "语言切换按钮缺失"
                btn_text = btn.inner_text()
                # 检查文章列表
                articles = page.query_selector_all("article, .article-card, .post-card")
                assert len(articles) >= 3, f"文章数={len(articles)}, 太少"
                return {
                    "status_code": resp.status,
                    "title": title,
                    "articles_count": len(articles),
                    "lang_btn_visible": True,
                    "btn_text": btn_text,
                }
            finally:
                ctx.close()

        run_check("首页加载 & 基础结构", check_homepage_loads)

        # ========== 中英切换（首页） ==========

        def check_homepage_i18n():
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            try:
                page.goto("https://makerearn.com", wait_until="networkidle", timeout=30000)

                # 默认英文 → 检查英文标题
                hero = page.query_selector('[data-i18n="hero.title"]')
                if hero:
                    initial_text = hero.inner_text()
                    assert "Make Money" in initial_text, f"英文标题异常: {initial_text}"
                else:
                    # fallback: 查 h1
                    h1 = page.query_selector("h1")
                    initial_text = h1.inner_text() if h1 else ""

                # 点中文按钮
                btn = page.query_selector("#lang-switch")
                assert btn is not None, "无语言切换按钮"
                btn.click()
                page.wait_for_timeout(500)

                # 检查是否切换到中文
                hero = page.query_selector('[data-i18n="hero.title"]')
                if hero:
                    zh_text = hero.inner_text()
                else:
                    zh_text = page.query_selector("h1").inner_text() if page.query_selector("h1") else ""
                
                assert "搞钱" in zh_text or "独立" in zh_text, f"中文切换失败, 标题: {zh_text}"

                # 按钮文字应该变成 EN
                new_btn_text = btn.inner_text()
                return {
                    "en_title": initial_text,
                    "zh_title": zh_text,
                    "after_switch_btn": new_btn_text,
                }
            finally:
                ctx.close()

        run_check("首页中英切换", check_homepage_i18n)

        # ========== 文章页检查 ==========

        def check_article_page():
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            try:
                resp = page.goto(
                    "https://makerearn.com/articles/gumroad-beginner-guide.html",
                    wait_until="networkidle",
                    timeout=30000,
                )
                assert resp.status == 200, f"HTTP {resp.status}"

                # 文章标题
                h1 = page.query_selector("h1")
                assert h1 is not None, "缺少文章标题"
                en_title = h1.inner_text()
                assert "Gumroad" in en_title, f"文章标题异常: {en_title}"

                # 文章正文
                body = page.query_selector(".article-body")
                assert body is not None, "缺少文章正文区"
                body_text = body.inner_text()
                assert len(body_text) > 200, f"文章正文太短: {len(body_text)} chars"

                # 点中文按钮
                btn = page.query_selector("#lang-switch")
                assert btn is not None, "无语言切换按钮"
                btn.click()
                page.wait_for_timeout(800)

                # 正文变成中文
                zh_body = page.query_selector(".article-body").inner_text()
                # 中文翻译正文应该包含中文汉字
                has_chinese = any("\u4e00" <= c <= "\u9fff" for c in zh_body)
                assert has_chinese, f"文章正文切换中文失败, 未检测到中文字符"

                return {
                    "en_title": en_title,
                    "zh_body_preview": zh_body[:100],
                    "has_chinese": has_chinese,
                }
            finally:
                ctx.close()

        run_check("文章页加载 & 正文中文切换", check_article_page)

        # ========== Lucide 图标渲染检查 ==========

        def check_lucide_icons():
            ctx = browser.new_context(viewport={"width": 1440, "height": 900})
            page = ctx.new_page()
            try:
                page.goto("https://makerearn.com", wait_until="networkidle", timeout=30000)
                # lucide 图标在 DOM 里是 <i data-lucide="..."> 渲染后变成 <svg>
                icons = page.query_selector_all("svg")
                # 期望至少有几个 SVG 图标
                assert len(icons) >= 2, f"SVG 图标数={len(icons)}, 太少"
                return {"svg_icons_count": len(icons)}
            finally:
                ctx.close()

        run_check("Lucide 图标渲染", check_lucide_icons)

        # ========== 关键页面可访问 ==========

        def check_all_pages():
            pages_to_check = [
                "https://makerearn.com",
                "https://makerearn.com/about.html",
                "https://makerearn.com/articles/gumroad-beginner-guide.html",
                "https://makerearn.com/articles/digital-product-ideas-2026.html",
                "https://makerearn.com/sitemap.xml",
            ]
            ctx = browser.new_context()
            page = ctx.new_page()
            fails = []
            try:
                for url in pages_to_check:
                    resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    if resp.status >= 400:
                        fails.append(f"{url} → HTTP {resp.status}")
                assert len(fails) == 0, "; ".join(fails)
                return {"pages_checked": len(pages_to_check), "all_ok": True}
            finally:
                ctx.close()

        run_check("关键页面 HTTP 200", check_all_pages)

        browser.close()

    # 生成报告
    print()
    print("=" * 60)
    print("📊 检查结果汇总")
    print("=" * 60)
    passes = sum(1 for c in RESULTS["checks"] if c["status"] == "pass")
    fails = sum(1 for c in RESULTS["checks"] if c["status"] == "fail")
    errors = sum(1 for c in RESULTS["checks"] if c["status"] == "error")
    print(f"  ✅ 通过: {passes}")
    print(f"  🔴 失败: {fails}")
    print(f"  🟡 异常: {errors}")
    print(f"  Severity: {RESULTS['severity']}")

    # 保存 JSON 结果
    report_path = os.path.join(os.path.dirname(__file__), "health_report.json")
    with open(report_path, "w") as f:
        json.dump(RESULTS, f, ensure_ascii=False, indent=2)
    print(f"\n报告已保存: {report_path}")

    severity_icon = {0: "🟢", 1: "🟡", 2: "🔴"}
    icon = severity_icon[RESULTS["severity"]]

    # 写入 GitHub Actions Step Summary
    if "GITHUB_STEP_SUMMARY" in os.environ:
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a") as f:
            f.write(f"## 🏥 makerearn.com 浏览器体检 {icon}\n\n")
            f.write(f"| 检查项 | 状态 | 详情 |\n")
            f.write(f"|--------|------|------|\n")
            for c in RESULTS["checks"]:
                s = "✅" if c["status"] == "pass" else "🔴" if c["status"] == "fail" else "🟡"
                d = c.get("data", c.get("error", ""))
                if isinstance(d, dict):
                    d = json.dumps(d, ensure_ascii=False)
                f.write(f"| {c['name']} | {s} | {str(d)[:200]} |\n")

    sys.exit(RESULTS["severity"])


if __name__ == "__main__":
    main()
