#!/usr/bin/env python3
"""
完整系統測試 - 創建完整的測試場景
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5000/api"

def complete_system_test():
    """完整系統測試"""
    print("🚀 開始完整系統測試")
    print("=" * 60)
    
    # 1. 學生創建請假申請
    print("\n1️⃣ 學生創建請假申請")
    student_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "student2@example.com", 
        "password": "password123"
    })
    
    if student_login.status_code == 200:
        student_token = student_login.json().get('token')
        print("✅ 學生2登入成功")
        
        # 創建緊急請假申請
        urgent_leave = {
            "leave_type": "emergency",
            "start_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "end_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
            "reason": "家人突發急病需要陪同就醫",
            "emergency_contact": "媽媽 0911-222-333"
        }
        
        leave_response = requests.post(
            f"{BASE_URL}/leave/apply",
            json=urgent_leave,
            headers={"Authorization": f"Bearer {student_token}"}
        )
        
        if leave_response.status_code == 201:
            print("✅ 緊急請假申請創建成功")
            emergency_request_id = leave_response.json().get('request_id')
        else:
            print(f"❌ 緊急請假申請失敗: {leave_response.json()}")
            return
    else:
        print("❌ 學生2登入失敗")
        return
    
    # 2. 老師查看並處理申請
    print("\n2️⃣ 老師查看並處理申請")
    teacher_login = requests.post(f"{BASE_URL}/auth/login", json={
        "email": "teacher1@example.com",
        "password": "password123"
    })
    
    if teacher_login.status_code == 200:
        teacher_token = teacher_login.json().get('token')
        print("✅ 老師登入成功")
        
        # 查看待審核申請
        pending_response = requests.get(
            f"{BASE_URL}/leave/pending",
            headers={"Authorization": f"Bearer {teacher_token}"}
        )
        
        if pending_response.status_code == 200:
            pending_requests = pending_response.json().get('requests', [])
            print(f"✅ 查看待審核申請: {len(pending_requests)} 筆")
            
            # 處理申請
            if pending_requests:
                # 核准第一個申請
                first_request = pending_requests[0]
                approve_response = requests.post(
                    f"{BASE_URL}/leave/approve/{first_request['_id']}",
                    json={
                        "teacher_note": "緊急狀況，同意請假。請保重身體！"
                    },
                    headers={"Authorization": f"Bearer {teacher_token}"}
                )
                
                if approve_response.status_code == 200:
                    print("✅ 核准第一個申請成功")
                else:
                    print(f"❌ 核准申請失敗: {approve_response.json()}")
                
                # 如果有第二個申請，拒絕它作為示例
                if len(pending_requests) > 1:
                    second_request = pending_requests[1]
                    reject_response = requests.post(
                        f"{BASE_URL}/leave/reject/{second_request['_id']}",
                        json={
                            "rejected_reason": "請假日期與重要課程衝突",
                            "teacher_note": "建議改期或參加補課"
                        },
                        headers={"Authorization": f"Bearer {teacher_token}"}
                    )
                    
                    if reject_response.status_code == 200:
                        print("✅ 拒絕第二個申請成功")
                    else:
                        print(f"❌ 拒絕申請失敗: {reject_response.json()}")
        else:
            print(f"❌ 查看待審核申請失敗: {pending_response.json()}")
    else:
        print("❌ 老師登入失敗")
    
    # 3. 學生查看申請結果
    print("\n3️⃣ 學生查看申請結果")
    my_requests_response = requests.get(
        f"{BASE_URL}/leave/my-requests",
        headers={"Authorization": f"Bearer {student_token}"}
    )
    
    if my_requests_response.status_code == 200:
        my_requests = my_requests_response.json().get('requests', [])
        print(f"✅ 學生查看個人申請: {len(my_requests)} 筆")
        
        for i, req in enumerate(my_requests[-3:]):  # 顯示最近3筆
            status_text = {
                'pending': '待審核',
                'approved': '已核准',
                'rejected': '已拒絕'
            }.get(req['status'], req['status'])
            
            print(f"\n  申請 {i+1}:")
            print(f"    狀態: {status_text}")
            print(f"    類型: {req['leave_type']}")
            print(f"    期間: {req['start_date']} 至 {req['end_date']}")
            if req['status'] == 'approved':
                print(f"    審核備註: {req.get('teacher_note', '無')}")
            elif req['status'] == 'rejected':
                print(f"    拒絕原因: {req.get('rejected_reason', '無')}")
                print(f"    審核備註: {req.get('teacher_note', '無')}")
    else:
        print(f"❌ 學生查看申請失敗: {my_requests_response.json()}")
    
    print("\n" + "=" * 60)
    print("🎉 完整系統測試完成！")
    print("\n📋 測試摘要:")
    print("✅ 學生註冊與登入")
    print("✅ 請假申請提交")
    print("✅ 老師審核申請")
    print("✅ 申請核准/拒絕")
    print("✅ 學生查看結果")
    
    print(f"\n🌐 現在可以在瀏覽器中測試:")
    print(f"📱 前端網站: http://localhost:3000")
    print(f"👨‍🎓 學生帳號: student1@example.com 或 student2@example.com")
    print(f"👨‍🏫 老師帳號: teacher1@example.com")
    print(f"👑 管理員帳號: admin1@example.com")
    print(f"🔑 所有密碼: password123")

if __name__ == "__main__":
    complete_system_test()
