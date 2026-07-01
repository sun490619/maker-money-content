#!/usr/bin/env python3
"""
意图分类器 ContentClassifier
多维打分：内容选题型 vs 工具型 vs 垃圾
只放行"内容选题型"进入选题池
"""

import json
import re
from typing import Dict, List, Tuple


class ContentClassifier:
    """意图分类器：判断一条需求信号属于哪种类型"""

    # 内容选题型特征词（强信号）
    CONTENT_SIGNALS = [
        # 中文教程/方法类
        "怎么", "如何", "教程", "指南", "方法", "步骤", "经验", "心得",
        "入门", "进阶", "实战", "案例", "拆解", "分析",
        "推荐", "对比", "测评", "排行", "榜单", "best", "top",
        "搞钱", "赚钱", "副业", "变现", "收入", "利润",
        "定价", "策略", "思路", "技巧", "秘诀",
        # 英文教程/方法类
        "how to", "tutorial", "guide", "beginner", "tips", "tricks",
        "review", "comparison", "vs", "best of", "top 10",
        "workflow", "strategy", "framework", "playbook",
    ]

    # 工具型特征词（这类需求是要工具，不是要文章）
    TOOL_SIGNALS = [
        "工具", "tool", "app", "软件", "平台", "网站",
        "github.com", "npm", "pypi", "chrome extension",
        "下载", "安装", "download", "install",
        "开源", "open source", "免费工具", "free tool",
        "生成器", "generator", "checker", "检测器",
        "saas", "API", "CLI",
    ]

    # 垃圾信号词（闲聊/无意义）
    GARBAGE_SIGNALS = [
        "哈哈", "笑死", "牛逼", "卧槽", "绝了",
        "今天天气", "吃什么", "好无聊",
        "转发", "抽奖", "点赞", "关注",
        "lol", "lmao", "wtf", "omg",
    ]

    def __init__(self):
        self.stats = {"content": 0, "tool": 0, "garbage": 0, "total": 0}

    def classify(self, text: str, source: str = "", meta: Dict = None) -> Dict:
        """
        分类一条需求信号
        返回: {
            "type": "content" | "tool" | "garbage",
            "confidence": 0.0-1.0,
            "scores": {各维度得分},
            "reason": "分类原因",
            "keywords": [提取的关键词]
        }
        """
        text_lower = text.lower()
        self.stats["total"] += 1

        scores = {"content": 0.0, "tool": 0.0, "garbage": 0.0}

        # ---- 内容选题型打分 ----
        for signal in self.CONTENT_SIGNALS:
            if signal.lower() in text_lower:
                scores["content"] += 1.5

        # 标题特征（问句、数字列表、对比）
        if re.search(r'[？?]', text):
            scores["content"] += 1.0  # 问句倾向内容
        if re.search(r'\d+\s*(个|款|种|条|大|步)', text):
            scores["content"] += 1.0  # 数字列表
        if re.search(r'(\d{4})\s*年', text):
            scores["content"] += 1.0  # 年份标注

        # ---- 工具型打分 ----
        for signal in self.TOOL_SIGNALS:
            if signal.lower() in text_lower:
                scores["tool"] += 1.5

        # 纯链接
        if re.search(r'^https?://', text.strip()):
            scores["tool"] += 2.0

        # ---- 垃圾打分 ----
        for signal in self.GARBAGE_SIGNALS:
            if signal.lower() in text_lower:
                scores["garbage"] += 2.0

        # 纯表情/纯符号
        if len(re.sub(r'[\w\s]', '', text)) > len(text) * 0.3:
            scores["garbage"] += 2.0

        # 纯英文短句且无内容信号
        if len(text) < 50 and scores["content"] == 0 and scores["tool"] == 0:
            scores["garbage"] += 1.0

        # 如果 meta 里有 filter 的 content_score，加权
        if meta and "content_score" in meta:
            scores["content"] += meta["content_score"] * 0.5

        # ---- 决定最终类型 ----
        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]
        total_score = sum(scores.values()) or 1
        confidence = max_score / max(total_score, 1)

        # 兜底：如果所有分数都很低，判垃圾
        if max_score < 1.0:
            max_type = "garbage"
            confidence = 0.5

        self.stats[max_type] += 1

        # 提取关键词
        keywords = self._extract_keywords(text)

        return {
            "type": max_type,
            "confidence": round(confidence, 3),
            "scores": scores,
            "reason": f"最高分维度: {max_type} ({max_score:.1f})",
            "keywords": keywords,
            "source": source,
            "original_text": text[:200],
        }

    def _extract_keywords(self, text: str) -> List[str]:
        """简单提取关键词"""
        keywords = []
        # 提取 2-4 字的中文词
        chinese_words = re.findall(r'[\u4e00-\u9fff]{2,4}', text)
        # 去重 + 去常见停用词
        stopwords = {"这个", "那个", "可以", "什么", "怎么", "一个", "没有", "还是", "不是", "因为", "所以"}
        seen = set()
        for w in chinese_words:
            if w not in stopwords and w not in seen:
                keywords.append(w)
                seen.add(w)
        return keywords[:10]

    def should_enter_pool(self, result: Dict) -> bool:
        """判断是否应该进入选题池"""
        return result["type"] == "content" and result["confidence"] >= 0.3

    def get_stats(self) -> Dict:
        return self.stats


# ===== 命令行测试 =====
if __name__ == "__main__":
    cc = ContentClassifier()

    test_cases = [
        ("Notion 模板怎么定价才能卖出去？分享我的实战经验", "reddit"),
        ("github.com/xxx/awesome-tools 一个开源工具合集", "github"),
        ("哈哈笑死我了这个视频", "v2ex"),
        ("2026年最好的AI写作工具对比：ChatGPT vs Claude vs DeepSeek", "devto"),
        ("免费领取限时优惠券，点击链接", "reddit"),
        ("How to make money with Gumroad in 2026", "reddit"),
        ("Show HN: I built a CLI tool for managing dotfiles", "hackernews"),
        ("零成本启动的20个副业创意", "v2ex"),
    ]

    for text, source in test_cases:
        result = cc.classify(text, source=source)
        enter = "🎯选题池" if cc.should_enter_pool(result) else "🗑️丢弃"
        print(f"{enter} [{result['type']}] conf={result['confidence']}")
        print(f"  {text[:80]}")
        print(f"  keywords: {result['keywords']}")
        print()

    print(f"📊 统计: {json.dumps(cc.get_stats(), ensure_ascii=False)}")
