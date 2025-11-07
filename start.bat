@echo off
echo ========================================
echo   AI 智能切题工具 - 启动脚本
echo ========================================
echo.

REM 检查 .env 文件
if not exist .env (
    echo [错误] 未找到 .env 文件
    echo 请先复制 .env.example 为 .env 并配置 API Key
    pause
    exit /b 1
)

echo [1/2] 启动 Python 后端服务...
start "Python Backend" cmd /k "python backend_api.py"

echo [2/2] 等待后端启动...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo   后端服务已启动
echo   API 文档: http://localhost:8000/docs
echo ========================================
echo.
echo 提示：关闭此窗口将停止后端服务
pause

