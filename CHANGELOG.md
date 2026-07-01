# 搞钱工具箱 — 更新日志

## v1.0 — 2026-07-01

### 🚀 初始上线
- 10 篇原创文章：数字产品、AI 工具、副业搞钱、效率工具四大分类
- 首页：文章列表 + 分类筛选 + 暗色模式
- 关于页面
- 404 页面

### 🤖 自动化流水线脚本
- `content_filter.py`：闲聊过滤器，正则+关键词挡掉新闻/广告/招聘
- `content_classifier.py`：意图分类器，多维打分区分内容/工具/垃圾
- `content_radar.py`：需求雷达+选题引擎，从 10 个水源抓取→过滤→分类→选题池
- `ai_client.py`：多模型降级链 Ollama→Gemini→DeepSeek→HuggingFace
- `content_guard.py`：四道质量门禁（闲聊→选题识别→质量校验→门禁拦截）+自动备份
- `content_health_check.py`：站点体检（页面状态+死链+保鲜度+sitemap+SEO）
- `purge_cache.py`：Cloudflare CDN 缓存刷新

### 🔍 SEO 基础
- 所有页面含 meta description、OG 标签、结构化数据
- sitemap.xml、robots.txt
- _headers（CSP、HSTS、缓存策略）
- PWA 支持（manifest.json、service-worker.js）

### 📋 待办
- 域名替换（YOUR_DOMAIN → 实际域名）
- 部署到 Cloudflare Pages
- 配置 GitHub Actions（pipeline + health-check + deploy）
- 配置 CodeBuddy 定时自动化
- GSC + GA4 + Bing Webmaster 接入
