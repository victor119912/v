from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from config.database import db
import re

class User:
    def __init__(self, email, password, role='student', **kwargs):
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # 可選欄位
        self.name = kwargs.get('name', '')
        self.student_id = kwargs.get('student_id', '')
        self.is_active = kwargs.get('is_active', True)
    
    def to_dict(self):
        """轉換為字典格式（不包含密碼）"""
        return {
            '_id': str(self._id) if hasattr(self, '_id') else None,
            'email': self.email,
            'role': self.role,
            'name': self.name,
            'student_id': self.student_id,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    def save(self):
        """儲存使用者到資料庫"""
        collection = db.get_collection('users')
        user_data = {
            'email': self.email,
            'password_hash': self.password_hash,
            'role': self.role,
            'name': self.name,
            'student_id': self.student_id,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        result = collection.insert_one(user_data)
        self._id = result.inserted_id
        return str(self._id)
    
    def check_password(self, password):
        """檢查密碼是否正確"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def validate_email(email):
        """驗證 email 格式"""
        pattern = r'^[^@\s]+@[^@\s]+\.[^@\s]+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password):
        """驗證密碼強度"""
        return len(password) >= 6
    
    @classmethod
    def find_by_email(cls, email):
        """根據 email 查找使用者"""
        collection = db.get_collection('users')
        user_data = collection.find_one({'email': email})
        
        if user_data:
            user = cls.__new__(cls)
            user._id = user_data['_id']
            user.email = user_data['email']
            user.password_hash = user_data['password_hash']
            user.role = user_data['role']
            user.name = user_data.get('name', '')
            user.student_id = user_data.get('student_id', '')
            user.is_active = user_data.get('is_active', True)
            user.created_at = user_data['created_at']
            user.updated_at = user_data['updated_at']
            return user
        return None
    
    @classmethod
    def find_by_id(cls, user_id):
        """根據 ID 查找使用者"""
        collection = db.get_collection('users')
        try:
            user_data = collection.find_one({'_id': ObjectId(user_id)})
        except:
            return None
            
        if user_data:
            user = cls.__new__(cls)
            user._id = user_data['_id']
            user.email = user_data['email']
            user.password_hash = user_data['password_hash']
            user.role = user_data['role']
            user.name = user_data.get('name', '')
            user.student_id = user_data.get('student_id', '')
            user.is_active = user_data.get('is_active', True)
            user.created_at = user_data['created_at']
            user.updated_at = user_data['updated_at']
            return user
        return None
    
    @classmethod
    def email_exists(cls, email):
        """檢查 email 是否已存在"""
        collection = db.get_collection('users')
        return collection.find_one({'email': email}) is not None
