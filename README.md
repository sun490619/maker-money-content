================================================================================
                    搞钱工具箱内容站 — AI启动文件
================================================================================

⚠️ 你是我的专属 AI 助手。读完这个文件，你就知道我是谁、项目是什么、
   代码在哪、我要什么、你要做什么。不用问，直接干。

================================================================================
一、我是谁 & 项目目标
================================================================================

我要建一个内容站，教独立创作者用 AI 工具搞钱。
目标受众：想做副业的人、想用 AI 提效的创作者、想卖数字产品的个体户。

核心理念：不是做一个"工具导航站"，而是做一个"教你搞钱的内容站"。
         用文章教方法，最终目标是打造一个自动化的内容流水线。

================================================================================
二、项目核心架构（这是最重要的，读完你就懂了）
================================================================================

整个项目的运转逻辑是一个闭环流水线：

  需求雷达 → 选题引擎 → AI写作 → 质量门禁 → 人工审核 → 发布 → 数据反馈 → 回灌雷达

每一步解释：

1. 【需求雷达】从 10 个精选免费水源抓取用户需求信号
   - Google Trends RSS：直接反映搜索热度，"Notion 模板怎么卖""Gumroad 教程"到底有没有人在搜
   - Hacker News (Algolia API)：技术圈讨论热点 → 选题信号
   - V2EX API：中文技术社区热门，贴近国内创作者
   - GitHub Trending：什么技术热 → 写"怎么用 XX 搞钱"
   - Dev.to RSS：开发者高质量教程，反映热门方向
   - ProductHunt：新工具层出不穷 → 写"XX 赛道最好的 5 个工具""这个新工具怎么赚钱"
   - Reddit（5 个 subreddit：r/automation, r/productivity, r/SideProject, r/Python, r/selfhosted）
   - HackerNoon RSS：技术博客，常见趋势分析
   - InfoQ RSS：技术新闻/趋势，可引用
   - Lobsters RSS：硬核技术社区，技术趋势
   - ⚠️ 百度热搜、知乎热榜、微博热搜、Wikipedia、arXiv 等不适合内容站的水源不接入
   - 意图分类器判断每条需求是"内容选题型"还是"工具型"还是"垃圾"
   - 垃圾（闲聊/新闻/八卦/招聘）→ 挡掉
   - 工具型 → 不处理（这不是工具站）
   - 内容选题型 → 进入选题池

2. 【选题引擎】把知识型需求转成文章选题
   - 去重（MD5 哈希，避免重复选题）
   - 优先级排序（搜索量大 + 竞争低 = 优先写）
   - 自动建议：标题、关键词、内容大纲

3. 【AI 写作】根据选题自动生成文章初稿
   - 结构：痛点引入 → 方案对比 → 实操步骤 → 避坑指南 → 推荐工具 → 延伸阅读
   - 多模型降级链（省钱自动化）：
     Ollama 本地模型(免费) → Gemini API(免费额度) → DeepSeek V3(¥0.14/百万token) → HuggingFace(免费兜底)
     优先走免费模型，实在不行才花钱，自动降级不用人管

4. 【质量门禁 — 四道防线】发布前自动校验
   第一道 · 闲聊过滤器：挡掉新闻、八卦、广告、招聘帖，纯内容信号才放行
   第二道 · 内容选题识别：判断这是"值得写文章的内容选题"还是"别人已经在卖的工具"
   第三道 · 质量校验：文章长度≥1500字、标题含关键词、有元描述、至少1张封面图、至少3个内链、无死链、无空壳段落（不能只有标题没内容）
   第四道 · 发布门禁脚本（content_guard.py）：不通过的不准发，输出具体问题清单
   - 同时自动备份当前版本到 backups/ 目录，出问题能回滚

5. 【人工审核】通过门禁的文章进入 review_queue
   - 你看一眼，确认发布或打回修改
   - 打回的文章记录原因到错题本

