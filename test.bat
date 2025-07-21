@echo off
echo 正在測試學生請假系統 API...
echo.

echo 1. 檢查服務狀態...
curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% neq 0 (
    echo 錯誤: 後端 API 服務未運行
    echo 請先執行 start.bat 啟動服務
    pause
    exit /b 1
)

echo 2. 測試使用者註冊...
curl -X POST http://localhost:5000/api/auth/register ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"test123\",\"name\":\"測試使用者\",\"student_id\":\"T001\"}"

echo.
echo.

echo 3. 測試使用者登入...
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"test123\"}"

echo.
echo.

echo 4. 測試錯誤登入...
curl -X POST http://localhost:5000/api/auth/login ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"wrong@example.com\",\"password\":\"wrong\"}"

echo.
echo.
echo API 測試完成！
echo.
echo 請檢查上述回應：
echo - 註冊成功應回傳 201 狀態碼
echo - 登入成功應回傳 200 狀態碼和 JWT token
echo - 錯誤登入應回傳 401 狀態碼
echo.
pause
