#!/usr/bin/env python3
"""Batch update nav HTML in all pages: move lang/theme into hamburger menu"""

import os
import glob

OLD_NAV = '''<nav class="nav">
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

NEW_NAV = '''<nav class="nav">
  <div class="nav-inner">
    <a href="/" class="nav-brand"><i data-lucide="dollar-sign" class="icon-brand"></i> Maker Earn</a>
    <div class="nav-links" id="nav-links">
      <a href="/#articles" data-i18n="nav.articles">Articles</a>
      <a href="/about.html" data-i18n="nav.about">About</a>
    </div>
    <button class="hamburger" id="hamburger-btn" aria-label="Menu"><i data-lucide="menu"></i></button>
  </div>
  <div class="menu-dropdown" id="menu-dropdown" hidden>
    <button class="menu-item" id="lang-switch"><i data-lucide="languages"></i> <span>中文</span></button>
    <button class="menu-item" id="theme-toggle"><i data-lucide="moon"></i> <span>Dark</span></button>
  </div>
</nav>'''

base = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(os.path.join(base, '*.html')) + glob.glob(os.path.join(base, 'articles', '*.html'))

count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    if OLD_NAV in content:
        content = content.replace(OLD_NAV, NEW_NAV)
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        count += 1
        print(f'✅ {os.path.relpath(f, base)}')
    else:
        print(f'⚠️  SKIP {os.path.relpath(f, base)} - nav not found')

print(f'\nUpdated {count}/{len(files)} files')
