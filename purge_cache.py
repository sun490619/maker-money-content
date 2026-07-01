#!/usr/bin/env python3
"""
CDN 缓存刷新 PurgeCache
发新文章后调用 Cloudflare API 清除对应页面缓存
"""

import os
import json
import sys
import urllib.request
import urllib.error
from typing import List, Dict


class PurgeCache:
    """Cloudflare CDN 缓存刷新"""

    def __init__(self, zone_id: str = None, api_token: str = None):
        self.zone_id = zone_id or os.environ.get("CF_ZONE_ID", "")
        self.api_token = api_token or os.environ.get("CF_API_TOKEN", "")

    def _check_config(self) -> bool:
        if not self.zone_id:
            print("❌ 缺少 CF_ZONE_ID（环境变量或构造函数参数）")
            return False
        if not self.api_token:
            print("❌ 缺少 CF_API_TOKEN（环境变量或构造函数参数）")
            return False
        return True

    def purge_url(self, url: str) -> Dict:
        """清除单个 URL 缓存"""
        if not self._check_config():
            return {"success": False, "error": "配置缺失"}

        api_url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/purge_cache"
        body = json.dumps({"files": [url]}).encode()

        req = urllib.request.Request(api_url, data=body, headers={
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        })

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
            success = result.get("success", False)
            if success:
                print(f"✅ 缓存已清除: {url}")
            else:
                errors = result.get("errors", [])
                print(f"❌ 清除失败: {url} — {errors}")
            return {"success": success, "result": result}
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            print(f"❌ API 错误 {e.code}: {error_body}")
            return {"success": False, "error": f"HTTP {e.code}: {error_body[:200]}"}
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return {"success": False, "error": str(e)}

    def purge_urls(self, urls: List[str]) -> List[Dict]:
        """批量清除缓存"""
        return [self.purge_url(url) for url in urls]

    def purge_article(self, base_url: str, article_path: str) -> Dict:
        """清除单篇文章缓存（自动拼接 URL）"""
        base = base_url.rstrip("/")
        path = article_path.lstrip("/")
        return self.purge_url(f"{base}/{path}")

    def purge_all(self) -> Dict:
        """清除全站缓存"""
        if not self._check_config():
            return {"success": False, "error": "配置缺失"}

        api_url = f"https://api.cloudflare.com/client/v4/zones/{self.zone_id}/purge_cache"
        body = json.dumps({"purge_everything": True}).encode()

        req = urllib.request.Request(api_url, data=body, headers={
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        })

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read())
            success = result.get("success", False)
            print(f"{'✅' if success else '❌'} 全站缓存清除: {success}")
            return {"success": success, "result": result}
        except Exception as e:
            print(f"❌ 全站清除失败: {e}")
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    pc = PurgeCache()

    if len(sys.argv) < 2:
        print("用法: python purge_cache.py <base_url> <article_path>")
        print("示例: python purge_cache.py https://maker-money.pages.dev articles/new-post.html")
        print("或:    python purge_cache.py --all  (清除全站)")
        sys.exit(1)

    if sys.argv[1] == "--all":
        pc.purge_all()
    elif len(sys.argv) >= 3:
        pc.purge_article(sys.argv[1], sys.argv[2])
    else:
        pc.purge_url(sys.argv[1])
