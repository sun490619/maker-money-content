#!/usr/bin/env python3
"""Add cache-busting version parameter to all JS/CSS references"""

import os
import glob
import re

base = os.path.dirname(os.path.abspath(__file__))
files = glob.glob(os.path.join(base, '*.html')) + glob.glob(os.path.join(base, 'articles', '*.html'))

VERSION = '1.3.5'

count = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    original = content
    
    # Add version to i18n.js (but not if already has version)
    content = re.sub(
        r'(src=["\']/js/i18n\.js)(\?v=[^"\']*)?(["\'])',
        f'\\1?v={VERSION}\\3',
        content
    )
    # Add version to main.js
    content = re.sub(
        r'(src=["\']/js/main\.js)(\?v=[^"\']*)?(["\'])',
        f'\\1?v={VERSION}\\3',
        content
    )
    # Add version to style.css
    content = re.sub(
        r'(href=["\']/css/style\.css)(\?v=[^"\']*)?(["\'])',
        f'\\1?v={VERSION}\\3',
        content
    )
    
    if content != original:
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        count += 1
        print(f'✅ {os.path.relpath(f, base)}')
    else:
        print(f'⚠️  SKIP {os.path.relpath(f, base)} - no changes')

print(f'\nUpdated {count}/{len(files)} files')
