#!/usr/bin/env python3
"""
簡化的請假申請創建腳本
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def create_leave_request():
    """創建請假申請"""
    
    # 先登入學生帳號
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "student1@example.com",
        "password": "password123"
    })
    
    if login_response.status_code != 200:
        print("❌ 學生登入失敗")
        return
    
    token = login_response.json().get('token')  # 改為 'token'
    print("✅ 學生登入成功")
    if token:
        print(f"Token: {token[:50]}...")  # 顯示token的前50個字符
    else:
        print("❌ 沒有收到token")
        print(f"回應內容: {login_response.json()}")
        return
    
    # 創建請假申請
    leave_data = {
        "leave_type": "sick",
        "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
        "reason": "感冒發燒，需要休息治療",
        "emergency_contact": "媽媽 0912-345-678"
    }
    
    response = requests.post(
        f"{BASE_URL}/leave/apply",
        json=leave_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 201:
        print("✅ 請假申請創建成功")
        print(f"申請ID: {response.json().get('request_id')}")
    else:
        print(f"❌ 請假申請失敗 (狀態碼: {response.status_code})")
        try:
            error_data = response.json()
            print(f"錯誤訊息: {error_data}")
        except:
            print(f"回應內容: {response.text}")
    
    # 創建第二個請假申請
    leave_data2 = {
        "leave_type": "personal",
        "start_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
        "reason": "家中有重要事務需要處理",
        "emergency_contact": "爸爸 0987-654-321"
    }
    
    response2 = requests.post(
        f"{BASE_URL}/leave/apply",
        json=leave_data2,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response2.status_code == 201:
        print("✅ 第二個請假申請創建成功")
        print(f"申請ID: {response2.json().get('request_id')}")
    else:
        print(f"❌ 第二個請假申請失敗 (狀態碼: {response2.status_code})")
        try:
            error_data = response2.json()
            print(f"錯誤訊息: {error_data}")
        except:
            print(f"回應內容: {response2.text}")

if __name__ == "__main__":
    create_leave_request()
