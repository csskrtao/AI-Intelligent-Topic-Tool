@echo off
echo ========================================
echo   AI 智能切题工具 - 开发模式
echo ========================================
echo.

REM 检查 .env 文件
if not exist .env (
    echo [错误] 未找到 .env 文件
    echo 请先复制 .env.example 为 .env 并配置 API Key
    pause
    exit /b 1
)

echo [1/3] 启动 Python 后端服务...
start "Python Backend" cmd /k "python backend_api.py"

echo [2/3] 等待后端启动...
timeout /t 3 /nobreak >nul

echo [3/3] 启动 Vite 开发服务器...
start "Vite Dev Server" cmd /k "npm run dev"

echo.
echo ========================================
echo   开发环境已启动
echo   后端 API: http://localhost:8000
echo   前端界面: http://localhost:5173
echo ========================================
echo.
echo 提示：关闭此窗口将停止所有服务
pause

