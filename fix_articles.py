#!/usr/bin/env python3
"""Fix all 10 article pages to v1.3 standard: English default + Lucide icons + i18n + language switch"""

import os, re, json

ARTICLES_DIR = os.path.dirname(os.path.abspath(__file__)) + '/articles'
I18N_FILE = os.path.dirname(os.path.abspath(__file__)) + '/js/i18n.js'

# Category English labels (matching i18n.js en values)
CAT_EN_LABELS = {
    "cat.digital": "Digital Products",
    "cat.ai": "AI Tools",
    "cat.sidehustle": "Side Hustles",
    "cat.productivity": "Productivity",
}

# Standard v1.3 nav
V13_NAV = '''<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand"><i data-lucide="dollar-sign" class="icon-brand"></i> Maker Earn</a>
    <div class="nav-links">
      <a href="/#articles" data-i18n="nav.articles">Articles</a>
      <a href="/about.html" data-i18n="nav.about">About</a>
      <button class="lang-switch" id="lang-switch" aria-label="Switch language">中文</button>
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme"><i data-lucide="moon"></i></button>
    </div>
  </div>
</nav>'''

V13_FOOTER = '''<footer class="footer">
  <p data-i18n="footer.copyright">© 2026 Maker Earn · Helping indie creators build independent income</p>
  <div class="footer-links">
    <a href="/" data-i18n="nav.articles">Articles</a>
    <a href="/sitemap.xml" data-i18n="footer.sitemap">Sitemap</a>
  </div>
</footer>

<script src="https://unpkg.com/lucide@latest"></script>
<script src="/js/i18n.js"></script>
<script src="/js/main.js"></script>'''

# Article body translations (Chinese kept as-is from original)
ARTICLE_BODY_ZH = {}

# ---- Article data: (filename, lucide_cat_icon, cat_i18n_key, title_i18n_key, readtime_i18n_key, date_i18n_key, english_title, readtime_en, date_en, body_key, english_body_html) ----

