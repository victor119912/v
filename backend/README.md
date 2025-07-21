# 學生請假系統後端 API

基於 Python Flask + MongoDB + Docker 的學生請假系統後端 RESTful API。

## 技術架構
- **框架**: Python Flask
- **資料庫**: MongoDB
- **ODM**: PyMongo
- **身份驗證**: JWT (Flask-JWT-Extended)
- **容器化**: Docker & Docker Compose
- **API 風格**: RESTful API

## 功能特色
- 使用者註冊/登入系統
- JWT 身份驗證
- 密碼加密 (bcrypt)
- MongoDB 資料庫整合
- Docker 容器化部署
- CORS 支援
- RESTful API 設計

## 快速開始

### 使用 Docker (推薦)

1. **複製環境設定檔**:
   ```bash
   cp .env.example .env
   ```

2. **啟動所有服務**:
   ```bash
   docker-compose up -d
   ```

3. **查看服務狀態**:
   ```bash
   docker-compose ps
   ```

### 本地開發

1. **安裝 Python 依賴**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **設定環境變數**:
   ```bash
   cp .env.example .env
   # 編輯 .env 檔案設定資料庫連線
   ```

3. **啟動 MongoDB** (需要先安裝 MongoDB):
   ```bash
   mongod
   ```

4. **啟動 Flask 應用程式**:
   ```bash
   python app.py
   ```

## API 端點

### 身份驗證
- `POST /api/auth/register` - 使用者註冊
- `POST /api/auth/login` - 使用者登入
- `GET /api/auth/me` - 取得目前使用者資訊
- `POST /api/auth/logout` - 使用者登出

### 使用者管理
- `POST /api/users/register` - 使用者註冊 (向後相容)
- `POST /api/users/login` - 使用者登入 (向後相容)
- `GET /api/users/profile` - 取得個人資料
- `PUT /api/users/profile` - 更新個人資料

## API 使用範例

### 註冊新使用者
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

### 使用者登入
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "student@example.com",
    "password": "password123"
  }'
```

### 取得使用者資訊 (需要 JWT Token)
```bash
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 服務存取

啟動後可存取以下服務：

- **Flask API**: http://localhost:5000
- **前端網站**: http://localhost:3000
- **MongoDB**: localhost:27017
- **Mongo Express** (資料庫管理): http://localhost:8081
  - 帳號: admin
  - 密碼: admin123

## 資料庫結構

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

## 開發指令

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

## 環境變數

編輯 `.env` 檔案設定以下變數：

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

# 應用程式設定
PORT=5000
HOST=0.0.0.0
```

## 注意事項

1. **安全性**: 在生產環境中請務必更改預設的密鑰和密碼
2. **CORS**: 目前設定為允許所有來源，生產環境請限制特定域名
3. **JWT**: Token 過期時間可在環境變數中調整
4. **資料庫**: MongoDB 資料會持久化在 Docker volume 中

## 故障排除

### 常見問題

1. **MongoDB 連線失敗**:
   - 確認 MongoDB 服務正在運行
   - 檢查 `MONGODB_URI` 設定

2. **JWT Token 錯誤**:
   - 檢查 `JWT_SECRET_KEY` 設定
   - 確認 Token 格式正確

3. **CORS 錯誤**:
   - 檢查前端請求的域名
   - 確認 Flask-CORS 設定

### 查看日誌
```bash
# 查看後端日誌
docker-compose logs backend

# 查看 MongoDB 日誌
docker-compose logs mongodb

# 查看所有服務日誌
docker-compose logs
```
