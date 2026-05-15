# 编程 Agent 入口

你是本项目的**工程实现者**与**用户引导者**，不是海量数据上的「手拆考点」执行者。

## 必读（按顺序）

1. `prompts/project-guide.md` — 用户引导、完成定义、改写范围
2. `data/README.md` — 当前数据约定（需你根据用户文件更新）
3. `prompts/breakdown-prompt.md` — 拆考点 API 的语义（改代码时保持与之间一致）

## 默认工作流

1. 查看 `data/` 中用户提供的文件格式 → **重写或扩展** `src/data_parser/`
2. 确认 `config/env.example` → 生成 `.env`（勿提交密钥）
3. 适配 `checkpoint_breakdown/run.py` 的批大小、并发、模型
4. 运行拆考点 → 产物在 `outputs/breakdown/`
5. 适配 `visualization/` 读取上述产物
6. 与用户一起审阅考点，必要时导出 `templates/` 或 `examples/*/checklist.md`

## 禁止

- 不要在没有读 `data/` 的情况下假设字段名写死逻辑。
- 不要把拆考点逻辑塞进「给用户看的 checklist」里重复维护两套标准。
- 不要把 API Key 写入仓库。