articles = [
    ("gumroad-beginner-guide.html", "package", "cat.digital",
     "article.gumroad.title", "article.gumroad.readtime", "article.gumroad.date",
     "Gumroad Beginner's Guide: From Signup to First Sale", "12 min read", "2026-06-30",
     "article.gumroad.body",
     # Chinese body (original)
     '''<p>Gumroad 是目前最流行的数字产品销售平台。不管你想卖电子书、Notion 模板、设计素材还是在线课程，Gumroad 都能帮你搞定。</p>
    <p>这篇教程从零开始，带你走完整个流程：注册 → 设置 → 上传产品 → 收款 → 卖出第一单。</p>

    <h2>为什么选 Gumroad？</h2>
    <p>跟其他平台比，Gumroad 有三个核心优势：</p>
    <ul>
      <li><strong>零门槛</strong>：不需要营业执照，不需要公司，个人就能注册</li>
      <li><strong>品类不限</strong>：电子书、模板、预设、课程、代码、设计源文件…… 只要是数字文件都能卖</li>
      <li><strong>自带支付</strong>：支持信用卡、PayPal，买家付款直接到你账户</li>
    </ul>
    <p>费率方面：免费版收 10% 佣金，付费版（$10/月）只收 2.9% + 30¢ 交易费。如果你月销超过 $100，建议直接上付费版，算下来更划算。</p>

    <h2>第一步：注册 Gumroad 账号</h2>
    <p>去 <a href="https://gumroad.com" target="_blank" rel="nofollow">gumroad.com</a> 点 Sign Up，用 Google 账号或邮箱注册即可。注册后需要设置：</p>
    <ol>
      <li><strong>个人资料</strong>：头像、Bio（用一句话说清楚你卖什么）、社交媒体链接</li>
      <li><strong>支付设置</strong>：绑定 Stripe（用于收款）。中国大陆用户需要注册 Stripe Atlas 或用其他方式，这点后面单独说</li>
      <li><strong>URL 自定义</strong>：把默认的一串数字改成你的名字，比如 gumroad.com/你的名字</li>
    </ol>

    <h2>第二步：创建第一个产品</h2>
    <p>点 Products → New Product，你会看到这些选项：</p>
    <ul>
      <li><strong>产品名称</strong>：清晰直接比花哨重要。比如"Notion 项目管理模板"比"终极效率神器"好一百倍</li>
      <li><strong>价格</strong>：新手建议从 $5-$15 起步，低价好卖、积累评价</li>
      <li><strong>描述</strong>：用买家视角写——"你会得到什么"、"能解决什么问题"、"包含哪些文件"</li>
      <li><strong>封面图</strong>：1600×840 像素，干净专业</li>
      <li><strong>文件上传</strong>：支持 ZIP、PDF、图片等多种格式</li>
    </ul>

    <h2>第三步：定价策略</h2>
    <p>Gumroad 提供的定价选项很灵活：</p>
    <ul>
      <li><strong>固定价格</strong>：适合大多数产品</li>
      <li><strong>买家自主定价</strong>：设一个最低价，让买家自己加价（适合粉丝经济）</li>
      <li><strong>分期付款</strong>：高价产品（$100+）可以分 3-6 期</li>
      <li><strong>折扣码</strong>：可以创建限时折扣，促进销售</li>
    </ul>
    <p>一个很有效的策略：<strong>设置两个版本</strong>。基础版 $9，完整版 $19。很多人会选中间的。这叫"锚定效应"。</p>

    <h2>第四步：如何推广</h2>
    <p>产品上架只是开始，没人知道你的产品存在才是最大的问题。几种实用推广方式：</p>
    <ol>
      <li><strong>社交媒体</strong>：在 Twitter/X、Reddit 相关子版块分享你的产品故事和使用场景</li>
      <li><strong>写教程文章</strong>：写一篇跟你的产品相关的教程（比如你现在读的这篇），文末放产品链接</li>
      <li><strong>Product Hunt 发布</strong>：数字工具类产品的最佳冷启动渠道</li>
      <li><strong>建立邮件列表</strong>：用 Gumroad 自带的邮件功能收集买家邮箱，新品直接推</li>
    </ol>

    <h2>常见问题</h2>
    <h3>中国大陆用户怎么收款？</h3>
    <p>Gumroad 默认用 Stripe 收款，Stripe 目前不完全支持中国大陆个人用户。你可以：注册一家美国公司（通过 Stripe Atlas）、用香港 Stripe 账号、或者通过 Payoneer 中转。</p>

    <h3>需要交税吗？</h3>
    <p>Gumroad 会自动代收代缴欧盟 VAT。美国用户需要填写 W-9 表格（报税用）。具体建议咨询会计师。</p>''',
     # English body
     '''<p>Gumroad is the most popular digital product sales platform. Whether you want to sell ebooks, Notion templates, design assets, or online courses, Gumroad has you covered.</p>
    <p>This tutorial walks you through the entire process: signup → setup → upload product → accept payment → make your first sale.</p>

    <h2>Why Choose Gumroad?</h2>
    <p>Compared to other platforms, Gumroad has three core advantages:</p>
    <ul>
      <li><strong>Zero barrier to entry</strong>: No business license, no company required — individuals can register</li>
      <li><strong>No category restrictions</strong>: Ebooks, templates, presets, courses, code, design source files — any digital file can be sold</li>
      <li><strong>Built-in payments</strong>: Supports credit cards and PayPal, payments go directly to your account</li>
    </ul>
    <p>Fee structure: the free plan charges 10% commission, while the paid plan ($10/month) only charges 2.9% + 30¢ per transaction. If you're selling over $100/month, go with the paid plan — the math works out better.</p>

    <h2>Step 1: Sign Up for Gumroad</h2>
    <p>Go to <a href="https://gumroad.com" target="_blank" rel="nofollow">gumroad.com</a> and click Sign Up. Use your Google account or email to register. After signing up, you'll need to set up:</p>
    <ol>
      <li><strong>Profile</strong>: Avatar, bio (one sentence explaining what you sell), social media links</li>
      <li><strong>Payment settings</strong>: Connect Stripe (for receiving payments). Non-US users may need alternative setups — covered separately below</li>
      <li><strong>Custom URL</strong>: Change the default random string to your name, e.g. gumroad.com/yourname</li>
    </ol>

    <h2>Step 2: Create Your First Product</h2>
    <p>Click Products → New Product, and you'll see these options:</p>
    <ul>
      <li><strong>Product name</strong>: Clear and direct beats clever. "Notion Project Management Template" is 100x better than "Ultimate Productivity Powerhouse"</li>
      <li><strong>Price</strong>: Start at $5-$15 as a beginner — low price, easy to sell, build reviews</li>
      <li><strong>Description</strong>: Write from the buyer's perspective — "What you'll get", "What problem this solves", "What files are included"</li>
      <li><strong>Cover image</strong>: 1600×840 pixels, clean and professional</li>
      <li><strong>File upload</strong>: Supports ZIP, PDF, images, and more</li>
    </ul>

    <h2>Step 3: Pricing Strategy</h2>
    <p>Gumroad offers flexible pricing options:</p>
    <ul>
      <li><strong>Fixed price</strong>: Best for most products</li>
      <li><strong>Pay what you want</strong>: Set a minimum price, let buyers add more (great for fan-driven sales)</li>
      <li><strong>Installments</strong>: Higher-priced products ($100+) can be split into 3-6 payments</li>
      <li><strong>Discount codes</strong>: Create time-limited discounts to boost sales</li>
    </ul>
    <p>An effective strategy: <strong>offer two versions</strong>. Basic at $9, Complete at $19. Most people will pick the middle option. This is called "anchoring."</p>

    <h2>Step 4: How to Promote</h2>
    <p>Listing your product is just the beginning. The real challenge is getting people to know it exists. Here are some practical promotion methods:</p>
    <ol>
      <li><strong>Social media</strong>: Share your product story and use cases on Twitter/X and relevant Reddit communities</li>
      <li><strong>Write tutorial articles</strong>: Write a guide related to your product (like the one you're reading now), with a product link at the end</li>
      <li><strong>Product Hunt launch</strong>: The best cold-start channel for digital tool products</li>
      <li><strong>Build an email list</strong>: Use Gumroad's built-in email feature to collect buyer emails and notify them of new products</li>
    </ol>

    <h2>FAQ</h2>
    <h3>How do non-US creators receive payments?</h3>
    <p>Gumroad uses Stripe by default for payments. If Stripe isn't fully available in your country, alternatives include registering a US company (via Stripe Atlas), using a supported-region Stripe account, or routing through Payoneer.</p>

    <h3>Do I need to pay taxes?</h3>
    <p>Gumroad automatically collects and remits EU VAT. US sellers need to fill out a W-9 form. Consult an accountant for specific advice.</p>'''),

    ("notion-templates-sell-guide.html", "package", "cat.digital",
     "article.notion-templates.title", "article.notion-templates.readtime", "article.notion-templates.date",
     "Can You Make Money Selling Notion Templates? Real Income Data for 2026", "10 min read", "2026-06-29",
     "article.notion-templates.body",
     '''<p>"Notion 模板能赚钱？"——两年前我也这么问。现在我可以直接回答：<strong>能，而且收入比你想象的高。</strong></p>

    <h2>Notion 模板市场有多大？</h2>
    <p>Notion 有超过 1 亿用户。2026 年，Notion 模板已经成为一个正经的数字产品品类。Gumroad 上"Notion template"标签下的产品超过 10 万个，头部卖家月入 $5000-$15000。</p>
    <p>关键的转变是：2024 年之前大家只觉得 Notion 是"笔记软件"。现在它已经变成"个人操作系统"——项目管理、CRM、知识库、财务管理，什么都往里塞。功能越多，模板需求越大。</p>

    <h2>哪些模板最好卖？</h2>
    <p>根据 Gumroad 和 Etsy 的销售数据，这 5 类模板最赚钱：</p>

    <h3>1. 个人管理系统（销量王）</h3>
    <p>把任务管理、习惯追踪、目标规划、日记整合到一个 Notion 页面里。类似"Second Brain"概念。这类模板定价 $15-39，头部产品销量 5000+。</p>

    <h3>2. 项目管理模板</h3>
    <p>自由职业者和小团队不想买 Jira/Asana，用 Notion 搭一套项目管理。含任务看板、时间线、甘特图。定价 $9-25。</p>

    <h3>3. 财务管理模板</h3>
    <p>收入支出追踪、发票管理、税务记录。Freelancer 特别喜欢这类。定价 $8-19。</p>

    <h3>4. 学术/学生模板</h3>
    <p>课程表、笔记系统、考试复习计划。学生群体大，单价低但量大。定价 $3-10。</p>

    <h3>5. 内容创作工作流</h3>
    <p>给 YouTuber/Blogger 用的：选题库、脚本管理、发布日历、数据追踪。垂直场景，用户付费意愿强。定价 $12-29。</p>

    <h2>真实收入案例</h2>
    <p>以下来自公开可查的 Gumroad 数据和创作者自曝：</p>
    <ul>
      <li>Second Brain 模板：$39 × 5000+ 销量 = $195,000+（上线两年）</li>
      <li>Freelancer 管理系统：$19 × 1200+ 销量 = $22,800+（一年）</li>
      <li>学生笔记模板包：$12 × 3000+ 销量 = $36,000+（一年半）</li>
      <li>小型项目管理模板：$15 × 800 销量 = $12,000（八个月）</li>
    </ul>

    <h2>做一个好模板需要什么？</h2>
    <p>不需要编程。需要的是：</p>
    <ol>
      <li><strong>深入理解一个场景</strong>：你必须是这个问题的"过来人"。做学生模板，你得是学生；做 Freelancer 模板，你得接过单</li>
      <li><strong>Notion 熟练度</strong>：数据库关系、公式、自动化、不同的视图——这些基础操作要熟</li>
      <li><strong>审美</strong>：丑的模板卖不动。颜色协调、排版干净、信息层级清晰</li>
    </ol>
    <p>做一个模板 4-8 小时。第一次做长一点，熟了之后 2-3 小时做一个。</p>

    <h2>怎么推广你的模板？</h2>
    <ul>
      <li><strong>Twitter/X 发截图</strong>：展示模板界面 + 使用效果，带上 Notion 社区话题</li>
      <li><strong>Reddit r/Notion</strong>：最有价值的推广渠道，可以发免费版引流</li>
      <li><strong>Product Hunt 发布</strong>：适合有创新性的模板</li>
      <li><strong>做免费版引流</strong>：免费版给基础功能，Pro 版解锁高级功能</li>
    </ul>''',
     '''<p>"Can you really make money selling Notion templates?" — I asked the same question two years ago. Now I can answer directly: <strong>Yes, and the income is higher than you'd expect.</strong></p>

    <h2>How Big Is the Notion Template Market?</h2>
    <p>Notion has over 100 million users. By 2026, Notion templates have become a legitimate digital product category. There are over 100,000 products tagged "Notion template" on Gumroad, with top sellers earning $5,000-$15,000 per month.</p>
    <p>The key shift: before 2024, people just thought of Notion as "note-taking software." Now it's become a "personal operating system" — project management, CRM, knowledge base, finance tracking — everything goes in. The more features, the greater the template demand.</p>

    <h2>Which Templates Sell Best?</h2>
    <p>Based on Gumroad and Etsy sales data, these 5 categories earn the most:</p>

    <h3>1. Personal Management System (Best Seller)</h3>
    <p>Combines task management, habit tracking, goal planning, and journaling into a single Notion page. Think "Second Brain." These templates are priced at $15-39, with top products selling 5,000+ copies.</p>

    <h3>2. Project Management Templates</h3>
    <p>Freelancers and small teams who don't want to pay for Jira/Asana build project management in Notion. Includes task boards, timelines, Gantt charts. Priced $9-25.</p>

    <h3>3. Finance Management Templates</h3>
    <p>Income/expense tracking, invoice management, tax records. Freelancers especially love this category. Priced $8-19.</p>

    <h3>4. Academic/Student Templates</h3>
    <p>Course schedules, note systems, exam review plans. Large student audience, low unit price but high volume. Priced $3-10.</p>

    <h3>5. Content Creation Workflows</h3>
    <p>For YouTubers and bloggers: topic library, script management, publishing calendar, data tracking. Vertical niche with strong willingness to pay. Priced $12-29.</p>

    <h2>Real Income Case Studies</h2>
    <p>From publicly available Gumroad data and creator disclosures:</p>
    <ul>
      <li>Second Brain template: $39 × 5,000+ sales = $195,000+ (two years live)</li>
      <li>Freelancer management system: $19 × 1,200+ sales = $22,800+ (one year)</li>
      <li>Student note template bundle: $12 × 3,000+ sales = $36,000+ (18 months)</li>
      <li>Small project management template: $15 × 800 sales = $12,000 (8 months)</li>
    </ul>

    <h2>What Do You Need to Make a Great Template?</h2>
    <p>No coding required. What you need:</p>
    <ol>
      <li><strong>Deep understanding of a specific workflow</strong>: You must have lived the problem. Making a student template? You need to have been a student. Making a freelancer template? You need to have worked with clients</li>
      <li><strong>Notion proficiency</strong>: Database relations, formulas, automations, different views — you need to know the fundamentals</li>
      <li><strong>Design sense</strong>: Ugly templates don't sell. Consistent colors, clean layout, clear information hierarchy</li>
    </ol>
    <p>Making a template takes 4-8 hours. Longer the first time, down to 2-3 hours once you're experienced.</p>

    <h2>How to Promote Your Templates</h2>
    <ul>
      <li><strong>Post screenshots on Twitter/X</strong>: Show the template interface + results, tag Notion community hashtags</li>
      <li><strong>Reddit r/Notion</strong>: The most valuable promotion channel — share a free version as a lead magnet</li>
      <li><strong>Product Hunt launch</strong>: Great for innovative templates</li>
      <li><strong>Free version lead gen</strong>: Free version with basic features, Pro version unlocks advanced functionality</li>
    </ul>'''),

    ("digital-product-ideas-2026.html", "package", "cat.digital",
     "article.ideas.title", "article.ideas.readtime", "article.ideas.date",
     "15 Most Profitable Digital Product Ideas for 2026", "8 min read", "2026-06-28",
     "article.ideas.body",
     '''<p>想做数字产品但不知道卖什么？这是最常见的卡点。好消息是：你不需要发明什么新东西，已经有无数人在这些方向上赚到钱了。</p>

    <h2>入门级（适合新手，门槛低）</h2>

    <h3>1. Notion 模板</h3>
    <p>2026 年最热门的数字产品之一。项目管理、习惯追踪、财务管理、读书笔记——任何一个场景都能做成模板。价格 $5-$30，制作时间 2-4 小时。真实案例：有人在 Gumroad 上靠 3 个 Notion 模板月入 $2000+。</p>

    <h3>2. Canva 模板</h3>
    <p>社交媒体帖子、简历、PPT、海报。Canva 有 1.5 亿用户，模板需求巨大。做一套 10 个 Instagram 模板卖 $8，很多人愿意买。</p>

    <h3>3. 电子书（短篇）</h3>
    <p>不需要写 300 页。30-50 页的"微电子书"反而更好卖——价格低（$3-9）、决策成本低、读者读完概率高。选题要窄：比如"Upwork 写手 Proposal 模板 20 个"，不要"如何做自由职业"。</p>

    <h3>4. Checklist / PDF 清单</h3>
    <p>最简单的数字产品。比如"SEO 上手指南 Checklist"、"远程办公装备清单"。1-2 页 PDF，卖 $1-3，制作 30 分钟。单个利润虽低，但量大。</p>

    <h3>5. 社交媒体内容日历</h3>
    <p>很多小企业主需要规划社交媒体内容但不知道怎么做。你做一个 30 天内容日历模板（Google Sheets + PDF），卖 $7-12。</p>

    <h2>进阶级（需要一定技能）</h2>

    <h3>6. 预设包（Lightroom / Figma / VS Code）</h3>
    <p>摄影师需要 Lightroom 预设，设计师需要 Figma 插件/组件库，程序员需要 VS Code 主题/配置包。做一个高质量预设包，定价 $15-35，复购率高。</p>

    <h3>7. 在线迷你课程</h3>
    <p>不是 Udemy 那种 10 小时的课。30-60 分钟的"微课程"，解决一个具体问题。比如"30 分钟学会用 AI 做 PPT"。定价 $15-29。</p>

    <h3>8. 字体 / 图标包</h3>
    <p>手写字体、手绘图标、定制 emoji——设计师和内容创作者永远需要这些素材。做一套 50 个图标，卖 $10-20。</p>

    <h3>9. 网站/App 模板</h3>
    <p>Next.js 模板、Framer 模板、Webflow 模板。前期投入大（做一套好模板可能要 2 周），但定价高（$29-79），且可重复卖。</p>

    <h3>10. 电子表格模板</h3>
    <p>财务预算表、项目管理表、客户 CRM 表。Google Sheets/Excel 模板永远有市场。定价 $5-20。</p>

    <h2>高级（需要专业能力）</h2>

    <h3>11. SaaS 微工具</h3>
    <p>一个小功能工具（比如 Chrome 插件、Figma 插件），一次性付费或免费+付费版。开发周期 1-4 周，但成功后是真正的被动收入。</p>

    <h3>12. 3D 素材 / 模型</h3>
    <p>Web 3D 需求爆发。Blender 模型、Spline 场景、Three.js 组件——供不应求。单个模型 $5-50。</p>

    <h3>13. Prompt 合集</h3>
    <p>AI Prompt Engineering 是一个新兴品类。"100 个 ChatGPT 商业写作 Prompt"、"Midjourney 风格词库 200+"，定价 $5-19。</p>

    <h3>14. 数据报告</h3>
    <p>行业分析报告、市场调研数据。需要花时间做研究，但一份 $49-199 的报告可以反复卖。</p>

    <h3>15. 音频素材包</h3>
    <p>免版税背景音乐、音效包。YouTube 创作者、播客主都需要。定价 $15-49。</p>

    <h2>怎么选？三个判断标准</h2>
    <ol>
      <li><strong>你已有的技能</strong>：会设计→模板，会写作→电子书，会编程→SaaS 微工具</li>
      <li><strong>制作时间</strong>：新手先选 4 小时内能完成的（模板、清单类）</li>
      <li><strong>市场需求</strong>：去 Gumroad 搜一下同类产品，看销量。有人卖就说明有需求</li>
    </ol>''',
     '''<p>Want to create digital products but don't know what to sell? This is the most common roadblock. The good news: you don't need to invent anything new — countless people are already making money in these directions.</p>

    <h2>Beginner Level (Low Barrier to Entry)</h2>

    <h3>1. Notion Templates</h3>
    <p>One of the hottest digital products in 2026. Project management, habit tracking, finance management, reading notes — any workflow can become a template. Price $5-$30, creation time 2-4 hours. Real case: someone earns $2,000+/month on Gumroad with just 3 Notion templates.</p>

    <h3>2. Canva Templates</h3>
    <p>Social media posts, resumes, presentations, posters. Canva has 150 million users and massive template demand. A set of 10 Instagram templates for $8 — plenty of people will buy.</p>

    <h3>3. Ebooks (Short Form)</h3>
    <p>You don't need to write 300 pages. 30-50 page "micro-ebooks" actually sell better — lower price ($3-9), lower decision friction, higher completion rates. Go narrow with your topic: "20 Upwork Proposal Templates for Writers" rather than "How to Freelance."</p>

    <h3>4. Checklists / PDF Documents</h3>
    <p>The simplest digital product. Think "SEO Beginner Checklist" or "Remote Work Setup Checklist." 1-2 page PDF, sell for $1-3, takes 30 minutes to create. Low per-unit profit but scales with volume.</p>

    <h3>5. Social Media Content Calendars</h3>
    <p>Many small business owners need to plan social media content but don't know how. Create a 30-day content calendar template (Google Sheets + PDF), sell for $7-12.</p>

    <h2>Intermediate Level (Requires Some Skill)</h2>

    <h3>6. Preset Packs (Lightroom / Figma / VS Code)</h3>
    <p>Photographers need Lightroom presets, designers need Figma plugins/component libraries, developers need VS Code themes/configs. Make a high-quality preset pack, price $15-35, high repeat purchase rate.</p>

    <h3>7. Online Mini Courses</h3>
    <p>Not the 10-hour Udemy type. 30-60 minute "micro-courses" solving one specific problem. Like "Learn to Make AI Presentations in 30 Minutes." Price $15-29.</p>

    <h3>8. Font / Icon Packs</h3>
    <p>Handwritten fonts, hand-drawn icons, custom emoji — designers and content creators always need these assets. A set of 50 icons for $10-20.</p>

    <h3>9. Website/App Templates</h3>
    <p>Next.js templates, Framer templates, Webflow templates. Higher upfront investment (a good template may take 2 weeks), but premium pricing ($29-79) and you can sell them repeatedly.</p>

    <h3>10. Spreadsheet Templates</h3>
    <p>Budget spreadsheets, project management sheets, client CRM sheets. Google Sheets/Excel templates have an evergreen market. Price $5-20.</p>

    <h2>Advanced Level (Requires Professional Skill)</h2>

    <h3>11. SaaS Micro-Tools</h3>
    <p>A small utility tool (Chrome extension, Figma plugin), sold as one-time purchase or freemium. Development takes 1-4 weeks, but success means true passive income.</p>

    <h3>12. 3D Assets / Models</h3>
    <p>Web 3D demand is exploding. Blender models, Spline scenes, Three.js components — supply can't keep up. Individual models $5-50.</p>

    <h3>13. Prompt Collections</h3>
    <p>AI Prompt Engineering is an emerging category. "100 ChatGPT Business Writing Prompts," "200+ Midjourney Style Keywords." Price $5-19.</p>

    <h3>14. Data Reports</h3>
    <p>Industry analysis reports, market research data. Takes time to research, but a $49-199 report can be sold over and over.</p>

    <h3>15. Audio Asset Packs</h3>
    <p>Royalty-free background music, sound effect packs. YouTube creators and podcasters all need these. Price $15-49.</p>

    <h2>How to Choose? Three Criteria</h2>
    <ol>
      <li><strong>Your existing skills</strong>: Design → templates, Writing → ebooks, Coding → SaaS micro-tools</li>
      <li><strong>Creation time</strong>: Beginners should start with something completable in under 4 hours (templates, checklists)</li>
      <li><strong>Market demand</strong>: Search Gumroad for similar products and check their sales. If people are selling it, there's demand</li>
    </ol>'''),

    ("best-ai-writing-tools-2026.html", "bot", "cat.ai",
     "article.ai-writing.title", "article.ai-writing.readtime", "article.ai-writing.date",
     "Best AI Writing Tools 2026: ChatGPT vs Claude vs DeepSeek", "14 min read", "2026-06-27",
     "article.ai-writing.body",
     '''<p>2026 年，AI 写作工具已经成了内容创作者的标配。但问题来了：ChatGPT、Claude、DeepSeek 这三巨头，到底选哪个？</p>
    <p>我花了两个月，用这三款工具写了超过 200 篇文章，从中文写作、代码生成、营销文案到 SEO 优化，全面实测。下面是真实结论。</p>

    <h2>速览对比</h2>
    <table style="width:100%;border-collapse:collapse;margin:1em 0">
      <tr style="background:var(--accent-light)"><th style="padding:.5em;text-align:left">维度</th><th style="padding:.5em">ChatGPT</th><th style="padding:.5em">Claude</th><th style="padding:.5em">DeepSeek</th></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">中文质量</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">英文质量</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">长文能力</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">代码能力</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">性价比</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">上下文长度</td><td>128K</td><td>200K</td><td>128K</td></tr>
      <tr><td style="padding:.5em">月费</td><td>$20</td><td>$20</td><td>$2-8</td></tr>
    </table>

    <h2>ChatGPT（OpenAI）</h2>
    <h3>优势</h3>
    <ul><li><strong>生态最完整</strong>：插件、API、DALL-E 生图、代码解释器一应俱全</li><li><strong>英文写作最强</strong>：写英文文章、邮件、营销文案几乎完美</li><li><strong>社区最大</strong>：教程多、案例多、遇到问题容易搜到答案</li></ul>
    <h3>劣势</h3><ul><li>中文偶尔生硬，翻译腔明显</li><li>长文逻辑有时跳跃，需要人工检查</li><li>$20/月不算便宜，重度使用可能有额度限制</li></ul>
    <h3>最适合</h3><p>需要多模态（文字+图片+代码）综合能力的创作者；主要写英文内容的用户。</p>

    <h2>Claude（Anthropic）</h2>
    <h3>优势</h3><ul><li><strong>长文能力第一</strong>：200K 上下文，一次能处理整本书，写长文逻辑最连贯</li><li><strong>中文比 ChatGPT 自然</strong>：翻译腔更少，语感更接近人类</li><li><strong>代码能力极强</strong>：复杂项目、架构设计表现优异</li></ul>
    <h3>劣势</h3><ul><li>没有生图功能</li><li>免费版使用次数较少</li><li>偶尔"过于谨慎"，拒绝回答一些其实无害的问题</li></ul>
    <h3>最适合</h3><p>写长文（5000 字以上）的创作者；需要写代码的独立开发者。</p>

    <h2>DeepSeek（深度求索）</h2>
    <h3>优势</h3><ul><li><strong>中文第一</strong>：中文写作最自然流畅，几乎没有 AI 感</li><li><strong>性价比爆炸</strong>：API 价格是 OpenAI 的 1/10，月费才几块钱</li><li><strong>开源模型</strong>：可以本地部署，数据不外传</li></ul>
    <h3>劣势</h3><ul><li>英文写作稍弱于 ChatGPT 和 Claude</li><li>生态不如 OpenAI 丰富（插件少）</li><li>高峰时段可能排队</li></ul>
    <h3>最适合</h3><p>以中文写作为主的内容创作者；预算有限但需要高质量 AI 辅助的用户。</p>

    <h2>我的实际使用方案</h2>
    <p>我不会只用一款。我现在的组合是：</p>
    <ul><li><strong>中文文章初稿</strong> → DeepSeek（最自然、最便宜）</li><li><strong>英文内容</strong> → Claude（英文好、长文连贯）</li><li><strong>写代码 / 建站</strong> → Claude + ChatGPT 交替用</li><li><strong>配图生成</strong> → ChatGPT（内建 DALL-E）</li></ul>
    <p>一个月总共花费不到 $30，覆盖了所有内容创作需求。</p>''',
     '''<p>By 2026, AI writing tools have become essential for content creators. But here's the question: ChatGPT, Claude, DeepSeek — which of these three giants should you choose?</p>
    <p>I spent two months writing over 200 articles with these three tools, testing them on Chinese writing, code generation, marketing copy, and SEO optimization. Here are the real results.</p>

    <h2>Quick Comparison</h2>
    <table style="width:100%;border-collapse:collapse;margin:1em 0">
      <tr style="background:var(--accent-light)"><th style="padding:.5em;text-align:left">Dimension</th><th style="padding:.5em">ChatGPT</th><th style="padding:.5em">Claude</th><th style="padding:.5em">DeepSeek</th></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Chinese Quality</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">English Quality</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Long-form Writing</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Coding</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td><td>⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Value for Money</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Context Length</td><td>128K</td><td>200K</td><td>128K</td></tr>
      <tr><td style="padding:.5em">Monthly Cost</td><td>$20</td><td>$20</td><td>$2-8</td></tr>
    </table>

    <h2>ChatGPT (OpenAI)</h2>
    <h3>Strengths</h3>
    <ul><li><strong>Most complete ecosystem</strong>: Plugins, API, DALL-E image generation, code interpreter — all in one</li><li><strong>Best English writing</strong>: Near-perfect for English articles, emails, and marketing copy</li><li><strong>Largest community</strong>: Tons of tutorials, case studies, easy to find answers to problems</li></ul>
    <h3>Weaknesses</h3><ul><li>Chinese output can feel stiff with noticeable translation artifacts</li><li>Long-form logic sometimes jumps around, needs human review</li><li>$20/month isn't cheap, heavy usage may hit rate limits</li></ul>
    <h3>Best For</h3><p>Creators needing multimodal capabilities (text + images + code); primarily English content writers.</p>

    <h2>Claude (Anthropic)</h2>
    <h3>Strengths</h3><ul><li><strong>#1 for long-form writing</strong>: 200K context — can process an entire book at once, the most coherent long-form logic</li><li><strong>More natural Chinese than ChatGPT</strong>: Less translation-like, feels closer to human writing</li><li><strong>Excellent coding ability</strong>: Outstanding performance on complex projects and architecture design</li></ul>
    <h3>Weaknesses</h3><ul><li>No image generation capability</li><li>Fewer free tier messages</li><li>Occasionally "overly cautious," refusing to answer harmless questions</li></ul>
    <h3>Best For</h3><p>Long-form writers (5,000+ words); indie developers who need to write code.</p>

    <h2>DeepSeek</h2>
    <h3>Strengths</h3><ul><li><strong>#1 in Chinese</strong>: The most natural and fluid Chinese writing, almost no AI feel</li><li><strong>Insane value for money</strong>: API pricing at 1/10 of OpenAI, monthly cost is just a few dollars</li><li><strong>Open-source model</strong>: Self-hostable, your data stays private</li></ul>
    <h3>Weaknesses</h3><ul><li>English writing slightly weaker than ChatGPT and Claude</li><li>Smaller ecosystem (fewer plugins) than OpenAI</li><li>May queue during peak hours</li></ul>
    <h3>Best For</h3><p>Primarily Chinese content creators; users on a budget who still need high-quality AI assistance.</p>

    <h2>My Actual Workflow</h2>
    <p>I don't use just one. Here's my current setup:</p>
    <ul><li><strong>Chinese article drafts</strong> → DeepSeek (most natural, cheapest)</li><li><strong>English content</strong> → Claude (great English, coherent long-form)</li><li><strong>Coding / site building</strong> → Claude + ChatGPT, alternating</li><li><strong>Image generation</strong> → ChatGPT (built-in DALL-E)</li></ul>
    <p>Total monthly cost under $30, covering all my content creation needs.</p>'''),

    ("free-ai-tools-creators.html", "bot", "cat.ai",
     "article.free-ai.title", "article.free-ai.readtime", "article.free-ai.date",
     "10 Free AI Tools Every Creator Should Know", "9 min read", "2026-06-26",
     "article.free-ai.body",
     '''<p>2026 年了，还在手动做图剪视频？下面这 10 个 AI 工具全都提供免费套餐，足够大多数创作者日常使用。</p>

    <h2>写作与内容</h2>
    <h3>1. DeepSeek（写作助手）</h3>
    <p>中文写作能力最强的免费 AI。写文章、改稿、翻译、头脑风暴，免费额度大得离谱，基本等于无限用。API 价格也是几家大模型中最便宜的。</p>
    <p><strong>免费额度</strong>：网页版基本无限 / API 有免费额度</p>
    <h3>2. Claude（长文写作）</h3>
    <p>200K 上下文的怪兽。丢一本 10 万字的书进去都能读完并总结。写长文章逻辑最连贯。免费版每天几十条消息，够用。</p>
    <p><strong>免费额度</strong>：每天约 50 条消息</p>

    <h2>图片与设计</h2>
    <h3>3. Leonardo AI（AI 生图）</h3>
    <p>画质不输 Midjourney，但每天有 150 免费额度。自带图片编辑、扩图、背景替换等实用功能。设计素材图的神器。</p>
    <p><strong>免费额度</strong>：150 tokens/天</p>
    <h3>4. Canva AI（设计+AI）</h3>
    <p>Canva 的 AI 功能越来越强：AI 生图、去背景、魔法扩图、自动配色。免费版足够做社交媒体图、缩略图、简单海报。</p>
    <p><strong>免费额度</strong>：基础功能免费，AI 功能有限额</p>
    <h3>5. Remove.bg（一键去背景）</h3>
    <p>虽然不算 AI 新秀，但真的太实用。上传图片自动去背景，免费版每月 50 张。做素材必备。</p>
    <p><strong>免费额度</strong>：50 张/月</p>

    <h2>视频与音频</h2>
    <h3>6. CapCut / 剪映（AI 视频剪辑）</h3>
    <p>自动字幕、AI 配音、智能剪片、一键成片。免费版功能比很多付费剪片软件还全。短视频创作者人手一个。</p>
    <p><strong>免费额度</strong>：核心功能全免费</p>
    <h3>7. ElevenLabs（AI 配音）</h3>
    <p>文字转语音天花板。音色自然到几乎听不出是 AI。做视频配音、Podcast 旁白的神器。免费版每月 10 分钟。</p>
    <p><strong>免费额度</strong>：10 分钟/月</p>

    <h2>效率与工作流</h2>
    <h3>8. Notion AI（笔记+AI）</h3>
    <p>Notion 的 AI 功能可以帮你总结笔记、改写文案、生成表格、翻译。如果你已经在用 Notion 做知识管理，AI 加成就很自然。</p>
    <p><strong>免费额度</strong>：Notion 免费版 + Notion AI 有免费试用</p>
    <h3>9. Perplexity AI（AI 搜索）</h3>
    <p>做内容调研的神器。不像 ChatGPT 会编造信息，Perplexity 每条回答都附带来源链接。免费版每天几十次搜索，做研究、查资料、验证事实都用它。</p>
    <p><strong>免费额度</strong>：每天约 20 次深度搜索</p>
    <h3>10. Otter.ai（会议转录）</h3>
    <p>采访、会议、Podcast 录音 → 自动转文字 → AI 总结。做访谈类内容的创作者必备。免费版每月 300 分钟。</p>
    <p><strong>免费额度</strong>：300 分钟/月</p>

    <h2>组合使用建议</h2>
    <p>我自己每天用的组合：</p>
    <ul><li><strong>写作</strong>：DeepSeek（中文初稿）+ Claude（长文润色）</li><li><strong>配图</strong>：Leonardo AI（生图）+ Canva（排版）+ Remove.bg（去背景）</li><li><strong>视频</strong>：CapCut（剪辑）+ ElevenLabs（配音）</li><li><strong>研究</strong>：Perplexity（调研）+ Notion（整理）</li></ul>
    <p>全部免费，一个月 0 元。等你收入上来了再考虑付费版解锁更多功能。</p>''',
     '''<p>It's 2026 — are you still manually making graphics and editing videos? The 10 AI tools below all offer free plans, more than enough for most creators' daily needs.</p>

    <h2>Writing & Content</h2>
    <h3>1. DeepSeek (Writing Assistant)</h3>
    <p>The strongest free AI for Chinese writing. Articles, editing, translation, brainstorming — the free tier is absurdly generous, practically unlimited. API pricing is also the cheapest among major models.</p>
    <p><strong>Free tier</strong>: Web version essentially unlimited / API has free credits</p>
    <h3>2. Claude (Long-Form Writing)</h3>
    <p>A 200K context monster. Drop in a 100,000-word book and it can read and summarize the entire thing. Most coherent long-form logic. Free tier: dozens of messages per day, plenty for most.</p>
    <p><strong>Free tier</strong>: ~50 messages per day</p>

    <h2>Images & Design</h2>
    <h3>3. Leonardo AI (AI Image Generation)</h3>
    <p>Image quality rivals Midjourney, but with 150 free daily credits. Built-in image editing, outpainting, background replacement — a design asset powerhouse.</p>
    <p><strong>Free tier</strong>: 150 tokens/day</p>
    <h3>4. Canva AI (Design + AI)</h3>
    <p>Canva's AI keeps getting stronger: AI image generation, background removal, magic expand, auto color palettes. The free version handles social media graphics, thumbnails, and simple posters.</p>
    <p><strong>Free tier</strong>: Core features free, AI features have limits</p>
    <h3>5. Remove.bg (One-Click Background Removal)</h3>
    <p>Not a new AI tool, but incredibly useful. Upload an image, background gone instantly. Free plan: 50 images/month. Essential for asset creation.</p>
    <p><strong>Free tier</strong>: 50 images/month</p>

    <h2>Video & Audio</h2>
    <h3>6. CapCut (AI Video Editing)</h3>
    <p>Auto captions, AI voiceover, smart trimming, one-click video creation. The free version has more features than many paid editing tools. Every short-form creator's essential tool.</p>
    <p><strong>Free tier</strong>: All core features free</p>
    <h3>7. ElevenLabs (AI Voiceover)</h3>
    <p>The pinnacle of text-to-speech. Voices so natural you can barely tell it's AI. Perfect for video voiceovers and podcast narration. Free tier: 10 minutes/month.</p>
    <p><strong>Free tier</strong>: 10 minutes/month</p>

    <h2>Productivity & Workflow</h2>
    <h3>8. Notion AI (Notes + AI)</h3>
    <p>Notion's AI can summarize notes, rewrite copy, generate tables, and translate. If you're already using Notion for knowledge management, the AI add-on fits naturally.</p>
    <p><strong>Free tier</strong>: Notion free plan + Notion AI free trial available</p>
    <h3>9. Perplexity AI (AI Search)</h3>
    <p>A research powerhouse. Unlike ChatGPT, which can hallucinate, Perplexity cites sources for every answer. Free tier: dozens of searches per day — use it for research, fact-checking, and data gathering.</p>
    <p><strong>Free tier</strong>: ~20 deep searches/day</p>
    <h3>10. Otter.ai (Meeting Transcription)</h3>
    <p>Interviews, meetings, podcast recordings → auto transcription → AI summary. Essential for interview-based content creators. Free tier: 300 minutes/month.</p>
    <p><strong>Free tier</strong>: 300 minutes/month</p>

    <h2>Recommended Combo</h2>
    <p>Here's what I use daily:</p>
    <ul><li><strong>Writing</strong>: DeepSeek (Chinese drafts) + Claude (long-form polish)</li><li><strong>Images</strong>: Leonardo AI (generation) + Canva (layout) + Remove.bg (background removal)</li><li><strong>Video</strong>: CapCut (editing) + ElevenLabs (voiceover)</li><li><strong>Research</strong>: Perplexity (research) + Notion (organization)</li></ul>
    <p>All free, zero dollars a month. Upgrade to paid plans when your revenue catches up.</p>'''),

    ("affiliate-marketing-beginner-2026.html", "briefcase", "cat.sidehustle",
     "article.affiliate.title", "article.affiliate.readtime", "article.affiliate.date",
     "Affiliate Marketing for Beginners: Is It Still Worth It in 2026?", "15 min read", "2026-06-26",
     "article.affiliate.body",
     '''<p>"Affiliate Marketing 已经死了"——每隔几年就有人这么说。但事实是，2026 年全球联盟营销市场规模预计超过 $200 亿美元。死的是那些垃圾站群和搬运工，认真做的人反而更容易出头。</p>
    <p>这篇从零讲清楚：联盟营销是什么、怎么做、2026 年哪些渠道还能赚钱。</p>

    <h2>什么是 Affiliate Marketing？</h2>
    <p>一句话：你推荐别人的产品，别人通过你的链接买了，你拿佣金。不需要囤货、不需要客服、不需要发货。你只负责"带人去买"。</p>
    <p>典型流程：写一篇推荐/对比文章 → 文末放你的专属链接 → 读者点链接购买 → 你赚 5%-30% 佣金。</p>

    <h2>2026 年还能做吗？</h2>
    <p>简短回答：<strong>能，但方法变了。</strong></p>
    <p>2018 年那套"建 100 个垃圾站、互相挂链接"的方法早就不行了。Google 2024 年 Helpful Content Update 之后，低质量联盟站几乎全灭。但反过来讲，认真写、提供真实价值的网站，流量反而涨了。</p>
    <p><strong>好消息是</strong>：AI 工具让"认真写"的成本降低了 90%。以前写一篇深度测评要 3 天，现在有了 AI 辅助，一天能写 3 篇。</p>

    <h2>选品：卖什么最赚钱？</h2>
    <p>不是所有产品都适合做联盟。几个原则：</p>
    <ul><li><strong>佣金率高</strong>：软件/SaaS 类通常 20%-30%，实体商品只有 3%-8%</li><li><strong>Cookie 有效期长</strong>：有些软件给 90 天 cookie（用户 90 天内购买都算你的），有些只有 24 小时</li><li><strong>复购率高的产品</strong>：有些联盟计划给续费佣金，用户每月续费你每月拿钱</li></ul>
    <h3>2026 年推荐关注的联盟计划</h3>
    <ul><li><strong>软件/SaaS</strong>：Notion、ClickUp、NordVPN、Cloudflare — 佣金 20%-40%</li><li><strong>AI 工具</strong>：Jasper、Writesonic、Grammarly — AI 赛道热，佣金可观</li><li><strong>建站工具</strong>：SiteGround、Bluehost、Shopify — 佣金 $50-150/单</li><li><strong>课程平台</strong>：Skillshare、Coursera — 稳定收入来源</li></ul>

    <h2>推广渠道怎么选？</h2>
    <h3>方式一：内容站（推荐）</h3>
    <p>建一个垂直领域的博客/网站，写深度文章，嵌入联盟链接。这种方式的优势是长期积累、被动收入。缺点是起效慢（通常 3-6 个月才有稳定流量）。</p>
    <h3>方式二：YouTube</h3>
    <p>做产品测评/教程视频，描述区放联盟链接。视频 SEO 竞争比文章小，而且 YouTube 本身就是搜索引擎（第二大搜索引擎）。</p>
    <h3>方式三：Newsletter</h3>
    <p>建立邮件列表，定期推荐工具/产品。转化率通常高于网站（因为订阅者已经信任你）。</p>
    <h3>方式四：社交媒体</h3>
    <p>Twitter/X、Reddit 的某些子版块可以发推荐帖。但注意平台规则，滥发链接会被封。</p>

    <h2>新手起步路线图</h2>
    <ol><li><strong>第 1 周</strong>：选定一个细分领域（比如"独立开发者工具"或"远程办公软件"）</li><li><strong>第 2 周</strong>：注册 3-5 个联盟计划（Impact、PartnerStack、ShareASale 是最大的联盟平台）</li><li><strong>第 3-4 周</strong>：写 5 篇深度文章，每篇推荐 2-3 个产品</li><li><strong>第 2 个月</strong>：开始推广文章（社交媒体、SEO、相关论坛）</li><li><strong>第 3-6 个月</strong>：根据数据优化高转化文章，删除低转化内容</li></ol>

    <h2>关键提醒</h2>
    <blockquote>不要为了佣金推荐烂产品。你的信誉比一笔佣金值钱一万倍。推荐你真正用过、觉得好的东西。</blockquote>
    <p>另外，大部分国家要求你在页面上披露 affiliate 关系（FTC 规定）。诚实标注"这篇文章包含 affiliate 链接"不仅合规，反而增加读者信任。</p>''',
     '''<p>"Affiliate marketing is dead" — someone says this every few years. The reality: the global affiliate marketing market is projected to exceed $200 billion in 2026. What's dead is the spam farms and content scrapers. Those who put in real effort are actually finding it easier to stand out.</p>
    <p>This guide covers everything from scratch: what affiliate marketing is, how to do it, and which channels still work in 2026.</p>

    <h2>What Is Affiliate Marketing?</h2>
    <p>In one sentence: you recommend someone else's product, someone buys through your link, you earn a commission. No inventory, no customer service, no shipping. Your only job is to "bring people to buy."</p>
    <p>Typical flow: Write a review/comparison article → Place your affiliate link at the end → Readers click and purchase → You earn 5%-30% commission.</p>

    <h2>Is It Still Worth Doing in 2026?</h2>
    <p>Short answer: <strong>Yes, but the game has changed.</strong></p>
    <p>The 2018 playbook of "build 100 spam sites and cross-link them" is dead. Google's 2024 Helpful Content Update wiped out low-quality affiliate sites. But flip side: sites that write genuinely useful content have actually seen traffic increases.</p>
    <p><strong>The good news</strong>: AI tools have cut the cost of "writing genuinely" by 90%. What used to take 3 days for a deep review now takes one day for three pieces with AI assistance.</p>

    <h2>Product Selection: What Sells Best?</h2>
    <p>Not all products work well for affiliates. Key principles:</p>
    <ul><li><strong>High commission rates</strong>: Software/SaaS typically 20%-30%, physical products only 3%-8%</li><li><strong>Long cookie duration</strong>: Some programs offer 90-day cookies (purchases within 90 days count as yours), others only 24 hours</li><li><strong>Recurring revenue products</strong>: Some programs pay renewal commissions — user renews monthly, you earn monthly</li></ul>
    <h3>Recommended Affiliate Programs for 2026</h3>
    <ul><li><strong>Software/SaaS</strong>: Notion, ClickUp, NordVPN, Cloudflare — 20%-40% commissions</li><li><strong>AI tools</strong>: Jasper, Writesonic, Grammarly — hot AI niche with solid commissions</li><li><strong>Hosting/Building</strong>: SiteGround, Bluehost, Shopify — $50-150 per conversion</li><li><strong>Course platforms</strong>: Skillshare, Coursera — steady income stream</li></ul>

    <h2>Which Promotion Channels to Use?</h2>
    <h3>Channel 1: Content Site (Recommended)</h3>
    <p>Build a niche blog/website, write in-depth articles, embed affiliate links. The advantage: long-term accumulation and passive income. The downside: slow start (typically 3-6 months for stable traffic).</p>
    <h3>Channel 2: YouTube</h3>
    <p>Create product review/tutorial videos, place affiliate links in descriptions. Video SEO has less competition than written content, and YouTube is the world's second-largest search engine.</p>
    <h3>Channel 3: Newsletter</h3>
    <p>Build an email list, regularly recommend tools and products. Conversion rates are typically higher than websites (subscribers already trust you).</p>
    <h3>Channel 4: Social Media</h3>
    <p>Twitter/X and certain Reddit communities allow recommendation posts. But respect platform rules — link spam gets you banned.</p>

    <h2>Beginner Roadmap</h2>
    <ol><li><strong>Week 1</strong>: Pick a niche (e.g., "indie developer tools" or "remote work software")</li><li><strong>Week 2</strong>: Sign up for 3-5 affiliate programs (Impact, PartnerStack, ShareASale are the largest platforms)</li><li><strong>Weeks 3-4</strong>: Write 5 in-depth articles, each recommending 2-3 products</li><li><strong>Month 2</strong>: Start promoting articles (social media, SEO, relevant forums)</li><li><strong>Months 3-6</strong>: Optimize high-converting articles based on data, remove low-performers</li></ol>

    <h2>Key Reminder</h2>
    <blockquote>Never recommend a bad product for a commission. Your reputation is worth 10,000 times more than a single payout. Only recommend products you've actually used and genuinely believe in.</blockquote>
    <p>Also, most countries require affiliate disclosure (FTC rules). Honestly stating "this article contains affiliate links" is not only compliant — it actually increases reader trust.</p>'''),
]

