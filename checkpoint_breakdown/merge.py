"""
多批 breakdown 结果合并（可选）。

编程 Agent：实现考点去重、权重归一化、与人工审阅流程对接。
"""
from __future__ import annotations

import json
from pathlib import Path

from src.common.paths import breakdown_output_dir


def load_all_batches() -> list[dict]:
    out_dir = breakdown_output_dir()
    results = []
    for p in sorted(out_dir.glob("batch_*.json")):
        results.append(json.loads(p.read_text(encoding="utf-8")))
    return results


def merge_simple() -> dict:
    """简单合并：拼接所有 checkpoints（未去重）。"""
    batches = load_all_batches()
    all_cps = []
    for b in batches:
        all_cps.extend(b.get("checkpoints", []))
    return {
        "batch_count": len(batches),
        "checkpoint_count": len(all_cps),
        "checkpoints": all_cps,
    }


if __name__ == "__main__":
    merged = merge_simple()
    out = breakdown_output_dir() / "merged.json"
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"写入 {out}, 考点数 {merged['checkpoint_count']}")
