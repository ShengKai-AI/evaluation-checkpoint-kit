# 项目引导与完成标准（给编程 Agent）

本文档定义：**如何带用户走完一个通用评测/标注项目**，以及何时视为「项目完成」。拆考点本身由 `checkpoint_breakdown/` 通过 API 并发完成，不在此文档里要求 Agent 对全量数据手拆。

---

## 一、与用户对齐（第一轮对话）

请向用户确认或帮助其填写：

| 项 | 说明 |
|----|------|
| 任务名称 | 例如：对话安全评测、代码生成 rubric |
| 数据位置 | `data/` 下文件名与格式（jsonl / csv / …） |
| 单条样本含义 | 每条记录代表什么（一轮对话 / 一道题+模型答案） |
| 拆考点目标 | 要产出「考点树」还是「带权重的 rubric」还是二者 |
| API | 提供商、模型、预算、并发上限 |
| 成功标准 | 例如：100 条抽样拆完、人工认可 rubric、可视化可交付 |

---

## 二、Agent 应改写的模块（按依赖顺序）

### 1. `src/data_parser/`

- **目标**：把用户原始文件解析为统一的 `Record` 列表（见 `models.py`）。
- **动作**：阅读 `data/` 真实文件 → 改 `load.py` / 字段映射；必要时增加 `jsonl` / `csv` 分支。
- **完成标志**：`python -m src.data_parser.load --preview` 能打印合理条数与 1–2 条样例。

### 2. `checkpoint_breakdown/`

- **目标**：对 Record **分批**调用 LLM API，并发生成考点草案。
- **动作**：改 `client.py` 对接用户 API；改 `run.py` 的 `batch_size`、`max_workers`；确保输出写入 `outputs/breakdown/`。
- **完成标志**：全量或约定抽样跑完；每条或每批有对应 JSON；失败可重试、可断点续跑（可选增强）。

### 3. `visualization/`

- **目标**：汇总 `outputs/breakdown/`（考点数量分布、权重、覆盖度等）。
- **动作**：按实际 JSON schema 改 `report.py`；生成 `outputs/reports/summary.html` 或图表。
- **完成标志**：用户能打开报告做抽检决策。

### 4. `templates/` 与 `examples/`（可选）

- 人工定稿后，把 rubric 沉淀为 `checklist.md` 供后续「逐条评测 Agent」使用。

---

## 三、不建议 Agent 做的事

- 对上万条数据在对话里逐条拆考点（应走 API 管道）。
- 维护与 `breakdown-prompt.md` 矛盾的考点定义（以 breakdown 产出 + 人工审为准）。

---

## 四、项目完成 checklist（Agent 自检）

- [ ] `data/` 数据可被解析，字段文档已更新在 `data/README.md`
- [ ] `.env` 已配置（且未提交 git）
- [ ] `checkpoint_breakdown` 已对约定范围跑通，产物在 `outputs/breakdown/`
- [ ] `visualization` 已生成可交付报告
- [ ] 用户已知晓如何复跑、如何只跑增量（若已实现）
- [ ] （可选）定稿 rubric 已写入 `templates/` 或任务子目录

---

## 五、给用户的一句话说明（可原样转发）

> 你把数据放进 `data/`，在 Cursor 里让 Agent 读 `AGENTS.md`。Agent 会帮你改解析和 API 拆考点脚本；拆出来的考点在 `outputs/` 里，用可视化报告抽检；定稿后再变成正式 checklist 做后续评测。