6. 【数据反馈】上线后追踪效果
   - CF Web Analytics + GA4 + GSC + Bing Webmaster 四路数据合并到数据引擎
   - 按文章 URL 拆分：哪篇流量涨、哪篇跳出率高、哪个关键词在爬升
   - 数据回灌选题引擎，指导后续优先写什么
   - GSC 看 Search Performance → 关键词在涨 → 加深度文章
   - GSC 看 Coverage → 有页面没收录 → 修 sitemap 重新提交
   - Bing Webmaster 同步提交 sitemap，看关键词排名

7. 【发布后操作 — CDN 缓存刷新 + 收录推送】
   - 发新文章后自动调用 Cloudflare API 清除该页面缓存
   - sitemap.xml 自动更新（加入新文章 URL）
   - 重要文章手动在 GSC 申请索引（Request Indexing）

8. 【CodeBuddy 定时自动化】
   - 三个定时任务在后台自动跑：
     a) 每小时跑雷达 → 抓取新需求 → 出选题报告
     b) 每天跑站点体检 → 检查所有页面200、死链、文章保鲜度
     c) push 后自动触发部署到 Cloudflare Pages

================================================================================
三、网站当前状态
================================================================================

代码已写好，在 content-site/ 目录下：

 content-site/
 ├── index.html          # 首页（工具目录+文章列表，当前列出 20 个选题，10 篇已写完）
 ├── about.html          # 关于页面
 ├── css/style.css       # 全局样式
 ├── js/main.js          # 交互逻辑（分类过滤）
 ├── js/analytics.js     # 数据统计埋点
 ├── images/             # 图片资源
 ├── sitemap.xml         # 站点地图
 ├── robots.txt          # 爬虫规则
 ├── _headers            # Cloudflare Pages 安全头
 ├── manifest.json       # PWA 配置
 ├── service-worker.js   # 离线缓存
 ├── 404.html            # 404 页面
 ├── articles/           # 文章目录（当前 10 篇已写完）
 │   ├── gumroad-beginner-guide.html
 │   ├── notion-templates-sell-guide.html
 │   ├── digital-product-ideas-2026.html
 │   ├── best-ai-writing-tools-2026.html
 │   ├── free-ai-tools-creators.html
 │   ├── affiliate-marketing-beginner-2026.html
 │   ├── upwork-freelancing-guide.html
 │   ├── notion-setup-workflow.html
 │   ├── automation-tools-no-code.html
 │   └── cloudflare-for-indie-makers.html
 └── README.md           # 项目说明

10 篇文章分类：
  - 数字产品 x3：Gumroad 指南、Notion 模板卖钱、数字产品创意
  - AI 工具 x2：AI 写作工具对比、免费 AI 工具推荐
  - 副业搞钱 x2：Affiliate Marketing 入门、Upwork 接单
  - 效率工具 x3：Notion 工作流、无代码自动化、Cloudflare 全家桶

当前状态：
  ✅ 10 篇文章写完（index.html 与 articles/ 完全对齐）
  ✅ SEO 基础做好（meta、OG、结构化数据、sitemap）
  ✅ PWA 配置就绪（manifest.json + service-worker.js）
  ✅ 404 页面已创建
  ❌ 域名还没替换（代码里写的 YOUR_DOMAIN 占位符）
  ❌ GitHub 仓库还没建
  ❌ 还没部署到 Cloudflare Pages
  ❌ 自动化流水线还没搭

================================================================================
四、你要帮我做的事（优先级排序）
================================================================================

【第一优先级 — 立即执行】
1. 建 GitHub 仓库
   - gh CLI 已登录（账号 sun490619），有 repo 权限
   - 仓库名建议：maker-money-content
   - 把 content-site/ 推上去

2. 替换域名
   - 所有文件中搜 YOUR_DOMAIN，替换成实际域名
   - 域名：等我告诉你（或者你先用 maker-money.pages.dev 占位）
   - 需要替换的地方：OG 标签、canonical URL、sitemap、结构化数据、PWA manifest

3. 部署到 Cloudflare Pages
   - 连接 GitHub 仓库
   - 构建命令：不需要（纯静态）
   - 输出目录：content-site/
   - 自定义域名（等我买了再配）

【第二优先级 — 搭建自动化流水线】
4. 写闲聊过滤器 content_filter.py
   - ChatterFilter 类：正则 + 关键词挡掉新闻/八卦/广告/招聘
   - 纯内容信号才放行

