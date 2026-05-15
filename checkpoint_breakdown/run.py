"""
拆考点批处理：并发调用 API，结果写入 outputs/breakdown/。

用法（在项目根目录）:
  python -m checkpoint_breakdown.run
  python -m checkpoint_breakdown.run --limit 100
"""
from __future__ import annotations

import argparse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from checkpoint_breakdown.client import call_breakdown_api
from src.common.paths import breakdown_output_dir
from src.data_parser.load import batch_digest, load_records


def _process_batch(batch_id: int, records, task_description: str) -> tuple[int, dict]:
    digest = batch_digest(records, max_items=15)
    result = call_breakdown_api(task_description, digest, len(records))
    result["_batch_id"] = batch_id
    result["_record_ids"] = [r.id for r in records]
    return batch_id, result


def run(limit: int | None = None) -> None:
    records = load_records()
    if limit:
        records = records[:limit]

    batch_size = int(os.getenv("BREAKDOWN_BATCH_SIZE", "10"))
    max_workers = int(os.getenv("BREAKDOWN_MAX_WORKERS", "4"))
    task_description = os.getenv(
        "TASK_DESCRIPTION", "请根据样本归纳可复用的评测考点。"
    )

    batches: list[tuple[int, list]] = []
    for i in range(0, len(records), batch_size):
        batches.append((i // batch_size, records[i : i + batch_size]))

    out_dir = breakdown_output_dir()
    print(f"共 {len(records)} 条 -> {len(batches)} 批, workers={max_workers}")

    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {
            ex.submit(_process_batch, bid, batch, task_description): bid
            for bid, batch in batches
        }
        for fut in as_completed(futures):
            batch_id, result = fut.result()
            out_path = out_dir / f"batch_{batch_id:04d}.json"
            out_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"写入 {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="只处理前 N 条")
    args = parser.parse_args()
    run(limit=args.limit)


if __name__ == "__main__":
    main()
