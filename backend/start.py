"""
后端服务启动入口
兼容旧版路径，确保 start_with_ui.bat 能正常工作
"""
import os
import sys

# 确保 backend/backend/app/main.py 能正确导入
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

# 导入并运行主模块
from app.main import app

if __name__ == "__main__":
    import uvicorn

    frontend_dist = os.path.join(backend_path, "..", "frontend", "dist")
    if os.path.exists(frontend_dist):
        assets_dir = os.path.join(frontend_dist, "assets")
        if os.path.exists(assets_dir):
            from fastapi.staticfiles import StaticFiles
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    uvicorn.run(app, host="127.0.0.1", port=9131, log_level="info")
