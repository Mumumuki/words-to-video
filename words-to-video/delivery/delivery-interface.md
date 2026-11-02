# 可迁移交付接口（Delivery Interface）

> 本目录服务本技能的 **S15 步骤**：把 **S14 产出的填表包** 提交到 AI 视频生成平台的"运输层"。设计目标是 **配置驱动、可迁移**：换平台只改 `config.example.json`，不改脚本；任何 agent 拿到 config 都能执行。
>
> **铁律（继承 SKILL 第 18 / 479 行）**：接口只是"运输"，**不是"决策"**。提交前必须已获得用户**显式同意**——用户说"直接提交"也不视为同意。脚本以 `--consent` 作为硬性闸门，未确认则只产出执行计划（`--dry-run`），绝不调用接口。

---

## 一、抽象契约

每段 `P0N` 在 S14 产出一套独立生成单元，对应平台的一次生成任务（job）。契约字段：

| 字段 | 含义 | 来源 |
|---|---|---|
| `segment_id` | 段落号，如 `P01` | 目录名 |
| `prompt` | 第八步确认版六段式全文 | `P0N/prompt.txt` |
| `refs` | 本段挂载的参考图（按 `Picture N` 裁切后的文件） | `P0N/refs/*.png` |
| `handoff_first` / `handoff_last` | 段首/段末承接帧（Ref2VA 纯参考模式不进节点，升级首帧驱动后作为首帧输入） | `P0N/handoff/*.png` |
| `params` | 时长（10–15s）、分辨率、seed、workflow 版本 | `P0N/sheet.md` + `参数清单.md` |
| `cost` | 本段预计图片数与消耗 | S14 成本告知 |

**适配器必须实现两个方法**：
- `submit(payload) -> job_id`：把一段 payload 投到平台，返回任务 ID。
- `get_status(job_id) -> ("pending"|"running"|"succeeded"|"failed", detail)`：轮询状态。

**失败回退**：任一 `failed` 段，按 `SKILL.md` 回退矩阵回到对应步骤（通常是 S14 参数 / S8 提示词 / S7 分镜），不静默重试。

---

## 二、配置 schema（`config.example.json`）

```jsonc
{
  "skill": "words-to-video",
  "default_adapter": "comfyui_local",   // 或 "cloud_minimax"
  "consent_required": true,             // 必须显式同意才提交
  "adapters": {
    "comfyui_local": {
      "type": "comfyui_local",
      "base_url": "http://127.0.0.1:8188",
      "prompt_endpoint": "/prompt",
      "history_endpoint": "/history",
      "workflow_file": "comfyui_minimax_video.json",
      "poll_interval_sec": 3,
      "timeout_sec": 600
    },
    "cloud_minimax": {
      "type": "cloud_minimax",
      "api_base": "https://api.minimax.io/v1",
      "api_key_env": "MINIMAX_API_KEY",        // 从环境变量读，不落盘
      "group_id_env": "MINIMAX_GROUP_ID",
      "model": "video-01",
      "poll_interval_sec": 5,
      "timeout_sec": 1800
    }
  },
  "cost_report": { "notify_before_submit": true }
}
```

新增平台：在 `adapters` 下加一个块 + 写一个名为 `adapters/<type>.py` 的适配器模块即可，无需改 `submit.py`。

---

## 三、用法（`submit.py`）

```bash
# 1) 只出执行计划，不提交（默认、安全）
python delivery/submit.py --package package/ --config delivery/config.example.json --adapter comfyui_local --dry-run

# 2) 已获用户显式同意后，真正提交
python delivery/submit.py --package package/ --config delivery/config.example.json --adapter cloud_minimax --consent

# 3) 只提交指定段落
python delivery/submit.py --package package/ --adapter comfyui_local --consent --segments P01 P02
```

脚本输出 `delivery-manifest.json`：每段 `job_id` 与状态，供后续轮询与回退。失败段不阻塞其余段，但会在 manifest 标注。

---

## 四、与现有流程的关系

- **S14 不变**：仍只产出填表包（不调用接口）。
- **新增 S15（可选自动提交）**：G4（`生产包确认`）通过后、用户显式同意下，调用本接口把 `package/` 提交平台。S15 不产生新内容，只做"运输"。
- **保留手动**：不配置 adapter、或 `--dry-run` 时，只交付填表包，由用户自行运行。
- **工具无关**：适配器是可替换示例，不绑定任何具体产品；云端适配器仅作骨架，真实端点以平台文档为准。
