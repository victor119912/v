# 學生請假系統

基於 Python Flask + MongoDB + Docker 的現代化學生請假管理系統。

## 🚀 技術架構

### 後端
- **框架**: Python Flask
- **資料庫**: MongoDB
- **ODM**: PyMongo
- **身份驗證**: JWT (Flask-JWT-Extended)
- **容器化**: Docker & Docker Compose

### 前端
- **基礎版本**: HTML + CSS + JavaScript
- **進階版本**: React (計劃中)

## 📁 專案結構

```
v/
├── backend/              # Python Flask 後端 API
│   ├── app.py           # Flask 應用程式入口
│   ├── config/          # 資料庫設定
│   ├── models/          # 資料模型
│   ├── routes/          # API 路由
│   ├── requirements.txt # Python 依賴
│   └── Dockerfile       # 後端容器設定
├── frontend/            # 前端檔案
│   ├── index.html       # 主頁
│   ├── login.html       # 登入頁
│   ├── register.html    # 註冊頁
│   ├── css/             # 樣式檔案
│   └── js/              # JavaScript 檔案
├── docker-compose.yml   # Docker 服務編排
├── nginx.conf          # Nginx 設定
├── init-mongo.js       # MongoDB 初始化
└── start.bat           # Windows 啟動腳本
```

## ⚡ 快速開始

### 方法一：使用啟動腳本 (Windows)
```bash
# 執行啟動腳本
start.bat
```

### 方法二：手動啟動
```bash
# 1. 複製環境設定檔
cp backend/.env.example backend/.env

# 2. 啟動所有服務
docker-compose up -d --build

# 3. 查看服務狀態
docker-compose ps
```

## 🌐 服務存取

啟動後可存取以下服務：

- **前端網站**: http://localhost:3000
- **後端 API**: http://localhost:5000
- **MongoDB**: localhost:27017
- **Mongo Express** (資料庫管理): http://localhost:8081
  - 帳號: `admin`
  - 密碼: `admin123`

## 📝 API 文檔

### 身份驗證端點
```
POST /api/auth/register    # 使用者註冊
POST /api/auth/login       # 使用者登入
GET  /api/auth/me         # 取得目前使用者資訊
POST /api/auth/logout     # 使用者登出
```

### 使用者管理端點
```
POST /api/users/register   # 使用者註冊 (向後相容)
POST /api/users/login      # 使用者登入 (向後相容)
GET  /api/users/profile    # 取得個人資料
PUT  /api/users/profile    # 更新個人資料
```

### API 使用範例

#### 註冊新使用者
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "password123",
    "name": "張小明",
    "student_id": "S001"
  }'
```

#### 使用者登入
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "password123"
  }'
```

## 🗄️ 資料庫結構

### Users Collection
```javascript
{
  "_id": ObjectId,
  "email": "string (unique)",
  "password_hash": "string",
  "role": "string (student/teacher/admin)",
  "name": "string",
  "student_id": "string",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🔧 開發指令

```bash
# 啟動開發環境
docker-compose up -d

# 查看日誌
docker-compose logs -f backend

# 重建容器
docker-compose build --no-cache

# 停止所有服務
docker-compose down

# 停止並刪除所有資料
docker-compose down -v
```

## ⚙️ 環境設定

編輯 `backend/.env` 檔案：

```env
# Flask 設定
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key

# MongoDB 設定
MONGODB_URI=mongodb://mongodb:27017/student_leave_system
MONGODB_DATABASE=student_leave_system

# JWT 設定
JWT_SECRET_KEY=your-jwt-secret
JWT_ACCESS_TOKEN_EXPIRES=3600
```

## 📋 開發進度

### ✅ 已完成
- [x] 後端 API 架構設計
- [x] MongoDB 資料庫整合
- [x] 使用者註冊/登入功能
- [x] JWT 身份驗證
- [x] Docker 容器化
- [x] 前端基礎頁面
- [x] 前端表單驗證
- [x] API 整合

### 🚧 進行中
- [ ] 前端 JWT 驗證優化
- [ ] 自動登入功能
- [ ] 錯誤處理優化

### 📅 計劃中
- [ ] 請假申請功能
- [ ] 請假審核流程
- [ ] 檔案上傳功能
- [ ] 通知系統
- [ ] React 前端版本
- [ ] 單元測試
- [ ] API 文檔生成

## 🚨 注意事項

1. **安全性**: 生產環境請更改預設密鑰
2. **CORS**: 目前允許所有來源，生產環境請限制
3. **資料備份**: MongoDB 資料持久化在 Docker volume
4. **日誌**: 可透過 `docker-compose logs` 查看

## 🔍 故障排除

### MongoDB 連線問題
```bash
# 檢查 MongoDB 服務
docker-compose logs mongodb

# 重啟 MongoDB
docker-compose restart mongodb
```

### JWT Token 問題
- 檢查 `JWT_SECRET_KEY` 設定
- 確認 Token 格式正確
- 檢查 Token 過期時間

### CORS 錯誤
- 檢查 nginx.conf 設定
- 確認 Flask-CORS 配置

## 📞 支援

如有問題請參考：
1. [後端 API 文檔](backend/README.md)
2. [開發進度追蹤](學生請假系統/todo.md)
3. Docker 服務日誌: `docker-compose logs`