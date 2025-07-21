from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from datetime import timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """使用者註冊"""
    try:
        data = request.get_json()
        
        # 檢查必要欄位
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': '請提供 email 和密碼'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # 驗證 email 格式
        if not User.validate_email(email):
            return jsonify({'message': '請輸入正確的 Email 格式'}), 400
        
        # 驗證密碼強度
        if not User.validate_password(password):
            return jsonify({'message': '密碼長度至少 6 碼'}), 400
        
        # 檢查 email 是否已存在
        if User.email_exists(email):
            return jsonify({'message': '此 Email 已被註冊'}), 409
        
        # 建立新使用者
        user = User(
            email=email,
            password=password,
            role=data.get('role', 'student'),
            name=data.get('name', ''),
            student_id=data.get('student_id', '')
        )
        
        user_id = user.save()
        
        return jsonify({
            'message': '註冊成功',
            'user_id': user_id,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'註冊失敗: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """使用者登入"""
    try:
        data = request.get_json()
        
        # 檢查必要欄位
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'message': '請提供 email 和密碼'}), 400
        
        email = data['email'].lower().strip()
        password = data['password']
        
        # 查找使用者
        user = User.find_by_email(email)
        if not user:
            return jsonify({'message': 'Email 或密碼錯誤'}), 401
        
        # 檢查密碼
        if not user.check_password(password):
            return jsonify({'message': 'Email 或密碼錯誤'}), 401
        
        # 檢查帳號是否啟用
        if not user.is_active:
            return jsonify({'message': '帳號已被停用'}), 401
        
        # 建立 JWT token
        access_token = create_access_token(
            identity=str(user._id),
            expires_delta=timedelta(seconds=int(3600))
        )
        
        return jsonify({
            'message': '登入成功',
            'token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'登入失敗: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """取得目前登入使用者資訊"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': '使用者不存在'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'取得使用者資訊失敗: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """使用者登出"""
    # 注意：JWT 是無狀態的，真正的登出需要在前端刪除 token
    # 或者實作 token 黑名單機制
    return jsonify({'message': '登出成功'}), 200
