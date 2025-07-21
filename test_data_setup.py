#!/usr/bin/env python3
"""
學生請假系統測試腳本
用於創建測試用戶和請假申請資料
"""

import requests
import json
from datetime import datetime, timedelta

# API 基礎 URL
BASE_URL = "http://localhost:5000/api"

def test_user_registration():
    """測試用戶註冊"""
    print("=== 測試用戶註冊 ===")
    
    # 測試用戶資料
    users = [
        {
            "email": "student1@example.com",
            "password": "password123",
            "name": "王小明",
            "student_id": "S20231001",
            "role": "student"
        },
        {
            "email": "student2@example.com",
            "password": "password123",
            "name": "李小華",
            "student_id": "S20231002",
            "role": "student"
        },
        {
            "email": "teacher1@example.com",
            "password": "password123",
            "name": "張老師",
            "student_id": "",
            "role": "teacher"
        },
        {
            "email": "admin1@example.com",
            "password": "password123",
            "name": "林管理員",
            "student_id": "",
            "role": "admin"
        }
    ]
    
    registered_users = []
    
    for user in users:
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json=user)
            if response.status_code == 201:
                print(f"✅ 註冊成功: {user['name']} ({user['email']})")
                registered_users.append(user)
            else:
                print(f"❌ 註冊失敗: {user['name']} - {response.json().get('message', '未知錯誤')}")
        except Exception as e:
            print(f"❌ 網路錯誤: {user['name']} - {str(e)}")
    
    return registered_users

def test_user_login(email, password):
    """測試用戶登入"""
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": email,
            "password": password
        })
        if response.status_code == 200:
            token = response.json().get('access_token')
            print(f"✅ 登入成功: {email}")
            return token
        else:
            print(f"❌ 登入失敗: {email} - {response.json().get('message', '未知錯誤')}")
            return None
    except Exception as e:
        print(f"❌ 登入錯誤: {email} - {str(e)}")
        return None

def create_test_leave_requests(student_tokens):
    """創建測試請假申請"""
    print("\n=== 創建測試請假申請 ===")
    
    # 測試請假申請資料
    leave_requests = [
        {
            "leave_type": "sick",
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "reason": "感冒發燒，需要休息",
            "emergency_contact": "媽媽 0912-345-678"
        },
        {
            "leave_type": "personal",
            "start_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
            "reason": "家中有事需要處理",
            "emergency_contact": "爸爸 0987-654-321"
        },
        {
            "leave_type": "family",
            "start_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=6)).strftime("%Y-%m-%d"),
            "reason": "陪同家人就醫",
            "emergency_contact": "姊姊 0923-456-789"
        }
    ]
    
    created_requests = []
    
    for i, (email, token) in enumerate(student_tokens.items()):
        if i < len(leave_requests):
            request_data = leave_requests[i]
            try:
                response = requests.post(
                    f"{BASE_URL}/leave/apply",
                    json=request_data,
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 201:
                    print(f"✅ 請假申請成功: {email} - {request_data['leave_type']}")
                    created_requests.append(response.json())
                else:
                    print(f"❌ 請假申請失敗: {email} - {response.json().get('message', '未知錯誤')}")
            except Exception as e:
                print(f"❌ 申請錯誤: {email} - {str(e)}")
    
    return created_requests

def test_admin_functions(admin_token):
    """測試管理員功能"""
    print("\n=== 測試管理員功能 ===")
    
    try:
        # 獲取待審核申請
        response = requests.get(
            f"{BASE_URL}/leave/pending",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        if response.status_code == 200:
            pending_requests = response.json().get('requests', [])
            print(f"✅ 獲取待審核申請成功: {len(pending_requests)} 筆")
            
            # 測試審核功能
            if pending_requests:
                request_id = pending_requests[0]['_id']
                
                # 測試核准
                approve_response = requests.post(
                    f"{BASE_URL}/leave/approve/{request_id}",
                    json={"teacher_note": "申請資料完整，核准"},
                    headers={"Authorization": f"Bearer {admin_token}"}
                )
                
                if approve_response.status_code == 200:
                    print("✅ 核准申請成功")
                else:
                    print(f"❌ 核准申請失敗: {approve_response.json().get('message', '未知錯誤')}")
            
        else:
            print(f"❌ 獲取待審核申請失敗: {response.json().get('message', '未知錯誤')}")
    
    except Exception as e:
        print(f"❌ 管理員功能測試錯誤: {str(e)}")

def main():
    """主測試函數"""
    print("🚀 開始學生請假系統測試")
    print("=" * 50)
    
    # 1. 測試用戶註冊
    registered_users = test_user_registration()
    
    if not registered_users:
        print("❌ 沒有成功註冊的用戶，測試終止")
        return
    
    print(f"\n📊 成功註冊 {len(registered_users)} 個用戶")
    
    # 2. 測試用戶登入
    print("\n=== 測試用戶登入 ===")
    student_tokens = {}
    teacher_token = None
    admin_token = None
    
    for user in registered_users:
        token = test_user_login(user['email'], user['password'])
        if token:
            if user['role'] == 'student':
                student_tokens[user['email']] = token
            elif user['role'] == 'teacher':
                teacher_token = token
            elif user['role'] == 'admin':
                admin_token = token
    
    # 3. 創建測試請假申請
    if student_tokens:
        created_requests = create_test_leave_requests(student_tokens)
        print(f"\n📊 成功創建 {len(created_requests)} 個請假申請")
    
    # 4. 測試管理員功能
    if admin_token:
        test_admin_functions(admin_token)
    elif teacher_token:
        test_admin_functions(teacher_token)
    else:
        print("❌ 沒有管理員或老師權限，無法測試審核功能")
    
    print("\n" + "=" * 50)
    print("🎉 測試完成！")
    print("\n📋 測試摘要:")
    print(f"- 註冊用戶: {len(registered_users)} 個")
    print(f"- 學生帳號: {len(student_tokens)} 個")
    print(f"- 老師帳號: {'有' if teacher_token else '無'}")
    print(f"- 管理員帳號: {'有' if admin_token else '無'}")
    
    print("\n🌐 現在您可以使用以下帳號登入測試:")
    for user in registered_users:
        print(f"- {user['name']} ({user['role']}): {user['email']} / password123")
    
    print(f"\n🔗 前端網址: http://localhost:3000")

if __name__ == "__main__":
    main()
