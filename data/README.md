# 数据目录

将原始数据放在此目录（或子目录）。**不要假设仓库内示例即你的真实 schema**——由编程 Agent 根据你放入的文件改写 `src/data_parser/`。

## 建议约定

| 格式 | 说明 |
|------|------|
| `.jsonl` | 一行一条 JSON，适合大规模 |
| `.csv` | 表格类标注导出 |
| `.json` | 小批量或嵌套结构 |

## 隐私与 git

- 大数据、含 PII 的文件请加入 `.gitignore`（已忽略 `data/*.jsonl` 等，可按需改）。
- 可只提交 `data/samples/` 下的脱敏小样。

## 当前示例

见 `data/samples/sample.jsonl`：仅用于跑通管道，字段名 `id` / `input` / `meta` 可被 Agent 替换。
