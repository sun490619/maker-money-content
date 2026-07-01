#!/usr/bin/env python3
"""
闲聊过滤器 ChatterFilter
挡掉新闻、八卦、广告、招聘帖，只放行纯内容信号
"""

import re
import json
from typing import Dict, Optional, Tuple


class ChatterFilter:
    """闲聊过滤器：正则 + 关键词 挡掉非内容信号"""

    # ===== 一级拦截：硬规则（直接挡掉，不给过） =====

    # 新闻/政治/八卦类关键词
    NEWS_GOSSIP_KEYWORDS = [
        "特朗普", "拜登", "习近平", "普京", "总统", "选举", "大选",
        "战争", "冲突", "导弹", "军事", "军队",
        "地震", "台风", "洪水", "灾难",
        "离婚", "出轨", "绯闻", "恋情", "八卦",
        "比特币", "以太坊", "加密货币", "炒币暴富", "百倍币",
        "彩票", "赌博", "赌场",
        "维权", "举报", "投诉", "曝光",
        "车祸", "杀人", "枪击", "死亡", "尸体",
    ]

    # 广告/推广类关键词
    AD_KEYWORDS = [
        "限时优惠", "免费领取", "点击领取", "立即抢购", "秒杀",
        "加微信", "加我微信", "私信我", "联系我", "V我",
        "招代理", "招代理", "兼职日结", "在家赚钱", "手机赚钱",
        "注册送", "邀请码", "推广链接", "affiliate link",
        "sponsored", "硬广", "推广链接", "广告投放",
    ]

    # 招聘/求职类关键词
    JOB_KEYWORDS = [
        "招聘", "求职", "找工作", "招人", "内推", "实习生",
        "薪资面议", "急招", "面试题", "投简历", "跳槽涨薪",
        "remote job", "hiring", "looking for",
    ]

    # ===== 二级评分：内容信号强度 =====

    # 高价值内容词（加分）
    HIGH_VALUE_WORDS = [
        "教程", "指南", "怎么", "如何", "方法", "技巧", "经验",
        "工具推荐", "对比", "测评", "实测", "review",
        "工作流", "自动化", "效率", "搞钱", "赚钱", "副业",
        "数字产品", "模板", "notion", "gumroad",
        "tutorial", "guide", "how to", "best", "vs",
    ]

    # 工具型信号词（不是内容站要的，但不挡掉，交给 classifier 判断）
    TOOL_SIGNAL_WORDS = [
        "工具", "tool", "app", "软件", "网站", "平台",
        "github", "开源", "open source", "下载",
    ]

    def __init__(self):
        self.blocked_count = 0
        self.passed_count = 0

    def check(self, text: str) -> Tuple[bool, str, Dict]:
        """
        检查一段文本是否是有效内容信号
        返回: (是否放行, 原因, 元数据)
        """
        text_lower = text.lower()

        # --- 第一道：硬规则拦截 ---
        for kw in self.NEWS_GOSSIP_KEYWORDS:
            if kw in text_lower:
                self.blocked_count += 1
                return False, f"闲聊/新闻关键词: {kw}", {"category": "gossip", "matched": kw}

        for kw in self.AD_KEYWORDS:
            if kw in text_lower:
                self.blocked_count += 1
                return False, f"广告/推广关键词: {kw}", {"category": "ad", "matched": kw}

        for kw in self.JOB_KEYWORDS:
            if kw in text_lower:
                self.blocked_count += 1
                return False, f"招聘/求职关键词: {kw}", {"category": "job", "matched": kw}

        # --- 第二道：内容信号评分 ---
        score = 0
        matched_value_words = []
        matched_tool_words = []

        for word in self.HIGH_VALUE_WORDS:
            if word.lower() in text_lower:
                score += 2
                matched_value_words.append(word)

        for word in self.TOOL_SIGNAL_WORDS:
            if word.lower() in text_lower:
                score += 0.5
                matched_tool_words.append(word)

        # 太短的内容可能是垃圾
        if len(text) < 30:
            self.blocked_count += 1
            return False, "文本过短（<30字符）", {"category": "too_short"}

        # 纯链接/纯数字
        link_ratio = len(re.findall(r'https?://', text)) * 20 / max(len(text), 1)
        if link_ratio > 0.5:
            self.blocked_count += 1
            return False, "链接占比过高", {"category": "spam_links"}

        # 全是英文大写（可能是垃圾）
        upper_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        if upper_ratio > 0.7 and len(text) > 50:
            self.blocked_count += 1
            return False, "全大写比例过高", {"category": "all_caps"}

        self.passed_count += 1
        return True, "ok", {
            "content_score": score,
            "matched_value_words": matched_value_words,
            "matched_tool_words": matched_tool_words,
            "length": len(text),
        }

    def stats(self) -> Dict:
        return {
            "blocked": self.blocked_count,
            "passed": self.passed_count,
            "pass_rate": round(self.passed_count / max(self.passed_count + self.blocked_count, 1) * 100, 1),
        }


# ===== 命令行测试 =====
if __name__ == "__main__":
    import sys

    cf = ChatterFilter()

    test_cases = [
        "特朗普今天又发推了，引发热议",
        "加我微信xxx，日赚500不是梦",
        "招聘前端工程师，薪资面议",
        "Notion 模板怎么定价才能卖得出去？分享我的实战经验",
        "2026年最好的AI写作工具对比：ChatGPT vs Claude vs DeepSeek",
        "自动化工作流搭建教程：Zapier + Make 实战",
        "https://xxx.com https://yyy.com https://zzz.com",
        "HOW TO MAKE MONEY ONLINE FAST CLICK HERE!!!",
        "hi",
        "Gumroad 新手完全指南：从注册到卖出第一单",
    ]

    for text in test_cases:
        passed, reason, meta = cf.check(text)
        icon = "✅" if passed else "❌"
        print(f"{icon} [{reason}] {text[:60]}...")
        if meta:
            print(f"   meta: {json.dumps(meta, ensure_ascii=False)}")

    print(f"\n📊 统计: {json.dumps(cf.stats(), ensure_ascii=False)}")
