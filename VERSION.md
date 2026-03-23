v1.1.0 修复跨电脑硬编码路径问题，完善API Key注入机制

主要更新：
- 修复所有硬编码路径，使用动态获取用户目录
- 完善 API Key 注入，同时更新 openclaw.json 和 auth-profiles.json
- 修复前端配置状态判断，检查 API Key 是否完整
- 完善依赖文件，添加 pywin32 和 psutil
- 修复静态文件挂载路径问题
- 确保跨 Windows/Mac/Linux 平台兼容
