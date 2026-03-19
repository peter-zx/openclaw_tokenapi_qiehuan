# OpenClaw Model Switcher

一个基于 WebUI 的 OpenClaw 模型切换工具，支持快速切换 AI 模型提供商。

## 安全性声明（重要）

**本项目高度重视用户隐私和安全性：**

- ✅ **API Key 不上传**：项目不会将您的 API Key 上传到任何服务器
- ✅ **本地存储**：API Key 仅保存在您浏览器本地的 localStorage 中
- ✅ **不保存到配置文件**：后端 `openclaw.json` 文件只保存模型配置，不保存 API Key
- ✅ **完全离线**：项目代码开源，您可以自行审计安全性

**数据存储说明：**

| 数据类型 | 存储位置 | 是否推送到仓库 |
|---------|---------|---------------|
| 模型 ID | openclaw.json | ✅ 会 |
| Provider ID | openclaw.json | ✅ 会 |
| Base URL | openclaw.json | ✅ 会 |
| API Key | 浏览器 localStorage（仅本地） | ❌ 不会 |

**简单来说**：别人拉取你的项目代码后，看不到你的任何 API Key 信息，需要自己重新填写。

## 功能特性

- **模型通讯录**：保存常用模型配置，方便重复使用
- **一键切换**：点击卡片快速切换当前使用模型
- **批量导入**：支持在线输入或 TXT 文件批量导入模型
- **API Key 记忆**：自动记住每个提供商的 API Key（本地浏览器）
- **提供商筛选**：卡片太多时可按提供商筛选
- **预设支持**：内置阿里云、火山引擎、Kimi、DeepSeek、OpenAI、MiniMax 等预设

## 项目结构

```
.
├── backend/                     # 后端服务 (Python FastAPI)
│   ├── main.py                # FastAPI 主入口
│   ├── config_manager.py      # 配置文件管理
│   ├── gateway_controller.py   # Gateway 服务控制
│   ├── models.py              # 数据模型
│   └── requirements.txt       # Python 依赖
├── frontend/src/               # 前端源码 (Vue 3)
│   ├── App.vue               # 主组件
│   ├── main.js               # 入口文件
│   └── components/           # UI 组件
├── start_with_ui.bat          # 一键启动脚本（Windows）
├── start_with_ui.sh           # 一键启动脚本（Linux/Mac）
└── README.md
```

## 快速开始

### 方式一：一键启动（推荐）

```bash
# Windows: 双击 start_with_ui.bat
# Linux/Mac: bash start_with_ui.sh
```

脚本会自动：
1. 检测并创建 Python 虚拟环境
2. 安装依赖
3. 启动服务
4. 打开浏览器

### 方式二：手动启动

```bash
# 1. 创建虚拟环境
python -m venv venv

# 2. 激活虚拟环境
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. 安装依赖
pip install -r backend/requirements.txt

# 4. 启动服务
python backend/main.py
```

### 方式三：重新构建前端

```bash
cd frontend
npm install
npm run build
cd ..
python backend/main.py
```

## 使用说明

### 基本操作

1. **选择提供商**：点击预设按钮（阿里云/火山引擎等）或自定义
2. **配置服务商**：
   - 点击预设按钮旁边的 **齿轮图标** 打开配置弹窗
   - 填写 Provider ID / Base URL / API Key
   - API Key 只需首次填写，之后会自动从本地记忆
3. **输入模型 ID**：在输入框中填写要使用的模型 ID
4. **保存或应用**：
   - **保存到通讯录**：仅添加模型到列表，不切换
   - **保存并应用**：保存并重启 Gateway，立即切换

### 重启 OpenClaw 服务

当需要重启服务时：
1. 按 `Win + R`，输入 `powershell`
2. 右键选择 **"以管理员身份运行"**
3. 在 PowerShell 中粘贴以下命令回车：
   ```
   taskkill /F /IM node.exe; openclaw gateway
   ```

### 批量导入

1. 选择提供商并确保已配置
2. 点击模型输入框旁边的 **+** 按钮
3. 选择：
   - **在线输入**：每行一个模型 ID
   - **文件导入**：上传 TXT 文件（每行一个 ID）
   - **下载模板**：获取带注释的模板文件
4. 确认导入

### 卡片筛选

当模型太多时，用顶部的 **服务商筛选按钮** 筛选显示。

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/config` | GET | 获取当前配置和模型列表 |
| `/api/save` | POST | 保存模型到通讯录（不重启） |
| `/api/switch` | POST | 切换模型并重启服务 |
| `/api/gateway/control` | POST | 控制 Gateway（stop/start/restart） |

## 配置文件

服务会读写 `~/.openclaw/openclaw.json`（Windows: `C:\Users\xxx\.openclaw\openclaw.json`）

**注意**：API Key 不会保存到此文件中！

JSON 结构说明：
- `models.providers`：通讯录，保存所有模型配置（不含 API Key）
- `agents.defaults.model.primary`：当前实际使用的模型

## 技术栈

- **后端**：Python 3.10+, FastAPI, Uvicorn
- **前端**：Vue 3, Element Plus, Vite
- **样式**：CSS3（UTF-8 编码，支持中文）

## 注意事项

- 切换模型时会重启 OpenClaw Gateway 服务
- API Key 仅保存在浏览器本地（localStorage），不会上传到任何地方
- 配置文件修改后无需重启服务
- 请勿将 API Key 直接写入代码或推送到公开仓库
