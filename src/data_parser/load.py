"""
数据解析入口（脚手架）。

编程 Agent：阅读 data/ 下真实文件后重写 load_jsonl / load_csv 及字段映射。
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from src.common.paths import data_dir, project_root
from src.data_parser.models import Record


def load_jsonl(path: Path) -> list[Record]:
    records: list[Record] = []
    with path.open(encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            records.append(
                Record(
                    id=str(obj.get("id", i)),
                    input=str(obj.get("input", obj.get("text", ""))),
                    meta=dict(obj.get("meta") or {}),
                )
            )
    return records


def load_csv(path: Path) -> list[Record]:
    records: list[Record] = []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            records.append(
                Record(
                    id=str(row.get("id", i)),
                    input=str(row.get("input", row.get("text", ""))),
                    meta={k: v for k, v in row.items() if k not in ("id", "input", "text")},
                )
            )
    return records


def load_records(path: Path | None = None) -> list[Record]:
    """默认加载 data/ 下第一个 jsonl/csv，或指定 path。"""
    if path is None:
        root = data_dir()
        candidates = sorted(root.rglob("*.jsonl")) + sorted(root.rglob("*.csv"))
        if not candidates:
            samples = project_root() / "data" / "samples" / "sample.jsonl"
            if samples.exists():
                path = samples
            else:
                raise FileNotFoundError(f"未在 {root} 找到 jsonl/csv，请放入数据或指定 path")
        else:
            path = candidates[0]

    path = Path(path)
    if path.suffix == ".jsonl":
        return load_jsonl(path)
    if path.suffix == ".csv":
        return load_csv(path)
    raise ValueError(f"不支持的格式: {path.suffix}")


def batch_digest(records: list[Record], max_items: int = 10) -> str:
    lines = [r.digest_line() for r in records[:max_items]]
    if len(records) > max_items:
        lines.append(f"... 另有 {len(records) - max_items} 条未展示")
    return "\n".join(lines)


def preview_records(limit: int = 3) -> None:
    records = load_records()
    print(f"共 {len(records)} 条")
    for r in records[:limit]:
        print(r.digest_line(400))


def main() -> None:
    parser = argparse.ArgumentParser(description="预览数据解析结果")
    parser.add_argument("--preview", action="store_true")
    parser.add_argument("--path", type=Path, default=None)
    args = parser.parse_args()
    if args.preview or args.path:
        if args.path:
            recs = load_records(args.path)
            print(f"共 {len(recs)} 条")
            for r in recs[:3]:
                print(r.digest_line(400))
        else:
            preview_records()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
