#!/usr/bin/env python3
"""
质量门禁 ContentGuard — 四道防线
发布前自动校验文章质量，不通过不准发
同时自动备份当前版本到 backups/
"""

import os
import re
import json
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field, asdict

from content_filter import ChatterFilter
from content_classifier import ContentClassifier


@dataclass
class GuardResult:
    """门禁检查结果"""
    passed: bool
    article_path: str
    checks: Dict[str, bool]  # 各道检查是否通过
    issues: List[str]  # 问题清单
    warnings: List[str]  # 警告（不阻塞发布）
    score: int  # 0-100 质量分
    backup_path: Optional[str] = None


class ContentGuard:
    """四道质量防线"""

    MIN_WORD_COUNT = 1500  # 最少1500字
    MIN_INTERNAL_LINKS = 3  # 最少3个内链
    REQUIRED_ELEMENTS = ["<title>", "<h1>", "<h2>", "<p>", "<meta name=\"description\""]

    def __init__(self, site_dir: str = "."):
        self.site_dir = site_dir
        self.filter = ChatterFilter()
        self.classifier = ContentClassifier()
        self.backup_dir = os.path.join(site_dir, "backups")
        os.makedirs(self.backup_dir, exist_ok=True)

    def check_article(self, article_path: str) -> GuardResult:
        """对单篇文章执行四道门禁检查"""
        full_path = os.path.join(self.site_dir, article_path)
        if not os.path.exists(full_path):
            return GuardResult(
                passed=False,
                article_path=article_path,
                checks={"exists": False},
                issues=[f"文件不存在: {full_path}"],
                warnings=[],
                score=0,
            )

        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取纯文本（去掉 HTML 标签）
        text = re.sub(r'<[^>]+>', ' ', content)
        text = re.sub(r'\s+', ' ', text).strip()

        checks = {}
        issues = []
        warnings = []
        score = 100

        # ===== 第一道：闲聊过滤 =====
        passed, reason, meta = self.filter.check(text)
        checks["filter_noise"] = passed
        if not passed:
            issues.append(f"❌ 第一道-闲聊过滤: {reason}")
            score -= 30

        # ===== 第二道：内容选题识别 =====
        result = self.classifier.classify(text, source="article")
        is_content = self.classifier.should_enter_pool(result)
        checks["is_content"] = is_content
        if not is_content:
            issues.append(f"❌ 第二道-内容识别: 分类为 {result['type']}，非内容选题型")
            score -= 25
        else:
            checks["content_type"] = True

        # ===== 第三道：质量校验 =====

        # 字数检查
        word_count = len(re.findall(r'[\u4e00-\u9fff]', text))
        word_count += len(re.findall(r'[a-zA-Z]+', text))
        checks["word_count"] = word_count >= self.MIN_WORD_COUNT
        if not checks["word_count"]:
            issues.append(f"❌ 字数不足: {word_count} < {self.MIN_WORD_COUNT}")
            score -= 15
        else:
            score += 5

        # 标题含关键词
        title_match = re.search(r'<title>(.*?)</title>', content, re.DOTALL)
        title_text = title_match.group(1).strip() if title_match else ""
        checks["has_title"] = bool(title_text)
        if not checks["has_title"]:
            issues.append("❌ 缺少 <title> 标签")
            score -= 20

        # 元描述
        desc_match = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', content)
        desc_text = desc_match.group(1) if desc_match else ""
        checks["has_meta_desc"] = bool(desc_text) and len(desc_text) > 20
        if not checks["has_meta_desc"]:
            issues.append("❌ 缺少有效 meta description（需 >20 字符）")
            score -= 10

        # 内链数量
        internal_links = re.findall(r'href="(/[^"]*\.html)"', content)
        internal_links += re.findall(r"href='(/[^']*\.html)'", content)
        checks["internal_links"] = len(internal_links) >= self.MIN_INTERNAL_LINKS
        if not checks["internal_links"]:
            warnings.append(f"⚠️ 内链不足: {len(internal_links)} < {self.MIN_INTERNAL_LINKS}")
            score -= 5

        # 空壳段落检测
        h2_matches = re.findall(r'<h2[^>]*>(.*?)</h2>', content)
        for h2 in h2_matches:
            h2_clean = re.sub(r'<[^>]+>', '', h2).strip()
            if h2_clean:
                # 检查这个 h2 后面有没有实质内容
                h2_pos = content.find(h2)
                after_h2 = content[h2_pos + len(h2):h2_pos + len(h2) + 500]
                after_text = re.sub(r'<[^>]+>', ' ', after_h2).strip()
                if len(after_text) < 50:
                    issues.append(f"❌ 空壳段落: {h2_clean}")
                    score -= 5

        # 死链检测（检查内部链接指向的文件是否存在）
        for link in internal_links:
            link_path = os.path.join(self.site_dir, link.lstrip("/"))
            if not os.path.exists(link_path):
                warnings.append(f"⚠️ 死链: {link}")
                score -= 3

        checks["no_dead_links"] = len([w for w in warnings if "死链" in w]) == 0

        # 必须元素检查
        for elem in self.REQUIRED_ELEMENTS:
            if elem not in content:
                issues.append(f"❌ 缺少必须元素: {elem}")
                score -= 5

        # ===== 第四道：门禁决策 =====
        # 有 issue 就不给过
        passed = len(issues) == 0

        # 自动备份
        backup_path = None
        if passed:
            backup_path = self._backup(article_path, content)

        return GuardResult(
            passed=passed,
            article_path=article_path,
            checks=checks,
            issues=issues,
            warnings=warnings,
            score=max(0, min(100, score)),
            backup_path=backup_path,
        )

    def _backup(self, article_path: str, content: str) -> str:
        """备份当前版本"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(article_path)
        backup_name = f"{os.path.splitext(filename)[0]}_{timestamp}.html"
        backup_path = os.path.join(self.backup_dir, backup_name)
        with open(backup_path, "w", encoding="utf-8") as f:
            f.write(content)
        return backup_path

    def check_all_articles(self) -> List[GuardResult]:
        """检查 articles/ 下所有文章"""
        articles_dir = os.path.join(self.site_dir, "articles")
        results = []
        if os.path.exists(articles_dir):
            for fname in sorted(os.listdir(articles_dir)):
                if fname.endswith(".html"):
                    result = self.check_article(f"articles/{fname}")
                    results.append(result)
        return results

    def generate_report(self, results: List[GuardResult]) -> str:
        """生成门禁报告"""
        lines = [
            "# 🛡️ 质量门禁报告",
            f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            f"检查文章数: {len(results)}",
        ]

        passed_count = sum(1 for r in results if r.passed)
        lines.append(f"✅ 通过: {passed_count}")
        lines.append(f"❌ 未通过: {len(results) - passed_count}")
        lines.append("")

        for r in results:
            icon = "✅" if r.passed else "❌"
            lines.append(f"## {icon} {r.article_path} (得分: {r.score})")
            if r.issues:
                for issue in r.issues:
                    lines.append(f"  {issue}")
            if r.warnings:
                for warn in r.warnings:
                    lines.append(f"  {warn}")
            if r.backup_path:
                lines.append(f"  💾 已备份: {r.backup_path}")
            lines.append("")

        return "\n".join(lines)


# ===== 命令行 =====
if __name__ == "__main__":
    import sys

    guard = ContentGuard(site_dir=os.path.dirname(__file__) or ".")

    if len(sys.argv) > 1:
        # 检查指定文章
        results = [guard.check_article(sys.argv[1])]
    else:
        # 检查所有文章
        results = guard.check_all_articles()

    report = guard.generate_report(results)
    print(report)

    # 保存报告
    report_path = os.path.join(os.path.dirname(__file__) or ".", "guard_report.md")
    with open(report_path, "w") as f:
        f.write(report)

    # Exit code: 0=全通过 1=有未通过
    all_passed = all(r.passed for r in results)
    sys.exit(0 if all_passed else 1)
