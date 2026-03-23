# 更新日志

## v1.1.0 (2026-03-23)

### 🎯 核心修复

#### 跨平台兼容性
- ✅ 修复所有硬编码路径问题
  - `config_manager.py`: 使用 `os.path.expanduser("~")` 动态获取用户目录
  - `gateway.py`: 移除硬编码的 Gateway 路径，使用动态路径
  - `main.py`: 修复前端静态文件路径计算
- ✅ 现在支持任意用户名，跨电脑/用户无缝使用
- ✅ 为未来 Mac/Linux 支持做准备（Windows 专用命令标记注释）

#### API Key 注入机制
- ✅ 双文件注入机制
  - 同时更新 `~/.openclaw/openclaw.json`
  - 同时更新 `~/.openclaw/agents/main/agent/auth-profiles.json`
- ✅ 修复前端配置状态判断
  - 现在检查 `baseUrl`、`providerId` 和 `apiKey` 三个字段
  - 只有三项都配置完整才显示"（已配置）"

### 🔧 其他修复

- 完善依赖文件 `requirements.txt`
  - 添加 `pywin32` (Windows 进程管理)
  - 添加 `psutil` (跨平台进程管理)
  - 添加 `pydantic-settings` (配置管理)
- 修复静态文件挂载路径问题
  - 正确挂载 `frontend/dist/assets` 目录
  - 修复模块级别静态文件挂载，确保 `python -m uvicorn` 正常工作

### 📝 使用说明

1. **首次使用**：
   ```bash
   # 1. 安装依赖
   cd frontend && npm install && npm run build
   cd ../backend && pip install -r requirements.txt
   
   # 2. 启动服务
   python start.py
   ```

2. **配置模型**：
   - 选择服务商（如火山引擎）
   - 点击齿轮图标配置 Provider ID、Base URL、API Key
   - 填写模型 ID
   - 点击"保存到通讯录"或"保存并应用"

3. **切换模型**：
   - 点击已保存的模型卡片即可快速切换
   - 自动调用重启脚本，等待 8 秒后生效

### ⚠️ 注意事项

- API Key 仅保存在浏览器 localStorage 和 `auth-profiles.json` 中
- `openclaw.json` 中的 `apiKey` 字段为空（符合 OpenClaw 设计）
- 跨平台时，Mac/Linux 需要修改 `gateway.py` 中的进程管理命令

---

## v1.0.0 (初始版本)

- 基础模型切换功能
- WebUI 管理界面
- 模型通讯录
- 批量导入