articles2 = [
    ("upwork-freelancing-guide.html", "briefcase", "cat.sidehustle",
     "article.upwork.title", "article.upwork.readtime", "article.upwork.date",
     "Upwork Freelancing Guide: From Signup to $1,000/Month", "12 min read", "2026-06-24",
     "article.upwork.body",
     '''<p>Upwork 是全球最大的自由职业平台，2026 年活跃项目超过 200 万个。不管你是程序员、设计师、写手还是翻译，都有大量的接单机会。</p>
    <p>但是，90% 的新手在第一周就放弃了——因为不会写 Proposal，投 20 个一个都没回。这篇就是解决这个问题的。</p>

    <h2>第一步：注册和被拒的坑</h2>
    <p>Upwork 对新账号审核很严，注册时注意：</p>
    <ul><li>用真实信息注册（名字、地址、技能都要真）</li><li>选择竞争小的细分技能（比如别选"写作"，选"AI 工具教程写作"）</li><li>上传真实的个人头像（别用 AI 生成的，会被拒绝）</li></ul>
    <p>很多人注册就被拒。如果被拒：检查你的技能是不是太泛、Profile 是不是太空、头像是不是太假。修改后重新提交。</p>

    <h2>第二步：Profile 优化——让客户找你</h2>
    <p>好的 Profile 不是"我会 Python、JS、React"，而是"我能帮你解决什么问题"。对比：</p>
    <blockquote>❌ "I am a web developer with 5 years of experience in React and Node.js."<br>✅ "I build high-converting landing pages for SaaS startups. My last 3 clients saw 40%+ increase in trial signups within 2 weeks."</blockquote>
    <p><strong>Profile 黄金公式</strong>：标题 = 技能 + 结果 + 目标客户。比如"AI Content Writer for SaaS Blogs — 200+ Published Articles"。</p>

    <h2>第三步：写 Proposal——最关键的一步</h2>
    <p>Upwork Proposal 不是简历，是"方案"。客户不关心你是谁，只关心"你能帮我搞定这件事吗？"</p>
    <h3>Proposal 模板（直接抄）</h3>
    <pre>Hi [客户名],

I just read your job post about [项目简述].

Here's how I'd approach this:
1. [第一步做什么]
2. [第二步做什么]  
3. [交付什么]

I recently did something similar for [提一个相关案例].
Here's the result: [用一个数字说明结果].

[Attach 相关作品链接]

Happy to jump on a quick call if you'd like to discuss.
Best,
[你的名字]</pre>
    <p>关键点：<strong>前两行必须让客户觉得你真的看了他的需求</strong>。90% 的 Proposal 都是用模板批量投的，你只要稍微定制一下就能脱颖而出。</p>

    <h2>第四步：定价策略</h2>
    <p>新手最纠结的问题：报价多少？</p>
    <p><strong>策略：前 3 单低价拿评价，后面正常报价。</strong></p>
    <ul><li>第 1-3 单：报市场价的 60%-70%，目标不是赚钱，是拿 5 星评价</li><li>第 4-10 单：正常报价，拿到 Job Success Score 90%+</li><li>第 10 单之后：每 3-5 单涨价 10%-20%，直到找到你的天花板</li></ul>
    <p>参考价格（2026 年）：写作类 $30-80/篇、网页开发 $40-100/小时、设计 $25-60/小时。</p>

    <h2>第五步：避开常见坑</h2>
    <ul><li><strong>不要在站外沟通/收款</strong>：Upwork 会封号，保证金也没了</li><li><strong>不要接"先做一版看看"的活</strong>：免费试做 = 白嫖</li><li><strong>用 Upwork 的时间追踪器</strong>：按时计费项目必须用，出纠纷有证据</li><li><strong>不要同时接太多活</strong>：质量下降 → 差评 → 更难接单，恶性循环</li></ul>

    <h2>月入 $1000 需要多长时间？</h2>
    <p>真实数据：每天投入 2-3 小时，第一个月 $100-300，第三个月 $500-800，第六个月稳定 $1000+。当然，这取决于你的技能水平和投入程度。</p>
    <p>写得好的程序员/设计师，第一个月就能过 $1000。写手和翻译可能需要 2-3 个月。</p>''',
     '''<p>Upwork is the world's largest freelancing platform, with over 2 million active projects in 2026. Whether you're a developer, designer, writer, or translator, there are abundant opportunities to land work.</p>
    <p>But 90% of newcomers quit within the first week — because they don't know how to write proposals. They send 20 and get zero responses. This guide is here to fix that.</p>

    <h2>Step 1: Signup and Avoiding Rejection</h2>
    <p>Upwork is strict about new account reviews. When signing up, note:</p>
    <ul><li>Use real information (name, address, skills — all genuine)</li><li>Choose niche skills with less competition (e.g., don't pick "Writing," pick "AI Tool Tutorial Writing")</li><li>Upload a real profile photo (no AI-generated headshots — they'll be rejected)</li></ul>
    <p>Many people get rejected at signup. If rejected: check if your skills are too broad, your profile is too thin, or your photo looks fake. Revise and resubmit.</p>

    <h2>Step 2: Profile Optimization — Make Clients Come to You</h2>
    <p>A good profile isn't "I know Python, JS, React" — it's "What problem can I solve for you?" Compare:</p>
    <blockquote>❌ "I am a web developer with 5 years of experience in React and Node.js."<br>✅ "I build high-converting landing pages for SaaS startups. My last 3 clients saw 40%+ increase in trial signups within 2 weeks."</blockquote>
    <p><strong>Profile golden formula</strong>: Title = Skill + Result + Target Client. Example: "AI Content Writer for SaaS Blogs — 200+ Published Articles."</p>

    <h2>Step 3: Writing Proposals — The Most Critical Step</h2>
    <p>An Upwork proposal is not a resume — it's a "solution plan." Clients don't care who you are, they care about one thing: "Can you get this done for me?"</p>
    <h3>Proposal Template (Copy This)</h3>
    <pre>Hi [Client Name],

I just read your job post about [brief project summary].

Here's how I'd approach this:
1. [First step]
2. [Second step]
3. [Deliverable]

I recently did something similar for [mention a relevant case].
Here's the result: [state result with a number].

[Attach relevant portfolio link]

Happy to jump on a quick call if you'd like to discuss.
Best,
[Your Name]</pre>
    <p>Key point: <strong>the first two lines must show the client you've actually read their requirements</strong>. 90% of proposals are copy-paste templates. Even slight customization makes you stand out.</p>

    <h2>Step 4: Pricing Strategy</h2>
    <p>The most agonizing question for beginners: how much to charge?</p>
    <p><strong>Strategy: first 3 projects at lower rates to build reviews, then normal pricing.</strong></p>
    <ul><li>Projects 1-3: Bid at 60%-70% of market rate. The goal isn't profit — it's 5-star reviews</li><li>Projects 4-10: Normal pricing. Aim for 90%+ Job Success Score</li><li>After project 10: Raise rates 10%-20% every 3-5 projects until you find your ceiling</li></ul>
    <p>Reference rates (2026): Writing $30-80/article, Web Dev $40-100/hour, Design $25-60/hour.</p>

    <h2>Step 5: Common Pitfalls to Avoid</h2>
    <ul><li><strong>Never communicate or accept payment off-platform</strong>: Upwork will ban you, and you lose payment protection</li><li><strong>Never accept "do a sample first" gigs</strong>: Free samples = free work with no pay</li><li><strong>Use Upwork's time tracker</strong>: Mandatory for hourly projects; provides evidence in case of disputes</li><li><strong>Don't take on too many projects at once</strong>: Quality drops → bad reviews → harder to land work = downward spiral</li></ul>

    <h2>How Long to Reach $1,000/Month?</h2>
    <p>Real data: with 2-3 hours/day, expect $100-300 in month one, $500-800 by month three, and a stable $1,000+ by month six. This varies with your skill level and effort.</p>
    <p>Strong developers and designers can hit $1,000 in the first month. Writers and translators may need 2-3 months.</p>'''),

    ("notion-setup-workflow.html", "zap", "cat.productivity",
     "article.notion-workflow.title", "article.notion-workflow.readtime", "article.notion-workflow.date",
     "Build a Personal Workflow in Notion: From Chaos to Clarity", "11 min read", "2026-06-25",
     "article.notion-workflow.body",
     '''<p>大多数人用 Notion 是这样：今天建一个页面记笔记，明天建一个页面列任务，一周后页面散落各处，找不到东西。这不是 Notion 的问题，是缺少一个工作流框架。</p>
    <p>这篇给你一套可以直接照搬的 Notion 工作流。核心原则：<strong>用尽可能少的页面，覆盖所有日常场景。</strong></p>

    <h2>工作流概览：一个 Dashboard 管所有</h2>
    <p>整个系统只有 4 个核心模块，全部集中在一个 Dashboard（仪表盘）页面里：</p>
    <ol><li><strong>任务收件箱</strong>：所有待办事项的入口</li><li><strong>项目看板</strong>：进行中的项目追踪</li><li><strong>知识库</strong>：笔记和参考资料</li><li><strong>周回顾</strong>：每周复盘区域</li></ol>

    <h2>第一步：创建任务收件箱</h2>
    <p>建一个 Notion Database（数据库），叫"任务收件箱"。字段设置：</p>
    <ul><li>任务名称（Title）</li><li>状态（Select）：待处理 / 进行中 / 已完成</li><li>优先级（Select）：高 / 中 / 低</li><li>截止日期（Date）</li><li>所属项目（Relation → 关联到项目看板）</li></ul>
    <p>关键规则：<strong>任何想法、任务、提醒，第一时间丢进收件箱</strong>。不要"等一下记"，不要"脑记"。养成"脑中一闪 → 手就打进 Notion"的条件反射。</p>
    <p>每天早上花 3 分钟清收件箱：哪些今天做 → 标优先级高+截止日期今天；哪些以后做 → 标低优先级；哪些不需要做 → 直接删。</p>

    <h2>第二步：搭项目看板</h2>
    <p>再建一个数据库叫"项目"，用 Board 视图显示。字段：</p>
    <ul><li>项目名称</li><li>状态：规划中 → 进行中 → 暂停 → 完成</li><li>截止日期</li><li>关联任务（Relation → 关联任务收件箱）</li></ul>
    <p>每个项目是一个卡片，卡片里有项目描述、关键结果、关联的所有任务。一个页面看所有项目的进展。</p>

    <h2>第三步：建知识库</h2>
    <p>再一个数据库叫"知识库"，这是你的第二大脑。分类：</p>
    <ul><li>文章/教程笔记</li><li>会议记录</li><li>灵感/想法</li><li>书签/书摘</li></ul>
    <p>不用过度分类。Notion 的搜索很强，用标签（Multi-Select）代替文件夹结构。标签如：#SEO、#变现、#建站、#AI。想找东西时搜标签比翻文件夹快 10 倍。</p>

    <h2>第四步：设置周回顾模板</h2>
    <p>在 Dashboard 最底部放一个 Toggle List（折叠列表），里面是每周回顾的固定问题：</p>
    <ul><li>本周完成了什么？（去任务库筛"已完成"）</li><li>什么没完成？为什么？</li><li>下周最重要的 3 件事？</li><li>学到了什么新东西？</li></ul>
    <p>每周日花 15 分钟回答这 4 个问题。这是整个系统中最重要的一环——没有回顾，前面三件事都白做。</p>

    <h2>Dashboard 最终布局</h2>
    <p>把上面 4 个模块放在一个页面里，用分栏布局：</p>
    <ul><li>左栏 70%：任务收件箱（Today 视图）+ 项目看板</li><li>右栏 30%：快捷入口 + 知识库最近更新</li><li>底部：周回顾</li></ul>
    <p>每天打开 Notion，第一眼看到的就是今天要做什么。信息不散落，心理负担大幅降低。</p>''',
     '''<p>Most people use Notion like this: create a page for notes today, create another for tasks tomorrow, and a week later pages are scattered everywhere, nothing can be found. This isn't a Notion problem — it's a missing workflow framework.</p>
    <p>This guide gives you a Notion workflow you can copy directly. Core principle: <strong>cover all daily scenarios with as few pages as possible.</strong></p>

    <h2>Workflow Overview: One Dashboard Rules All</h2>
    <p>The entire system has just 4 core modules, all centralized in one Dashboard page:</p>
    <ol><li><strong>Task Inbox</strong>: The entry point for all to-dos</li><li><strong>Project Board</strong>: Tracking active projects</li><li><strong>Knowledge Base</strong>: Notes and reference materials</li><li><strong>Weekly Review</strong>: Weekly reflection area</li></ol>

    <h2>Step 1: Create the Task Inbox</h2>
    <p>Build a Notion Database called "Task Inbox." Field setup:</p>
    <ul><li>Task Name (Title)</li><li>Status (Select): To Do / In Progress / Done</li><li>Priority (Select): High / Medium / Low</li><li>Due Date (Date)</li><li>Project (Relation → link to Project Board)</li></ul>
    <p>Key rule: <strong>any thought, task, or reminder goes into the inbox immediately</strong>. No "I'll write it down later," no "I'll remember it." Build the reflex: thought pops up → fingers type into Notion.</p>
    <p>Spend 3 minutes every morning clearing the inbox: what to do today → mark high priority + due today; what to do later → mark low priority; what's not needed → delete.</p>

    <h2>Step 2: Build the Project Board</h2>
    <p>Create another database called "Projects," displayed in Board view. Fields:</p>
    <ul><li>Project Name</li><li>Status: Planning → In Progress → Paused → Complete</li><li>Due Date</li><li>Linked Tasks (Relation → link to Task Inbox)</li></ul>
    <p>Each project is a card containing the project description, key results, and all linked tasks. One page to see all project progress.</p>

    <h2>Step 3: Build the Knowledge Base</h2>
    <p>Another database called "Knowledge Base" — your second brain. Categories:</p>
    <ul><li>Article/Tutorial Notes</li><li>Meeting Notes</li><li>Ideas/Inspiration</li><li>Bookmarks/Highlights</li></ul>
    <p>Don't over-categorize. Notion's search is powerful — use tags (Multi-Select) instead of folder structures. Tags like: #SEO, #Monetization, #WebDev, #AI. Searching by tag is 10x faster than digging through folders.</p>

    <h2>Step 4: Set Up the Weekly Review Template</h2>
    <p>Place a Toggle List at the bottom of your Dashboard with these fixed weekly reflection questions:</p>
    <ul><li>What did I complete this week? (filter task DB for "Done")</li><li>What didn't get done? Why?</li><li>Top 3 priorities for next week?</li><li>What new thing did I learn?</li></ul>
    <p>Spend 15 minutes every Sunday answering these 4 questions. This is the most important part of the entire system — without review, the first three steps are wasted.</p>

    <h2>Final Dashboard Layout</h2>
    <p>Put all 4 modules on one page with a column layout:</p>
    <ul><li>Left column 70%: Task Inbox (Today view) + Project Board</li><li>Right column 30%: Quick links + Knowledge Base recent updates</li><li>Bottom: Weekly Review</li></ul>
    <p>Open Notion each day and the first thing you see is exactly what you need to do. No scattered information, dramatically reduced mental load.</p>'''),

    ("automation-tools-no-code.html", "zap", "cat.productivity",
     "article.automation.title", "article.automation.readtime", "article.automation.date",
     "No-Code Automation: Zapier + Make Practical Guide", "12 min read", "2026-06-21",
     "article.automation.body",
     '''<p>每天花 2 小时做重复的事情？复制粘贴数据、手动发社交媒体、挨个发邮件…… 这些都可以自动化。不需要写一行代码。</p>

    <h2>Zapier vs Make：选哪个？</h2>
    <table style="width:100%;border-collapse:collapse;margin:1em 0">
      <tr style="background:var(--accent-light)"><th style="padding:.5em;text-align:left">维度</th><th style="padding:.5em">Zapier</th><th style="padding:.5em">Make</th></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">上手难度</td><td>⭐（超简单）</td><td>⭐⭐（稍复杂）</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">功能深度</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">免费额度</td><td>100 tasks/月</td><td>1000 ops/月</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">视觉化</td><td>列表式</td><td>流程图式</td></tr>
      <tr><td style="padding:.5em">最佳用途</td><td>简单串联</td><td>复杂多步骤</td></tr>
    </table>
    <p><strong>建议</strong>：新手从 Zapier 开始，免费额度用完后切到 Make（免费额度多 10 倍，功能更强）。</p>

    <h2>10 个实用自动化场景</h2>
    <h3>1. RSS → 邮件（内容监测）</h3>
    <p>用 Make 监测竞品博客的 RSS，有新文章自动发邮件通知。设置：RSS 模块（定时检查）→ Email 模块（发送通知）。10 分钟搞定。</p>
    <h3>2. Google Forms → Notion 数据库</h3>
    <p>用户填表单 → 自动写入 Notion 数据库。适合做客户管理、反馈收集、问卷汇总。设置：Google Forms 触发器 → Notion 创建条目。</p>
    <h3>3. 社交媒体自动发布</h3>
    <p>在 Notion 写好内容 → 定时自动发到 Twitter、LinkedIn。用 Make 的调度器：Notion 查询 → 文本处理 → Twitter API 发帖。</p>
    <h3>4. 邮件附件自动存网盘</h3>
    <p>Gmail 收到带附件的邮件 → 自动下载 → 保存到 Google Drive/OneDrive。Gmail 触发器 → 检测附件 → Drive 上传。</p>
    <h3>5. 电商订单 → 自动发感谢信</h3>
    <p>Gumroad 新订单 → 自动提取买家邮箱 → 发送个性化感谢邮件 + 使用指南。</p>
    <h3>6. 日历事件 → Slack 通知</h3>
    <p>Google Calendar 明天有会议 → 今晚 8 点自动发 Slack/Discord 提醒。防止忘记第二天的事。</p>
    <h3>7. 表单提交 → 自动生成发票 PDF</h3>
    <p>客户通过表单提交项目信息 → 自动生成发票 PDF → 发邮件给客户。Freelancer 的发票流程全自动。</p>
    <h3>8. YouTube 新视频 → 自动写摘要发博客</h3>
    <p>你自己的 YouTube 频道发了新视频 → Make 抓取标题和描述 → 发给 AI 生成文字版 → 发布到博客。</p>
    <h3>9. 数据备份自动化</h3>
    <p>每天凌晨 2 点，自动把 Notion 数据库导出为 CSV，备份到 Google Drive。数据安全的基本保障。</p>
    <h3>10. 竞品监测仪表盘</h3>
    <p>定期抓取竞品网站的变化（新文章、新功能）→ 汇总到 Notion 数据库 ← 自动通知你。</p>

    <h2>搭建建议</h2>
    <ol><li><strong>先列需求再搭</strong>：把你每周重复做的 5 件事列出来，挑最花时间的那件先自动化</li><li><strong>从简单开始</strong>：别一上来就做 10 步的复杂流程。2-3 步的小自动化，做好了再拼起来</li><li><strong>加错误通知</strong>：每个自动化加一个"失败时发邮件/消息给我"的步骤，防止静默断掉</li></ol>''',
     '''<p>Spending 2 hours a day on repetitive tasks? Copy-pasting data, manually posting to social media, sending individual emails... all of this can be automated. No code required.</p>

    <h2>Zapier vs Make: Which to Choose?</h2>
    <table style="width:100%;border-collapse:collapse;margin:1em 0">
      <tr style="background:var(--accent-light)"><th style="padding:.5em;text-align:left">Dimension</th><th style="padding:.5em">Zapier</th><th style="padding:.5em">Make</th></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Ease of Use</td><td>⭐ (Super Easy)</td><td>⭐⭐ (Slightly Complex)</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Feature Depth</td><td>⭐⭐⭐</td><td>⭐⭐⭐⭐⭐</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Free Tier</td><td>100 tasks/month</td><td>1000 ops/month</td></tr>
      <tr style="border-bottom:1px solid var(--border)"><td style="padding:.5em">Visual Style</td><td>List-based</td><td>Flowchart-based</td></tr>
      <tr><td style="padding:.5em">Best Use</td><td>Simple connections</td><td>Complex multi-step</td></tr>
    </table>
    <p><strong>Recommendation</strong>: Start with Zapier as a beginner. When the free tier runs out, switch to Make (10x more free capacity, more powerful).</p>

    <h2>10 Practical Automation Scenarios</h2>
    <h3>1. RSS → Email (Content Monitoring)</h3>
    <p>Monitor competitor blog RSS feeds with Make, automatically email you when new articles appear. Setup: RSS module (periodic check) → Email module (send notification). Done in 10 minutes.</p>
    <h3>2. Google Forms → Notion Database</h3>
    <p>User fills out a form → automatically written to Notion database. Great for client management, feedback collection, survey aggregation. Setup: Google Forms trigger → Notion create entry.</p>
    <h3>3. Auto-Publish to Social Media</h3>
    <p>Write content in Notion → scheduled auto-posting to Twitter and LinkedIn. Use Make's scheduler: Notion query → text processing → Twitter API post.</p>
    <h3>4. Auto-Save Email Attachments to Cloud Storage</h3>
    <p>Gmail receives email with attachment → auto-download → save to Google Drive/OneDrive. Gmail trigger → detect attachment → Drive upload.</p>
    <h3>5. E-Commerce Orders → Auto Thank-You Email</h3>
    <p>New Gumroad order → auto-extract buyer email → send personalized thank-you email + usage guide.</p>
    <h3>6. Calendar Events → Slack Notifications</h3>
    <p>Google Calendar has a meeting tomorrow → auto-send Slack/Discord reminder at 8 PM tonight. Never forget tomorrow's commitments.</p>
    <h3>7. Form Submission → Auto-Generate Invoice PDF</h3>
    <p>Client submits project info via form → auto-generate invoice PDF → email to client. Fully automated invoicing for freelancers.</p>
    <h3>8. New YouTube Video → Auto Summary to Blog</h3>
    <p>You publish a new YouTube video → Make grabs title and description → sends to AI for text version → publishes to your blog.</p>
    <h3>9. Data Backup Automation</h3>
    <p>Every day at 2 AM, auto-export Notion database as CSV, back up to Google Drive. Basic data safety guarantee.</p>
    <h3>10. Competitor Monitoring Dashboard</h3>
    <p>Periodically scrape competitor website changes (new articles, new features) → aggregate into Notion database → auto-notify you.</p>

    <h2>Build Tips</h2>
    <ol><li><strong>List needs first, then build</strong>: Write down the 5 things you do repetitively each week. Automate the most time-consuming one first</li><li><strong>Start simple</strong>: Don't jump into a complex 10-step workflow. Build small 2-3 step automations, then combine them</li><li><strong>Add error notifications</strong>: For every automation, add a "notify me on failure" step to prevent silent breakdowns</li></ol>'''),

    ("cloudflare-for-indie-makers.html", "zap", "cat.productivity",
     "article.cloudflare.title", "article.cloudflare.readtime", "article.cloudflare.date",
     "Cloudflare for Indie Makers: The Complete Free Tier Guide", "14 min read", "2026-06-17",
     "article.cloudflare.body",
     '''<p>Cloudflare 是独立创作者的隐藏外挂。大多数人只知道它是 CDN，实际上它的免费版有 20+ 个服务，覆盖了你建站需要的几乎所有基础设施。</p>

    <h2>Cloudflare 免费版能做什么？</h2>
    <ul><li>托管静态网站（Pages，无限流量）</li><li>注册和管理域名（比 Namecheap 便宜）</li><li>全球 CDN 加速</li><li>DDoS 防护</li><li>免费 SSL 证书</li><li>Web Analytics（不依赖 Google Analytics）</li><li>无服务器函数（Workers，每日 10 万次免费）</li><li>KV 存储、D1 数据库（免费额度）</li><li>表单处理、邮件路由</li><li>图片优化、缓存规则</li></ul>
    <p>说真的，一个独立创作者的网站，免费版完全够用。不够用的是你对它的了解。</p>

    <h2>第一步：域名注册</h2>
    <p>直接在 Cloudflare 买域名，不要经过第三方。为什么？</p>
    <ol><li>Cloudflare 卖域名几乎零利润（只收注册局成本价）</li><li>不需要额外配置 DNS，买完直接管</li><li>没有隐藏续费涨价（Namecheap、GoDaddy 第一年便宜第二年翻倍）</li></ol>
    <p>一个 .com 域名约 $10/年，直接在 Cloudflare Dashboard → Domain Registration 搜索购买。</p>

    <h2>第二步：网站托管（Pages）</h2>
    <p>如果你的网站是纯静态（HTML+CSS+JS，就是我们这种内容站），Cloudflare Pages 是最佳选择：</p>
    <ul><li>直接连 GitHub 仓库，Push 代码自动部署</li><li>全球 330+ 节点，访问速度极快</li><li>无限流量、无限请求（免费）</li><li>自带预览部署（每个 PR 自动生成预览链接）</li></ul>
    <p>部署步骤：Pages → 创建项目 → 连接 GitHub 仓库 → 设置构建命令（纯静态选 None）→ 部署。全程 2 分钟。</p>

    <h2>第三步：分析工具（Web Analytics）</h2>
    <p>Google Analytics 太臃肿、隐私不友好、还被很多浏览器拦截。Cloudflare Web Analytics 是更好的选择：</p>
    <ul><li>基于服务器端数据，不会被 AdBlock 拦截</li><li>不追踪个人隐私，不需要 Cookie 弹窗</li><li>核心指标都有：PV、UV、来源、国家、设备</li><li>完全免费</li></ul>
    <p>在 Dashboard → Analytics & Logs → Web Analytics 里添加你的站点，把 JS 代码放到页面 &lt;head&gt; 里即可。</p>

    <h2>第四步：基础安全配置</h2>
    <h3>SSL/TLS</h3>
    <p>Cloudflare 默认提供免费 SSL 证书。在 SSL/TLS 设置里选"Full (strict)"，确保访问者和 Cloudflare 之间、Cloudflare 和你的服务器之间都加密。</p>
    <h3>安全头</h3>
    <p>在 Pages 项目的根目录创建一个 <code>_headers</code> 文件：</p>
    <pre>/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()</pre>
    <h3>缓存规则</h3>
    <p>在 Dashboard → Caching → Cache Rules 里设置：</p>
    <ul><li>HTML 文件缓存 1 小时（内容更新后能及时生效）</li><li>CSS/JS/图片缓存 1 个月（这些文件很少变，加版本号控制更新）</li></ul>

    <h2>第五步：其他实用功能</h2>
    <h3>Workers（无服务器函数）</h3>
    <p>需要一个简单的后端逻辑（比如表单提交、API 中转、A/B 测试）？Workers 每天免费 10 万次请求。写几行 JS 就行。</p>
    <h3>Email Routing（邮件路由）</h3>
    <p>想要 hello@你的域名.com 但不想维护邮件服务器？Cloudflare Email Routing 把你的域名邮箱转发到你现有的 Gmail，免费。</p>
    <h3>Zaraz（第三方脚本管理）</h3>
    <p>你的网站放了 GA、Facebook Pixel、Hotjar…… 这些第三方脚本拖慢网站。Zaraz 把它们通过 Cloudflare 的边缘网络加载，速度更快、用户隐私更好。</p>

    <h2>总结：独立创作者的标准配置</h2>
    <p>一个内容站的最小化 Cloudflare 配置：</p>
    <ul><li>域名：Cloudflare Registrar</li><li>托管：Cloudflare Pages（连 GitHub）</li><li>CDN/安全：默认开启</li><li>分析：Web Analytics</li><li>邮件：Email Routing → 转发到 Gmail</li></ul>
    <p>全年花费：域名 $10。其他全部 $0。</p>''',
     '''<p>Cloudflare is the indie creator's hidden superpower. Most people think it's just a CDN, but its free tier actually offers 20+ services covering nearly all the infrastructure you need to run a website.</p>

    <h2>What Can Cloudflare's Free Tier Do?</h2>
    <ul><li>Host static sites (Pages, unlimited bandwidth)</li><li>Register and manage domains (cheaper than Namecheap)</li><li>Global CDN acceleration</li><li>DDoS protection</li><li>Free SSL certificates</li><li>Web Analytics (no Google Analytics dependency)</li><li>Serverless functions (Workers, 100K free requests/day)</li><li>KV storage, D1 database (free tier)</li><li>Form handling, email routing</li><li>Image optimization, cache rules</li></ul>
    <p>Honestly, for an indie creator's website, the free tier is more than enough. The only thing lacking is your knowledge of what it can do.</p>

    <h2>Step 1: Domain Registration</h2>
    <p>Buy your domain directly from Cloudflare, not through a third party. Why?</p>
    <ol><li>Cloudflare sells domains at near zero profit (registry cost only)</li><li>No extra DNS configuration needed — buy it, manage it, done</li><li>No hidden renewal price hikes (Namecheap and GoDaddy offer cheap year one, then double on renewal)</li></ol>
    <p>A .com domain is roughly $10/year. Go to Cloudflare Dashboard → Domain Registration and search to buy.</p>

    <h2>Step 2: Site Hosting (Pages)</h2>
    <p>If your site is pure static (HTML+CSS+JS, like this content site), Cloudflare Pages is the best choice:</p>
    <ul><li>Direct GitHub repo connection — push code, auto-deploy</li><li>330+ global edge nodes, blazing fast access speed</li><li>Unlimited bandwidth, unlimited requests (free)</li><li>Built-in preview deployments (auto-generated preview URL per PR)</li></ul>
    <p>Deployment steps: Pages → Create Project → Connect GitHub repo → Set build command (select None for pure static) → Deploy. Total time: 2 minutes.</p>

    <h2>Step 3: Analytics (Web Analytics)</h2>
    <p>Google Analytics is bloated, privacy-unfriendly, and blocked by many browsers. Cloudflare Web Analytics is a better choice:</p>
    <ul><li>Server-side data, not blocked by AdBlock</li><li>No personal privacy tracking, no cookie banner needed</li><li>All core metrics: PV, UV, source, country, device</li><li>Completely free</li></ul>
    <p>Go to Dashboard → Analytics & Logs → Web Analytics, add your site, and place the JS snippet in your page's &lt;head&gt;.</p>

    <h2>Step 4: Basic Security Configuration</h2>
    <h3>SSL/TLS</h3>
    <p>Cloudflare provides free SSL certificates by default. In SSL/TLS settings, select "Full (strict)" to ensure encryption both between visitors and Cloudflare, and between Cloudflare and your server.</p>
    <h3>Security Headers</h3>
    <p>Create a <code>_headers</code> file in your Pages project root:</p>
    <pre>/*
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()</pre>
    <h3>Cache Rules</h3>
    <p>In Dashboard → Caching → Cache Rules, set:</p>
    <ul><li>HTML files: cache 1 hour (updates take effect promptly)</li><li>CSS/JS/images: cache 1 month (these rarely change; use versioned filenames for updates)</li></ul>

    <h2>Step 5: Other Useful Features</h2>
    <h3>Workers (Serverless Functions)</h3>
    <p>Need simple backend logic (form submissions, API proxying, A/B testing)? Workers give you 100K free requests per day. Just a few lines of JS.</p>
    <h3>Email Routing</h3>
    <p>Want hello@yourdomain.com but don't want to maintain a mail server? Cloudflare Email Routing forwards your domain emails to your existing Gmail — free.</p>
    <h3>Zaraz (Third-Party Script Management)</h3>
    <p>Your site loads GA, Facebook Pixel, Hotjar... these third-party scripts slow things down. Zaraz loads them through Cloudflare's edge network — faster and better for user privacy.</p>

    <h2>Summary: The Indie Creator's Standard Stack</h2>
    <p>A minimal Cloudflare configuration for a content site:</p>
    <ul><li>Domain: Cloudflare Registrar</li><li>Hosting: Cloudflare Pages (connected to GitHub)</li><li>CDN/Security: Enabled by default</li><li>Analytics: Web Analytics</li><li>Email: Email Routing → forward to Gmail</li></ul>
    <p>Annual cost: $10 for the domain. Everything else: $0.</p>'''),
]

