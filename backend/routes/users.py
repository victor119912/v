from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User

users_bp = Blueprint('users', __name__)

# 為了向後相容，保留原有的 /register 和 /login 路由
@users_bp.route('/register', methods=['POST'])
def register():
    """使用者註冊 (向後相容)"""
    from routes.auth import register as auth_register
    return auth_register()

@users_bp.route('/login', methods=['POST'])
def login():
    """使用者登入 (向後相容)"""
    from routes.auth import login as auth_login
    return auth_login()

@users_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """取得使用者個人資料"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': '使用者不存在'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'取得個人資料失敗: {str(e)}'}), 500

@users_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """更新使用者個人資料"""
    try:
        user_id = get_jwt_identity()
        user = User.find_by_id(user_id)
        
        if not user:
            return jsonify({'message': '使用者不存在'}), 404
        
        data = request.get_json()
        
        # 可更新的欄位
        if 'name' in data:
            user.name = data['name']
        if 'student_id' in data:
            user.student_id = data['student_id']
        
        # 更新時間
        from datetime import datetime
        user.updated_at = datetime.utcnow()
        
        # 儲存到資料庫
        from config.database import db
        collection = db.get_collection('users')
        collection.update_one(
            {'_id': user._id},
            {'$set': {
                'name': user.name,
                'student_id': user.student_id,
                'updated_at': user.updated_at
            }}
        )
        
        return jsonify({
            'message': '個人資料更新成功',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'更新個人資料失敗: {str(e)}'}), 500