5. 写意图分类器 content_classifier.py
   - 多维打分："内容选题型 vs 工具型 vs 垃圾"
   - 内容选题型才进选题池

6. 写选题引擎 content_radar.py
   - 调 content_filter → content_classifier → 选题池
   - 去重（MD5）、排序、输出：{title, keywords, outline, priority, source}

7. 写 AI 调用客户端 ai_client.py
   - 多模型降级链：Ollama(免费)→Gemini(免费)→DeepSeek(极便宜)→HuggingFace(兜底)
   - 自动降级，优先免费模型

8. 写质量门禁 content_guard.py
   - 四道防线：闲聊→选题识别→质量校验→门禁拦截
   - 不通过不准发，输出问题清单
   - 同时自动备份当前版本到 backups/

9. 写文章生产日志 content_log.json
   - 每篇：选题来源、生成时间、质量分、发布状态

10. 写 CDN 缓存刷新 purge_cache.py
    - 发新文章后调 Cloudflare API 清对应页面缓存
    - Zone ID 和 API Token 配在配置文件里

11. 配置 GitHub Actions（三个 workflow）
    - pipeline.yml：定时跑雷达 → 出选题建议 → 发 Issue
    - health-check.yml：定时跑站点体检
    - deploy.yml：push 自动触发 CF Pages 部署

12. 配置 CodeBuddy 定时自动化（三个任务）
    - 每小时跑雷达抓新需求
    - 每天跑站点体检
    - push 后自动部署

【第三优先级 — 运营基础设施】
13. 做站点体检脚本 content_health_check.py
    - 检查所有页面 HTTP 状态 + 死链
    - 文章保鲜度（超 90 天🟡 超 180 天🔴）
    - sitemap 完整性 + 死链检测
    - exit code：0=全绿 1=警告 2=严重

14. 做数据引擎 content_engine.py
    - 合并 CF + GA4 + GSC + Bing 四路数据
    - 按文章 URL 拆分：哪篇流量涨、跳出率高、关键词爬升

15. 做运营看板 content_dashboard.html
    - 选题池 + 待审核文章 + 各文章流量数据 + 站点健康

16. 建内容错题本 mistake_book.json
    - 哪些选题没流量、哪些标题点击率低 → 驱动优化

【第四优先级 — 增强功能】
17. 文章保鲜度自动监控 + 自动备份系统
18. 自动内链网络（新文章自动匹配 3 篇相关旧文章）
19. 竞品监控（雷达水源监控同类 → 发现爆款 → 标记跟进）
20. 一鱼多吃（文章摘要→Twitter/X帖子，要点→小红书/即刻，自动OG图片）

================================================================================
五、内容优先级策略（SEO 思路）
================================================================================

1. 长尾优先：先写搜索量小但精准的长尾关键词
   例子：不写"AI 工具"（竞争太大），写"Notion 模板怎么做才能卖出去"

2. 爬坡到首部：长尾文章多了 → 网站权重提升 → 再写热门关键词

3. 分类侧重：
   第一梯队 🔥：AI 工具赚钱、副业搞钱方法
   第二梯队 🟡：自动化效率、推荐合集
   第三梯队 🟢：案例拆解、个体户访谈

================================================================================
六、设计原则（所有决策的依据）
================================================================================

1. 自动化优先：能自动的绝不手动。雷达选题 → AI 写作 → 门禁检查 → 自动部署
2. 数据驱动：选题不是拍脑袋，从雷达数据中来
3. 质量兜底：宁可发得慢，不能不审核就直接发
4. 可追溯：CHANGELOG + 生产日志 + 错题本，所有改动都有记录
5. 你只做决策：代码、部署、内容初稿全是我的活，你只看最终要不要发

================================================================================
七、自动化脚本生态（每个脚本做什么）
================================================================================

