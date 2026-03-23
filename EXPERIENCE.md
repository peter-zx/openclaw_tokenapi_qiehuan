# 经验总结：OpenClaw 模型切换工具踩坑记录

## 问题一：API Key 保存后 openclaw.json 为空

**现象**：配置了 provider 的 API Key，保存后 `openclaw.json` 中 `apiKey` 仍为空。

**原因**：`/provider/apikey` 端点只调用了 `secure_config`（加密存储）和 `auth-profiles.json`，没有调用 `config_manager.save_provider()` 更新 `openclaw.json`。

**修复**：新增 `update_provider_config()` 方法，确保三处同时写入：
- `openclaw.json` — OpenClaw 实际读取，明文
- `secure_config.json` — 加密备份
- `auth-profiles.json` — 辅助认证

---

## 问题二：删除模型后 agents.defaults.models 残留引用

**现象**：删除模型卡片后，`openclaw.json` 的 `agents.defaults.models` 中仍有该模型的引用，导致 OpenClaw 热重载持续触发。

**原因**：`delete_model()` 只删了 `providers[xxx].models`，没有清理 `agents.defaults.models`。

**修复**：删除时同时清理：
- `models.providers[xxx].models`
- `agents.defaults.models[provider/model]`
- `agents.defaults.model.primary`（如果删除的是当前模型）

---

## 问题三：api 字段硬编码导致 OpenClaw 调用失败

**现象**：调用 volcengine-ark 时报错 `400 unknown field "prompt_cache_key"`，其他 provider 正常。

**原因**：保存 provider 时硬编码 `api: "openai-completions"`，没有根据 baseUrl 推断正确的 API 类型。OpenClaw 用错误的 API 格式调用火山引擎。

**修复**：新增 `_infer_api_type()` 方法，根据 baseUrl 自动推断：
| baseUrl 特征 | api 类型 |
|-------------|---------|
| 包含 `/v3` 或 `/responses` | `openai-responses` |
| 包含 `/v1` | `openai-chat` |
| 其他 | `openai-completions` |

**各 Provider 正确配置：**
| Provider | baseUrl | api |
|---------|---------|-----|
| volcengine-ark | `ark.cn-beijing.volces.com/api/v3` | `openai-responses` |
| ali-dashscope | `dashscope.aliyuncs.com/compatible-mode/v1` | `openai-chat` |
| kimi | `api.moonshot.cn/v1` | `openai-chat` |
| deepseek | `api.deepseek.com` | `openai-completions` |
| minimax | `api.minimax.chat/v1` | `openai-chat` |

---

## 问题四：prompt_cache_key 错误（OpenClaw 源码 bug）

**现象**：OpenClaw 调用火山引擎时报错 `400 json: unknown field "prompt_cache_key"`，请求 ID 持续变化。

**原因**：OpenClaw 的内部依赖 `@mariozechner/pi-ai` 在发送所有 OpenAI Responses API 请求时，自动注入 `prompt_cache_key: sessionId` 字段。但火山引擎的 API 不支持此字段。

**状态**：OpenClaw 源码问题，非本工具可修复。

**临时方案**：
1. 删除出错的 session 文件（`~/.openclaw/agents/main/sessions/*.jsonl`）
2. 重新开启对话
3. 或等待 OpenClaw 官方修复

**参考**：OpenClaw 源码中 `node_modules/@mariozechner/pi-ai/dist/providers/openai-responses.js` 自动注入该字段。

---

## 问题五：模型字段不完整

**现象**：部分模型（如 `doubao-seed-2-0-code-preview-260215`）保存后只有 `id` 和 `name`，缺少 `contextWindow`、`maxTokens` 等字段。

**原因**：保存时直接追加模型，没有补全完整字段。

**修复**：补全所有模型的标准字段：
```json
{
  "reasoning": false,
  "input": ["text"],
  "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0},
  "contextWindow": 64000,
  "maxTokens": 8000
}
```

---

## 经验教训

1. **OpenClaw 的配置分层**：`openclaw.json` 是核心，必须完整；`secure_config.json` 是加密备份；`auth-profiles.json` 是辅助认证。三者缺一不可。
2. **API 类型决定一切**：不同的 baseUrl 路径对应不同的 API 格式，填错会导致 OpenClaw 用错误的请求格式调用 Provider。
3. **删除要彻底**：删除模型不仅要清理 `providers`，还要清理 `agents.defaults.models` 中的引用，否则会导致热重载循环。
4. **OpenClaw 本身的 bug**：`prompt_cache_key` 是 OpenClaw 源码问题，不是配置问题，不应试图通过修改配置来解决。
5. **session 历史文件会残留错误**：每次 API 调用失败都会记录在 session 的 `.jsonl` 文件中，可能导致后续对话复用失败配置。

---

*文档版本：v1.3.6*
*最后更新：2026-03-24*
