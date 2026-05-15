# Evaluation Checkpoint Kit

通用「大数据标注 / 模型评测」项目骨架：**数据层 → 拆考点（API 并发）→ 结果落盘 → 可视化**；编程 Agent 负责按你的真实数据**改写/补全**代码，而不是开箱即用跑通全部数据。

## 核心理念

| 角色 | 做什么 | 不负责什么 |
|------|--------|------------|
| **编程 Agent**（Cursor / Trae / Claude Code） | 读 `prompts/project-guide.md`，引导用户、适配 `data/`、改解析与流水线、接好 API、调可视化 | 不直接对海量样本逐条手拆考点 |
| **拆考点 Agent / 模型**（API 调用） | 按 `prompts/breakdown-prompt.md` 对**批次样本**生成考点树 / rubric 草案 | 不写业务工程代码 |
| **人** | 定任务目标、审阅考点、抽检可视化 | — |

拆考点与逐条评测都适合 **API + 并发**；本仓库提供目录约定与可改写的脚手架。

## 目录结构

```
evaluation-checkpoint-kit/
├── README.md
├── AGENTS.md                      # 给编程 Agent 的入口（指向 project-guide）
├── prompts/
│   ├── project-guide.md           # 用户引导 + 项目完成清单（主 Agent 读这个）
│   └── breakdown-prompt.md        # 拆考点专用（API 侧 system/user 模板）
├── data/                          # 原始数据（jsonl / csv / …）
│   ├── README.md
│   └── samples/                   # 极小示例，便于跑通管道
├── config/
│   └── env.example                # API Key、模型名、并发度等
├── src/
│   ├── data_parser/               # 数据解析与统一 Record 结构
│   └── common/                    # 日志、路径、批处理工具
├── checkpoint_breakdown/            # 拆考点：API 并发、结果写入 outputs/
├── visualization/                 # 读 outputs 做统计图 / HTML 报告
├── outputs/                       # 运行产物（gitignore）
│   ├── breakdown/                 # 考点 JSON / rubric 草案
│   └── reports/
├── templates/                     # 给人看的 checklist / rubric 模板
└── examples/sample-task/          # 单任务 md 示例（可与 breakdown 产出合并）
```

## 快速开始

1. 把真实数据放进 `data/`（或改 `config` 里的路径）。
2. 在 Cursor 等中打开本仓库，让 Agent **先读** `AGENTS.md` → `prompts/project-guide.md`。
3. 按 project-guide 的步骤：适配 `src/data_parser` → 跑通 `checkpoint_breakdown` → 人审 `outputs/breakdown` → 再跑 `visualization`。
4. 定稿后的考点可导出为 `templates/checklist` 或 `examples/.../checklist.md` 供后续逐条评测 Agent 使用。

## 设计原则

- **脚手架不绑死数据格式**：示例仅演示接口；真实字段由编程 Agent 根据 `data/` 重写解析器。
- **拆考点与写代码分离**：`checkpoint_breakdown/` 只关心「样本批次 → API → 结构化考点」。
- **可版本化**：`data/` 可不进 git；`outputs/` 默认忽略；考点与 rubric 可提交。

## 依赖（建议）

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp config/env.example .env   # 填入 API Key
```

具体命令以 `prompts/project-guide.md` 为准（Agent 会根据你的环境更新）。
