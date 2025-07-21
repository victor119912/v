@echo off
echo 正在啟動學生請假系統...
echo.

echo 1. 檢查 Docker 是否運行中...
docker version >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: Docker 未運行或未安裝
    echo 請先啟動 Docker Desktop
    pause
    exit /b 1
)

echo 2. 建立環境設定檔...
if not exist backend\.env (
    copy backend\.env.example backend\.env
    echo 已建立 backend\.env 檔案
)

echo 3. 停止現有服務...
docker-compose down

echo 4. 建立並啟動所有服務...
docker-compose up -d --build

echo 5. 等待服務啟動...
timeout /t 10 /nobreak >nul

echo 6. 檢查服務狀態...
docker-compose ps

echo.
echo ========================================
echo 學生請假系統已啟動完成！
echo ========================================
echo.
echo 可存取的服務：
echo - 前端網站: http://localhost:3000
echo - 後端 API: http://localhost:5000
echo - 資料庫管理: http://localhost:8081
echo   (帳號: admin, 密碼: admin123)
echo.
echo 按任意鍵關閉此視窗...
pause >nul
