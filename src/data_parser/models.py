"""统一中间结构。Agent 应根据真实数据扩展字段。"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Record:
    id: str
    input: str
    meta: dict[str, Any] = field(default_factory=dict)

    def digest_line(self, max_chars: int = 200) -> str:
        text = self.input.replace("\n", " ")
        if len(text) > max_chars:
            text = text[: max_chars - 3] + "..."
        return f"id={self.id} domain={self.meta.get('domain', '?')} text={text}"