all_articles = articles + articles2

# =====================================================
# Part 1: Update i18n.js with article body translations
# =====================================================
def update_i18n():
    with open(I18N_FILE, 'r') as f:
        content = f.read()
    
    # Add Chinese body translations for all articles
    new_zh_entries = {}
    for (filename, cat_icon, cat_key, title_key, readtime_key, date_key,
         en_title, readtime_en, date_en, body_key, zh_body, en_body) in all_articles:
        # Clean up zh_body - remove leading whitespace per line
        zh_clean = '\n'.join(line[4:] if line.startswith('    ') else line for line in zh_body.strip().split('\n'))
        new_zh_entries[body_key] = zh_clean
    
    # Find the end of zh dict (before the closing };)
    # Insert new entries before the last }; in zh section
    for key, val in new_zh_entries.items():
        # Escape for JS string
        escaped = val.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n')
        # We'll build a single insertion
        pass
    
    # Build the new zh entries string
    zh_entries_str = ""
    for key, val in new_zh_entries.items():
        escaped = val.replace('\\', '\\\\').replace("'", "\\'")
        zh_entries_str += f'\n    "{key}": \'{escaped}\','
    
    # Find position before the closing of zh dict (before "};" after the last zh entry)
    # The zh dict ends with:   }\n};  (closing the zh object)
    # We insert before the "  }" line that closes the zh dict
    marker = "    // 404 page"
    if marker in content:
        # Insert after the 404 entries, before the closing }
        insert_pos = content.rfind("  }\n};")
        if insert_pos == -1:
            insert_pos = content.rfind("};")
        if insert_pos > 0:
            content = content[:insert_pos] + zh_entries_str + '\n' + content[insert_pos:]
    
    with open(I18N_FILE, 'w') as f:
        f.write(content)
    
    print(f"✅ Updated i18n.js with {len(new_zh_entries)} article body translations")

