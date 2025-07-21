#!/usr/bin/env python3
"""
學生請假系統 API 測試腳本
"""

import requests
import json
import time

# API 基礎 URL
BASE_URL = "http://localhost:5000"

def test_api():
    print("🧪 開始測試學生請假系統 API...")
    print("=" * 50)
    
    # 測試資料
    test_user = {
        "email": "test@example.com",
        "password": "test123",
        "name": "測試使用者",
        "student_id": "T001"
    }
    
    # 1. 測試使用者註冊
    print("\n1️⃣ 測試使用者註冊...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/auth/register",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {response.json()}")
        
        if response.status_code == 201:
            print("✅ 註冊成功")
        elif response.status_code == 409:
            print("⚠️ 使用者已存在")
        else:
            print("❌ 註冊失敗")
    except Exception as e:
        print(f"❌ 註冊請求失敗: {e}")
    
    # 2. 測試使用者登入
    print("\n2️⃣ 測試使用者登入...")
    try:
        login_data = {
            "email": test_user["email"],
            "password": test_user["password"]
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"回應: {result}")
        
        if response.status_code == 200 and "token" in result:
            print("✅ 登入成功")
            token = result["token"]
            
            # 3. 測試取得使用者資訊
            print("\n3️⃣ 測試取得使用者資訊...")
            try:
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
                print(f"狀態碼: {response.status_code}")
                print(f"回應: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ 取得使用者資訊成功")
                else:
                    print("❌ 取得使用者資訊失敗")
            except Exception as e:
                print(f"❌ 取得使用者資訊請求失敗: {e}")
            
            # 4. 測試更新個人資料
            print("\n4️⃣ 測試更新個人資料...")
            try:
                update_data = {
                    "name": "測試使用者(已更新)",
                    "student_id": "T001-UPDATED"
                }
                response = requests.put(
                    f"{BASE_URL}/api/users/profile",
                    json=update_data,
                    headers=headers
                )
                print(f"狀態碼: {response.status_code}")
                print(f"回應: {response.json()}")
                
                if response.status_code == 200:
                    print("✅ 更新個人資料成功")
                else:
                    print("❌ 更新個人資料失敗")
            except Exception as e:
                print(f"❌ 更新個人資料請求失敗: {e}")
                
        else:
            print("❌ 登入失敗")
    except Exception as e:
        print(f"❌ 登入請求失敗: {e}")
    
    # 5. 測試錯誤情況
    print("\n5️⃣ 測試錯誤情況...")
    try:
        # 測試錯誤的登入資訊
        wrong_login = {
            "email": "wrong@example.com",
            "password": "wrongpassword"
        }
        response = requests.post(
            f"{BASE_URL}/api/auth/login",
            json=wrong_login,
            headers={"Content-Type": "application/json"}
        )
        print(f"錯誤登入狀態碼: {response.status_code}")
        if response.status_code == 401:
            print("✅ 錯誤登入正確回傳 401")
        else:
            print("❌ 錯誤登入回應異常")
    except Exception as e:
        print(f"❌ 錯誤情況測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 API 測試完成")

def check_services():
    """檢查服務是否正常運行"""
    print("🔍 檢查服務狀態...")
    
    services = {
        "後端 API": "http://localhost:5000",
        "前端網站": "http://localhost:3000",
        "資料庫管理": "http://localhost:8081"
    }
    
    for name, url in services.items():
        try:
            response = requests.get(url, timeout=5)
            if response.status_code < 400:
                print(f"✅ {name}: 運行正常 ({url})")
            else:
                print(f"⚠️ {name}: 回應異常 {response.status_code} ({url})")
        except requests.exceptions.RequestException:
            print(f"❌ {name}: 無法連接 ({url})")
    
    print()

if __name__ == "__main__":
    print("學生請假系統 API 測試工具")
    print("確保 Docker 服務已啟動: docker-compose up -d")
    print()
    
    # 等待服務啟動
    print("⏳ 等待服務啟動...")
    time.sleep(2)
    
    # 檢查服務狀態
    check_services()
    
    # 執行 API 測試
    test_api()
