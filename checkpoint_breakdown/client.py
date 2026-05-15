"""
拆考点 API 客户端（脚手架）。

编程 Agent：对接用户实际 API（OpenAI 兼容 / 其他），读取 prompts/breakdown-prompt.md。
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import httpx

from src.common.paths import project_root

PROMPT_PATH = project_root() / "prompts" / "breakdown-prompt.md"


def load_breakdown_system_prompt() -> str:
    text = PROMPT_PATH.read_text(encoding="utf-8")
    # 取 System 段落到下一个 ## 之前（简单切分，Agent 可改）
    if "## System" in text:
        part = text.split("## System", 1)[1]
        if "## User" in part:
            part = part.split("## User", 1)[0]
        return part.strip()
    return text[:2000]


def call_breakdown_api(task_description: str, batch_digest: str, batch_size: int) -> dict:
    """
    调用 LLM 返回考点 JSON。未配置 API Key 时返回 mock，便于本地跑通管道。
    """
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        return _mock_breakdown(batch_size)

    base = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.getenv("BREAKDOWN_MODEL", "gpt-4o-mini")
    system = load_breakdown_system_prompt()
    user = (
        f"【任务说明】\n{task_description}\n\n"
        f"【本批样本数】\n{batch_size}\n\n"
        f"【样本摘要】\n{batch_digest}"
    )

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
    }
    with httpx.Client(timeout=120.0) as client:
        r = client.post(
            f"{base}/chat/completions",
            headers={"Authorization": f"Bearer {api_key}"},
            json=payload,
        )
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def _mock_breakdown(batch_size: int) -> dict:
    return {
        "task_id": "mock",
        "version": "0.1-mock",
        "checkpoints": [
            {
                "id": "c1",
                "name": "示例考点（未配置 API Key）",
                "weight": 1.0,
                "priority": "P0",
                "criteria": [f"本批 {batch_size} 条样本已收到摘要"],
                "anti_patterns": [],
            }
        ],
        "gaps": ["请配置 OPENAI_API_KEY 或改写 client.py 对接你的 API"],
        "notes": "mock response",
    }
