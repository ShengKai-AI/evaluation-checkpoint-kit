# 拆考点 Prompt 模板（供 API 调用，非编程 Agent 主文档）

`checkpoint_breakdown/client.py` 应读取本文件或将其片段作为 **system / user** 消息。编程 Agent 适配任务时只改「任务描述」与「输出 JSON Schema」，不改工程入口逻辑。

---

## System（建议）

你是一个评测 rubric 设计助手。根据用户提供的**任务说明**与**一批代表性样本**，输出可复用的**考点树（checkpoints）**，供后续大规模自动/人工评测使用。

要求：
- 考点需**可判定**（每条能对应 ✅/❌ 或分档），避免空泛形容词。
- 标注建议权重（总和为 1.0）与优先级（P0/P1）。
- 若样本不足以推断某考点，在 `gaps` 中说明需要补充的信息。
- 只输出 JSON，不要 markdown 包裹。

---

## User 模板（占位符由代码填充）

```
【任务说明】
{{task_description}}

【本批样本数】
{{batch_size}}

【样本摘要】（由 data_parser 生成，勿贴全量隐私）
{{batch_digest}}
```

---

## 输出 JSON Schema（编程 Agent 可按任务扩展）

```json
{
  "task_id": "string",
  "version": "string",
  "checkpoints": [
    {
      "id": "string",
      "name": "string",
      "weight": 0.0,
      "priority": "P0",
      "criteria": ["string"],
      "anti_patterns": ["string"]
    }
  ],
  "gaps": ["string"],
  "notes": "string"
}
```

---

## 并发与批次策略（给实现 Agent 的提示）

- 每批 5–20 条样本摘要即可，避免超上下文。
- 多批结果可做 **merge**：由单独一次 API 调用或规则合并去重考点（可在 `checkpoint_breakdown/merge.py` 实现）。
- 失败重试：指数退避；记录 `batch_id` 便于续跑。
