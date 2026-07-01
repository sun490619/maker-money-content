#!/usr/bin/env python3
"""
AI 调用客户端 AIClient
多模型降级链：Ollama(免费) → Gemini(免费额度) → DeepSeek(极便宜) → HuggingFace(兜底)
自动降级，优先免费模型
"""

import os
import json
import time
import subprocess
from typing import Optional, Dict, List
from dataclasses import dataclass, field


@dataclass
class AIResponse:
    model: str
    content: str
    tokens_used: int
    cost: float
    latency_ms: float
    success: bool
    error: str = ""


class AIClient:
    """
    多模型降级链 AI 客户端
    调用顺序: Ollama → Gemini → DeepSeek → HuggingFace
    哪个先成功就用哪个，全失败则抛异常
    """

    # 模型配置（按降级顺序）
    MODELS = [
        {
            "name": "ollama",
            "model_id": "qwen2.5:7b",
            "cost_per_1k": 0,  # 免费
            "type": "local",
        },
        {
            "name": "gemini",
            "model_id": "gemini-2.0-flash",
            "cost_per_1k": 0,  # 免费额度
            "type": "api",
        },
        {
            "name": "deepseek",
            "model_id": "deepseek-chat",
            "cost_per_1k": 0.00014,  # ¥0.14/百万token ≈ $0.02/百万token
            "type": "api",
        },
        {
            "name": "huggingface",
            "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
            "cost_per_1k": 0,  # 免费兜底
            "type": "api",
        },
    ]

    def __init__(self):
        self.stats = {"calls": 0, "success": 0, "fallback": 0, "total_cost": 0.0}
        self.api_keys = self._load_api_keys()

    def _load_api_keys(self) -> Dict[str, str]:
        """加载 API keys（环境变量优先，其次配置文件）"""
        keys = {}

        # Gemini
        keys["gemini"] = os.environ.get("GEMINI_API_KEY", "")

        # DeepSeek
        keys["deepseek"] = os.environ.get("DEEPSEEK_API_KEY", "")

        # HuggingFace
        keys["huggingface"] = os.environ.get("HF_API_KEY", os.environ.get("HUGGINGFACE_API_KEY", ""))

        # 尝试从 ~/.codebuddy/models.json 读 DeepSeek 配置
        if not keys["deepseek"]:
            try:
                config_path = os.path.expanduser("~/.codebuddy/models.json")
                if os.path.exists(config_path):
                    with open(config_path) as f:
                        config = json.load(f)
                    for model in config.get("models", []):
                        if "deepseek" in model.get("name", "").lower():
                            keys["deepseek"] = model.get("apiKey", "")
                            break
            except Exception:
                pass

        return keys

    def generate(self, prompt: str, system: str = "", max_tokens: int = 2000) -> AIResponse:
        """
        生成文本，自动按降级链尝试
        """
        self.stats["calls"] += 1
        last_error = ""

        for model_cfg in self.MODELS:
            t0 = time.time()
            try:
                content, tokens = self._call_model(model_cfg, prompt, system, max_tokens)
                latency = (time.time() - t0) * 1000

                cost = (tokens / 1000) * model_cfg["cost_per_1k"]
                self.stats["total_cost"] += cost
                self.stats["success"] += 1

                if model_cfg["name"] != self.MODELS[0]["name"]:
                    self.stats["fallback"] += 1

                return AIResponse(
                    model=f"{model_cfg['name']}/{model_cfg['model_id']}",
                    content=content,
                    tokens_used=tokens,
                    cost=cost,
                    latency_ms=latency,
                    success=True,
                )
            except Exception as e:
                last_error = f"{model_cfg['name']}: {str(e)[:100]}"
                continue

        # 全部失败
        self.stats["success"] -= 1  # 修正
        return AIResponse(
            model="none",
            content="",
            tokens_used=0,
            cost=0,
            latency_ms=0,
            success=False,
            error=f"所有模型调用失败: {last_error}",
        )

    def _call_model(self, cfg: Dict, prompt: str, system: str, max_tokens: int) -> tuple:
        """调用具体模型"""
        name = cfg["name"]

        if name == "ollama":
            return self._call_ollama(cfg["model_id"], prompt, system, max_tokens)
        elif name == "gemini":
            return self._call_gemini(cfg["model_id"], prompt, system, max_tokens)
        elif name == "deepseek":
            return self._call_deepseek(cfg["model_id"], prompt, system, max_tokens)
        elif name == "huggingface":
            return self._call_huggingface(cfg["model_id"], prompt, system, max_tokens)
        else:
            raise ValueError(f"未知模型: {name}")

    def _call_ollama(self, model: str, prompt: str, system: str, max_tokens: int) -> tuple:
        """调用本地 Ollama"""
        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        result = subprocess.run(
            ["ollama", "run", model, full_prompt],
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Ollama 失败: {result.stderr.strip()}")

        content = result.stdout.strip()
        if not content:
            raise RuntimeError("Ollama 返回空内容")

        return content, len(content.split()) * 1.5  # 粗略估算 tokens

    def _call_gemini(self, model: str, prompt: str, system: str, max_tokens: int) -> tuple:
        """调用 Google Gemini API"""
        api_key = self.api_keys.get("gemini", "")
        if not api_key:
            raise RuntimeError("未配置 GEMINI_API_KEY")

        import urllib.request

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

        contents = []
        if system:
            contents.append({"role": "user", "parts": [{"text": system}]})
            contents.append({"role": "model", "parts": [{"text": "好的，我理解了。"}]})
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        body = json.dumps({
            "contents": contents,
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": 0.7},
        }).encode()

        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
        resp = urllib.request.urlopen(req, timeout=60)
        data = json.loads(resp.read())

        content = data["candidates"][0]["content"]["parts"][0]["text"]
        usage = data.get("usageMetadata", {})
        tokens = usage.get("totalTokenCount", len(content.split()) * 1.5)

        return content, tokens

    def _call_deepseek(self, model: str, prompt: str, system: str, max_tokens: int) -> tuple:
        """调用 DeepSeek API"""
        api_key = self.api_keys.get("deepseek", "")
        if not api_key:
            raise RuntimeError("未配置 DEEPSEEK_API_KEY")

        import urllib.request

        url = "https://api.deepseek.com/v1/chat/completions"

        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        body = json.dumps({
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }).encode()

        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())

        content = data["choices"][0]["message"]["content"]
        tokens = data.get("usage", {}).get("total_tokens", len(content.split()) * 1.5)

        return content, tokens

    def _call_huggingface(self, model: str, prompt: str, system: str, max_tokens: int) -> tuple:
        """调用 HuggingFace Inference API（免费兜底）"""
        api_key = self.api_keys.get("huggingface", "")
        headers = {"Content-Type": "application/json"}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        import urllib.request

        url = f"https://api-inference.huggingface.co/models/{model}"

        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        body = json.dumps({
            "inputs": full_prompt,
            "parameters": {"max_new_tokens": max_tokens, "temperature": 0.7},
        }).encode()

        req = urllib.request.Request(url, data=body, headers=headers)
        resp = urllib.request.urlopen(req, timeout=120)
        data = json.loads(resp.read())

        if isinstance(data, list) and len(data) > 0:
            content = data[0].get("generated_text", "")
            # HF 返回包含 prompt，需要去掉
            if content.startswith(full_prompt):
                content = content[len(full_prompt):].strip()
        else:
            content = str(data)

        return content, len(content.split()) * 1.5

    def get_stats(self) -> Dict:
        return {
            **self.stats,
            "total_cost_rmb": round(self.stats["total_cost"], 4),
        }


# ===== 命令行测试 =====
if __name__ == "__main__":
    client = AIClient()

    print("🤖 AI 客户端初始化完成")
    print(f"   已配置 API: {[k for k, v in client.api_keys.items() if v]}")
    print(f"   降级链: {' → '.join([m['name'] for m in client.MODELS])}")

    # 快速测试
    response = client.generate(
        prompt="用一句话介绍什么是数字产品",
        max_tokens=100,
    )

    if response.success:
        print(f"\n✅ 成功! 模型: {response.model}")
        print(f"   耗时: {response.latency_ms:.0f}ms")
        print(f"   Tokens: {response.tokens_used}")
        print(f"   费用: ¥{response.cost:.6f}")
        print(f"   内容: {response.content[:200]}")
    else:
        print(f"\n❌ 失败: {response.error}")
