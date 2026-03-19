# OpenClaw Model Switcher

一个基于 WebUI 的 OpenClaw 模型切换工具，支持快速切换 AI 模型提供商。

## 项目结构

```
.
├── backend/                 # 后端服务 (Python FastAPI)
│   ├── main.py             # FastAPI 主入口
│   ├── config_manager.py   # 配置文件管理
│   ├── gateway_controller.py # Gateway 服务控制
│   ├── models.py           # 数据模型
│   └── requirements.txt    # Python 依赖
├── frontend/                # 前端 (Vue 3 + Vite)
│   ├── src/
│   │   ├── App.vue         # 主组件
│   │   ├── main.js         # 入口文件
│   │   ├── components/     # UI 组件
│   │   └── stores/         # 状态管理
│   ├── dist/               # 构建产物（已编译的静态文件）
│   ├── package.json
│   └── vite.config.js
├── scripts/                 # 脚本
│   ├── start_with_ui.bat   # 启动后端服务
│   ├── stop.bat            # 停止服务
│   └── build_frontend.bat  # 构建前端
└── README.md
```

## 快速开始

### 方式一：使用构建产物（推荐）

1. **克隆项目**
   ```bash
   git clone <repo-url>
   cd openclaw-model-switcher
   ```

2. **配置虚拟环境并安装依赖**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   pip install -r backend\requirements.txt

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   pip install -r backend/requirements.txt
   ```

3. **启动服务**
   ```bash
   # Windows
   start_with_ui.bat

   # Linux/Mac
   ./start_with_ui.sh
   ```

4. **访问 Web UI**
   打开浏览器访问：http://127.0.0.1:9131

### 方式二：重新构建前端

如果前端有修改，需要重新构建：

```bash
# 安装前端依赖
cd frontend
npm install

# 构建
npm run build
```

然后启动后端服务即可。

## 功能说明

- **保存到通讯录**：将模型配置保存到列表，不影响当前使用的模型
- **保存并应用**：保存配置并重启 Gateway 服务，立即切换模型
- **点击卡片切换**：快速切换到已保存的模型

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/config` | GET | 获取当前配置和模型列表 |
| `/api/save` | POST | 保存模型到通讯录（不重启） |
| `/api/switch` | POST | 切换模型并重启服务 |
| `/api/gateway/control` | POST | 控制 Gateway（stop/start/restart） |

## 配置文件

服务会读取 `C:\Users\Administrator\.openclaw\openclaw.json`，如果不存在会自动创建默认配置。

## 技术栈

- **后端**：Python 3.10+, FastAPI, Uvicorn
- **前端**：Vue 3, Element Plus, Vite
- **样式**：CSS3（UTF-8 编码，支持中文）
