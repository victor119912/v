# 學生請假系統後端

本專案為 Node.js + Express + Sequelize + MySQL 的學生請假系統後端，支援 JWT 身份驗證、角色權限、資料驗證、檔案上傳、Email/LINE 通知等功能。

## 主要功能
- RESTful API 架構
- JWT 身份驗證與角色權限控制（學生、老師、行政）
- Joi/express-validator 資料驗證
- 檔案上傳（本地或 S3）
- nodemailer Email 通知
- LINE Notify 推播
- Sequelize models：Users、LeaveRequests、LeaveTypes、Notifications

## 快速開始
1. `npm install`
2. 複製 `.env.example` 為 `.env` 並設定資料庫、JWT、Email、S3 等資訊
3. `npm run dev` 啟動伺服器