# =====================================================
# Part 2: Fix each article HTML
# =====================================================
def fix_article(filename, cat_icon, cat_key, title_key, readtime_key, date_key,
                en_title, readtime_en, date_en, body_key, zh_body, en_body):
    filepath = f"{ARTICLES_DIR}/{filename}"
    
    with open(filepath, 'r') as f:
        html = f.read()
    
    # Clean up en_body - remove common indentation
    lines = en_body.strip().split('\n')
    en_body_clean = '\n'.join(lines)
    
    # Build new article header
    cat_label = CAT_EN_LABELS.get(cat_key, cat_key.split('.')[1].title())
    new_header = f'''<main class="container-narrow">
  <div class="article-header">
    <div class="cat"><i data-lucide="{cat_icon}" class="icon-sm"></i> <span data-i18n="{cat_key}">{cat_label}</span></div>
    <h1 data-i18n="{title_key}">{en_title}</h1>
    <div class="article-meta">
      <span><i data-lucide="clock" class="icon-xs"></i> <span data-i18n="{readtime_key}">{readtime_en}</span></span>
      <span><i data-lucide="calendar" class="icon-xs"></i> <span data-i18n="{date_key}">{date_en}</span></span>
    </div>
  </div>

  <div class="article-body" data-i18n="{body_key}">
{en_body_clean}
  </div>'''
    
    # Replace from <main class="container-narrow"> to </main>
    # Use regex to find and replace the main content area
    import re
    pattern = r'<main class="container-narrow">.*?</main>'
    replacement = new_header + '\n</main>'
    html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    
    # Replace nav section
    nav_pattern = r'<nav class="nav">.*?</nav>'
    html = re.sub(nav_pattern, V13_NAV, html, flags=re.DOTALL)
    
    # Replace footer + script section
    footer_pattern = r'<footer class="footer">.*?</body>'
    replacement_footer = V13_FOOTER + '\n</body>'
    html = re.sub(footer_pattern, replacement_footer, html, flags=re.DOTALL)
    
    # Remove any old standalone main.js reference (should be in V13_FOOTER now)
    # Also remove old standalone lucide refs at bottom
    
    # Add Lucide CDN to <head> if not present
    if 'lucide@latest' not in html.split('</head>')[0]:
        html = html.replace('</head>', '\n<script src="https://unpkg.com/lucide@latest"></script>\n</head>')
    
    # Add og:image if missing (for article pages that don't have it)
    if 'og:image' not in html.split('</head>')[0]:
        og_insert = '\n<meta property="og:image" content="https://makerearn.com/images/og-image.png">\n<meta property="og:type" content="article">\n<meta name="twitter:card" content="summary_large_image">'
        html = html.replace('</head>', og_insert + '\n</head>')
    
    # Add JSON-LD if missing
    if 'application/ld+json' not in html:
        ld_json = f'''<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Article","headline":"{en_title}","datePublished":"{date_en}","author":{{"@type":"Organization","name":"Maker Earn"}}}}
</script>'''
        html = html.replace('</head>', ld_json + '\n</head>')
    
    with open(filepath, 'w') as f:
        f.write(html)
    
    print(f"✅ Fixed {filename}")

# =====================================================
# Run
# =====================================================
if __name__ == '__main__':
    print("=== Fixing 10 article pages to v1.3 standard ===\n")
    
    for article_data in all_articles:
        fix_article(*article_data)
    
    print("\n=== Updating i18n.js ===")
    # We need to add body translations to i18n.js zh section
    update_i18n()
    
    print("\n=== Done! ===")
    print("Next steps:")
    print("1. git add content-site/")
    print("2. git commit -m 'v1.3: fix all 10 article pages - English default + Lucide + i18n'")
    print("3. git push")
    print("4. GitHub Actions will auto-deploy to makerearn.com")
