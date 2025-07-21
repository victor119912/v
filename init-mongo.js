// MongoDB 初始化腳本
db = db.getSiblingDB('student_leave_system');

// 建立使用者集合索引
db.users.createIndex({ "email": 1 }, { unique: true });
db.users.createIndex({ "student_id": 1 });
db.users.createIndex({ "role": 1 });
db.users.createIndex({ "created_at": 1 });

// 建立請假申請集合索引 (為未來功能準備)
db.leave_requests.createIndex({ "user_id": 1 });
db.leave_requests.createIndex({ "status": 1 });
db.leave_requests.createIndex({ "start_date": 1 });
db.leave_requests.createIndex({ "created_at": 1 });

// 插入測試資料 (可選)
db.users.insertOne({
    email: "admin@example.com",
    password_hash: "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj8ukgJNGChW", // password: admin123
    role: "admin",
    name: "系統管理員",
    student_id: "",
    is_active: true,
    created_at: new Date(),
    updated_at: new Date()
});

print("MongoDB 初始化完成");
