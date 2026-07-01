# Maker Earn — Changelog

## v1.3 — 2026-07-01

### 🌐 全站英文化
- 所有页面默认英文，title/description/keywords 全部英文化
- 实现 i18n 中英文切换：右上角"中文/EN"按钮，localStorage 记住选择
- js/i18n.js 包含完整中英双语字典

### 🎨 UI 升级
- 所有 emoji 替换为 Lucide SVG 图标（wrench/package/bot/zap/clock/calendar/mail/sun/moon/dollar-sign/briefcase）
- 正经 favicon.svg 代替 emoji 图标
- 字体换成 Inter（Google Fonts），优先英文 web font
- 生成 og-image.png（1200x630）用于社交分享
- 生成 PWA icon（192x192 + 512x512）

### 🔧 修复
- about.html 死链修复
- GitHub Actions deploy 用 wrangler 自动部署

## v1.2 — 2026-07-01
- 域名 makerearn.com 上线
- DNS + SSL + Cloudflare Pages 部署完成
- GitHub Actions 自动部署验证通过

## v1.1 — 2026-07-01
- 7 个 Python 自动化脚本全家桶
- GitHub Actions pipeline + health-check + deploy

## v1.0 — 2026-07-01
- 初始上线：10 篇文章 + 首页 + 分类筛选 + 暗色模式