content_radar.py          → 需求雷达：从 10 个水源抓取 → 闲聊过滤 → 意图分类 → 选题池
content_filter.py          → 闲聊过滤器 ChatterFilter 类：挡新闻/八卦/广告/招聘
content_classifier.py      → 意图分类器：多维打分，"内容选题型 vs 工具型 vs 垃圾"
content_guard.py           → 四道质量防线 + 自动备份，不通过不准发
content_health_check.py    → 站点体检：HTTP 状态 + 死链 + 文章保鲜度 + sitemap 完整性
                             exit code 0=全绿 1=警告 2=严重🔴
purge_cache.py             → Cloudflare CDN 缓存刷新：发新文章后自动清对应页面缓存
content_backup.py          → 发布前自动备份到 backups/，JSON 格式，出问题可回滚
content_engine.py          → 数据引擎：合并 CF + GA4 + GSC + Bing 四路数据，按文章 URL 拆分
ai_client.py               → AI 调用客户端：多模型降级链 Ollama→Gemini→DeepSeek→HuggingFace
content_dashboard.html     → 运营看板：选题池 + 待审核 + 各文章流量 + 站点健康
review_queue.json          → 审核队列状态机：pending → reviewed → published
mistake_book.json          → 错题本：哪些选题没流量、哪些标题点击率低
content_log.json           → 生产日志：选题来源→生成时间→质量分→发布状态→流量数据

八、外部服务怎么接（全部免费额度足够用）
================================================================================

Cloudflare Pages：
  - 连接 GitHub 仓库自动部署，_headers 配安全头（CSP、HSTS）
  - API Token 需 Zone:Cache Purge 权限（清缓存用）

Google Search Console (GSC)：
  - 验证域名 → 提交 sitemap.xml
  - 重要文章手动 Request Indexing 加速收录
  - Search Performance → 关键词涨了 → 选题引擎标"跟进"
  - Coverage → 哪个页面没收录 → 修 sitemap 重提

Google Analytics 4 (GA4)：
  - Measurement ID 嵌入所有页面 <head>

Bing Webmaster：
  - 提交 sitemap，可导入 GSC 数据

GitHub Actions（三个 workflow）：
  1. pipeline.yml —— 定时跑 radar → 出选题 → 发 GitHub Issue
  2. health-check.yml —— 定时跑体检 → 出报告
  3. deploy.yml —— push main → 自动触发 CF Pages 部署

九、技术栈
================================================================================

- 前端：纯 HTML/CSS/JS（无框架），PWA 离线支持
- 部署：Cloudflare Pages
- 版本控制：GitHub（sun490619/maker-money-content）
- 自动化：GitHub Actions + CodeBuddy 定时任务
- 数据：CF Web Analytics + GA4 + GSC + Bing Webmaster
- 脚本：Python 3
- 域名：待购买，先用 maker-money.pages.dev 占位

================================================================================
十、会话开始时你需要做的事（Checklist）
================================================================================

□ 先 read_file content-site/ 目录看现有代码
□ 确认域名（问我，或先用 maker-money.pages.dev）
□ gh repo create 建仓库（如还没建）
□ 替换所有 YOUR_DOMAIN 占位符
□ git init → commit → push
□ 连接 Cloudflare Pages 部署
□ 写 content_filter.py（闲聊过滤器）
□ 写 content_classifier.py（意图分类器）
□ 写 content_radar.py（选题引擎，调 filter + classifier）
□ 写 ai_client.py（多模型降级链）
□ 写 content_guard.py（质量门禁 + 自动备份）
□ 写 CHANGELOG.md 第一时间开始记录
□ 配置 GitHub Actions（pipeline + health-check + deploy）
□ 配置 CodeBuddy 定时自动化
□ 写 purge_cache.py（CDN 缓存刷新）
□ 写 content_health_check.py（站点体检）

================================================================================
十一、关键提醒
================================================================================

- 这个项目的灵魂是"自动化流水线"，不是"一堆静态页面"
- 10 篇文章只是起点，真正的产出物是那条自动选题→写作→发布的链
- 所有脚本写完后都在 GitHub Actions 里跑起来，不靠手动
- 我不是程序员，我不写代码，所有代码你来写
- 我只做决策：买域名、审核文章、确认发布
- 遇到需要我决策的事情，总结清楚让我选
- 不要废话，直接开干

================================================================================
                           文件结束
================================================================================
