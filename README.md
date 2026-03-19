# OpenClaw Model Switcher

一个基于 WebUI 的 OpenClaw 模型切换工具，支持快速切换 AI 模型提供商。

## 功能特性

- **模型通讯录**：保存常用模型配置，方便重复使用
- **一键切换**：点击卡片快速切换当前使用模型
- **批量导入**：支持在线输入或 TXT 文件批量导入模型
- **API Key 记忆**：自动记住每个提供商的 API Key
- **提供商筛选**：卡片太多时可按提供商筛选
- **预设支持**：内置阿里云、火山引擎、Kimi、DeepSeek、OpenAI 等预设

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
2. **填写配置**：
   - URL 自动填充（预设不可改）
   - API Key 只需首次填写（自动记忆）
   - 模型 ID 每次必填
3. **保存或应用**：
   - **保存到通讯录**：仅添加模型到列表，不切换
   - **保存并应用**：保存并重启 Gateway，立即切换

### 批量导入

1. 点击「批量导入」按钮
2. 选择：
   - **在线输入**：每行一个模型 ID
   - **文件导入**：上传 TXT 文件（每行一个 ID）
   - **下载模板**：获取带注释的模板文件
3. 确认导入

### 卡片筛选

当模型太多时，用顶部的「提供商」下拉框筛选显示。

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/config` | GET | 获取当前配置和模型列表 |
| `/api/save` | POST | 保存模型到通讯录（不重启） |
| `/api/switch` | POST | 切换模型并重启服务 |
| `/api/gateway/control` | POST | 控制 Gateway（stop/start/restart） |

## 配置文件

服务会读写 `~/.openclaw/openclaw.json`（Windows: `C:\Users\xxx\.openclaw\openclaw.json`）

JSON 结构说明：
- `models.providers`：通讯录，保存所有模型配置
- `agents.defaults.model.primary`：当前实际使用的模型

## 技术栈

- **后端**：Python 3.10+, FastAPI, Uvicorn
- **前端**：Vue 3, Element Plus, Vite
- **样式**：CSS3（UTF-8 编码，支持中文）

## 注意事项

- 切换模型时会重启 OpenClaw Gateway 服务
- API Key 仅保存在浏览器本地（localStorage）
- 配置文件修改后无需重启服务
