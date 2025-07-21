#!/usr/bin/env python3
"""
測試老師審核功能
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_teacher_review():
    """測試老師審核功能"""
    
    # 老師登入
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "teacher1@example.com",
        "password": "password123"
    })
    
    if login_response.status_code != 200:
        print("❌ 老師登入失敗")
        print(f"錯誤: {login_response.json()}")
        return
    
    token = login_response.json().get('token')
    print("✅ 老師登入成功")
    
    # 獲取待審核申請
    response = requests.get(
        f"{BASE_URL}/leave/pending",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        data = response.json()
        requests_list = data.get('requests', [])
        print(f"✅ 獲取待審核申請成功: {len(requests_list)} 筆")
        
        for i, req in enumerate(requests_list):
            print(f"\n申請 {i+1}:")
            print(f"  ID: {req['_id']}")
            print(f"  申請人: {req.get('applicant', {}).get('name', '未知')}")
            print(f"  類型: {req['leave_type']}")
            print(f"  期間: {req['start_date']} 至 {req['end_date']}")
            print(f"  原因: {req['reason'][:50]}...")
        
        # 測試審核功能
        if requests_list:
            first_request = requests_list[0]
            request_id = first_request['_id']
            
            print(f"\n測試核准申請: {request_id}")
            approve_response = requests.post(
                f"{BASE_URL}/leave/approve/{request_id}",
                json={"teacher_note": "申請資料完整，同意核准"},
                headers={"Authorization": f"Bearer {token}"}
            )
            
            if approve_response.status_code == 200:
                print("✅ 核准申請成功")
            else:
                print(f"❌ 核准申請失敗: {approve_response.json()}")
    else:
        print(f"❌ 獲取待審核申請失敗: {response.json()}")

if __name__ == "__main__":
    test_teacher_review()
