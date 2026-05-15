"""
读取 outputs/breakdown/ 生成简易 HTML 报告（脚手架）。

编程 Agent：按真实 JSON 结构增加图表、抽检表格等。
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from jinja2 import Template

from checkpoint_breakdown.merge import load_all_batches
from src.common.paths import breakdown_output_dir, reports_output_dir


REPORT_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <title>拆考点报告</title>
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; max-width: 960px; }
    table { border-collapse: collapse; width: 100%; margin-top: 1rem; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f5f5f5; }
    .meta { color: #666; }
  </style>
</head>
<body>
  <h1>拆考点汇总</h1>
  <p class="meta">批次数: {{ batch_count }} · 考点条目总数（未去重）: {{ cp_count }}</p>

  <h2>考点名称频次（Top 20）</h2>
  <table>
    <tr><th>名称</th><th>出现次数</th></tr>
    {% for name, cnt in name_counts %}
    <tr><td>{{ name }}</td><td>{{ cnt }}</td></tr>
    {% endfor %}
  </table>

  <h2>各批 gaps</h2>
  <ul>
    {% for g in gaps %}
    <li>{{ g }}</li>
    {% endfor %}
  </ul>
</body>
</html>
"""


def build_report() -> Path:
    batches = load_all_batches()
    names: list[str] = []
    gaps: list[str] = []
    for b in batches:
        for cp in b.get("checkpoints", []):
            names.append(cp.get("name", "(unnamed)"))
        for g in b.get("gaps", []):
            if g:
                gaps.append(f"batch {b.get('_batch_id', '?')}: {g}")

    name_counts = Counter(names).most_common(20)
    html = Template(REPORT_TEMPLATE).render(
        batch_count=len(batches),
        cp_count=len(names),
        name_counts=name_counts,
        gaps=gaps[:50],
    )
    out = reports_output_dir() / "summary.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    if not list(breakdown_output_dir().glob("batch_*.json")):
        print("无 breakdown 结果，请先运行: python -m checkpoint_breakdown.run")
        return
    path = build_report()
    print(f"报告已生成: {path}")


if __name__ == "__main__":
    main()
