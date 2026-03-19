# 安装和启动指南

## 前置要求

- Python 3.8+
- Node.js 16+
- OpenClaw 已安装并配置

## 安装步骤

### 1. 后端安装

```powershell
# 确保虚拟环境已激活
.\venv\Scripts\Activate.ps1

# 安装Python依赖
cd backend
pip install -r requirements.txt
```

### 2. 前端安装

```powershell
# 安装Node.js依赖
cd frontend
npm install
```

### 3. 构建前端（可选）

```powershell
npm run build
```

## 启动方式

### 方式一：使用启动脚本（推荐）

```powershell
# 双击运行或在命令行执行
.\start_with_ui.bat
```

### 方式二：手动启动

```powershell
# 1. 激活虚拟环境
.\venv\Scripts\Activate.ps1

# 2. 启动后端（前端会自动服务）
cd backend
python main.py
```

服务将运行在：http://127.0.0.1:9131

### 方式三：前后端分离开发

```powershell
# 终端1 - 启动后端
cd backend
python main.py

# 终端2 - 启动前端开发服务器
cd frontend
npm run dev
```

前端开发服务器：http://localhost:5173

## 使用说明

1. 打开浏览器访问 http://127.0.0.1:9131
2. 选择提供商（阿里云、火山、Kimi、DeepSeek等）
3. 输入 Base URL、API Key 和模型ID
4. 点击"保存配置并应用"
5. 系统会自动保存配置并重启 OpenClaw Gateway

已保存的模型会显示在底部的卡片列表中，点击即可快速切换。

## 常见问题

### Q: 提示"配置文件不存在"
A: 请确保 OpenClaw 配置文件路径正确：`C:\Users\Administrator\.openclaw\openclaw.json`

### Q: 切换模型后服务无法启动
A: 请检查 API Key 和模型ID是否正确，查看后端日志获取详细错误信息

### Q: 前端页面无法访问
A: 确保后端服务已启动，端口 9130 未被占用

### Q: 如何查看API文档
A: 访问 http://127.0.0.1:9131/docs 查看 Swagger API 文档

## 项目结构

```
.
├── backend/              # 后端（FastAPI）
│   ├── main.py          # 主程序
│   ├── config_manager.py # 配置管理
│   ├── gateway_controller.py # 服务控制
│   ├── models.py        # 数据模型
│   └── requirements.txt
├── frontend/            # 前端（Vue3）
│   ├── src/
│   │   ├── components/
│   │   ├── stores/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── start.bat            # 启动脚本
├── README.md            # 项目说明
└── INSTALL.md           # 安装指南
```

## 下一步

- [ ] 根据需要修改配置文件路径
- [ ] 添加更多预设提供商
- [ ] 自定义前端主题颜色
- [ ] 添加使用统计功能
