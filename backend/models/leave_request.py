from datetime import datetime
from bson import ObjectId
from config.database import db

class LeaveRequest:
    def __init__(self, user_id, leave_type, start_date, end_date, reason, **kwargs):
        self.user_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
        self.leave_type = leave_type
        self.start_date = start_date
        self.end_date = end_date
        self.reason = reason
        self.status = kwargs.get('status', 'pending')  # pending, approved, rejected
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        
        # 可選欄位
        self.emergency_contact = kwargs.get('emergency_contact', '')
        self.teacher_note = kwargs.get('teacher_note', '')
        self.attachment_url = kwargs.get('attachment_url', '')
        self.approved_by = kwargs.get('approved_by', None)
        self.approved_at = kwargs.get('approved_at', None)
        self.rejected_reason = kwargs.get('rejected_reason', '')
    
    def to_dict(self):
        """轉換為字典格式"""
        return {
            '_id': str(self._id) if hasattr(self, '_id') else None,
            'user_id': str(self.user_id),
            'leave_type': self.leave_type,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, datetime) else self.start_date,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, datetime) else self.end_date,
            'reason': self.reason,
            'status': self.status,
            'emergency_contact': self.emergency_contact,
            'teacher_note': self.teacher_note,
            'attachment_url': self.attachment_url,
            'approved_by': str(self.approved_by) if self.approved_by else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'rejected_reason': self.rejected_reason,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'updated_at': self.updated_at.isoformat() if isinstance(self.updated_at, datetime) else self.updated_at
        }
    
    def save(self):
        """儲存請假申請到資料庫"""
        collection = db.get_collection('leave_requests')
        leave_data = {
            'user_id': self.user_id,
            'leave_type': self.leave_type,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'reason': self.reason,
            'status': self.status,
            'emergency_contact': self.emergency_contact,
            'teacher_note': self.teacher_note,
            'attachment_url': self.attachment_url,
            'approved_by': self.approved_by,
            'approved_at': self.approved_at,
            'rejected_reason': self.rejected_reason,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
        
        result = collection.insert_one(leave_data)
        self._id = result.inserted_id
        return str(self._id)
    
    def update(self, **kwargs):
        """更新請假申請"""
        collection = db.get_collection('leave_requests')
        
        # 可更新的欄位
        update_data = {}
        for field in ['status', 'teacher_note', 'approved_by', 'approved_at', 'rejected_reason']:
            if field in kwargs:
                update_data[field] = kwargs[field]
                setattr(self, field, kwargs[field])
        
        update_data['updated_at'] = datetime.utcnow()
        self.updated_at = update_data['updated_at']
        
        collection.update_one(
            {'_id': self._id},
            {'$set': update_data}
        )
        return True
    
    @staticmethod
    def validate_dates(start_date, end_date):
        """驗證日期"""
        try:
            if isinstance(start_date, str):
                start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            if isinstance(end_date, str):
                end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            
            # 檢查開始日期不能早於今天
            today = datetime.now().date()
            if start_date.date() < today:
                return False, "開始日期不能早於今天"
            
            # 檢查結束日期不能早於開始日期
            if end_date.date() < start_date.date():
                return False, "結束日期不能早於開始日期"
            
            return True, "日期驗證通過"
        except Exception as e:
            return False, f"日期格式錯誤: {str(e)}"
    
    @classmethod
    def find_by_user_id(cls, user_id, limit=None, status=None):
        """根據使用者 ID 查找請假申請"""
        collection = db.get_collection('leave_requests')
        
        query = {'user_id': ObjectId(user_id) if isinstance(user_id, str) else user_id}
        if status:
            query['status'] = status
        
        cursor = collection.find(query).sort('created_at', -1)
        if limit:
            cursor = cursor.limit(limit)
        
        requests = []
        for request_data in cursor:
            leave_request = cls.__new__(cls)
            leave_request._id = request_data['_id']
            leave_request.user_id = request_data['user_id']
            leave_request.leave_type = request_data['leave_type']
            leave_request.start_date = request_data['start_date']
            leave_request.end_date = request_data['end_date']
            leave_request.reason = request_data['reason']
            leave_request.status = request_data['status']
            leave_request.emergency_contact = request_data.get('emergency_contact', '')
            leave_request.teacher_note = request_data.get('teacher_note', '')
            leave_request.attachment_url = request_data.get('attachment_url', '')
            leave_request.approved_by = request_data.get('approved_by')
            leave_request.approved_at = request_data.get('approved_at')
            leave_request.rejected_reason = request_data.get('rejected_reason', '')
            leave_request.created_at = request_data['created_at']
            leave_request.updated_at = request_data['updated_at']
            requests.append(leave_request)
        
        return requests
    
    @classmethod
    def find_by_id(cls, request_id):
        """根據 ID 查找請假申請"""
        collection = db.get_collection('leave_requests')
        try:
            request_data = collection.find_one({'_id': ObjectId(request_id)})
        except:
            return None
            
        if request_data:
            leave_request = cls.__new__(cls)
            leave_request._id = request_data['_id']
            leave_request.user_id = request_data['user_id']
            leave_request.leave_type = request_data['leave_type']
            leave_request.start_date = request_data['start_date']
            leave_request.end_date = request_data['end_date']
            leave_request.reason = request_data['reason']
            leave_request.status = request_data['status']
            leave_request.emergency_contact = request_data.get('emergency_contact', '')
            leave_request.teacher_note = request_data.get('teacher_note', '')
            leave_request.attachment_url = request_data.get('attachment_url', '')
            leave_request.approved_by = request_data.get('approved_by')
            leave_request.approved_at = request_data.get('approved_at')
            leave_request.rejected_reason = request_data.get('rejected_reason', '')
            leave_request.created_at = request_data['created_at']
            leave_request.updated_at = request_data['updated_at']
            return leave_request
        return None
    
    @classmethod
    def find_all_pending(cls, limit=None):
        """查找所有待審核的請假申請"""
        collection = db.get_collection('leave_requests')
        
        cursor = collection.find({'status': 'pending'}).sort('created_at', 1)
        if limit:
            cursor = cursor.limit(limit)
        
        requests = []
        for request_data in cursor:
            leave_request = cls.__new__(cls)
            leave_request._id = request_data['_id']
            leave_request.user_id = request_data['user_id']
            leave_request.leave_type = request_data['leave_type']
            leave_request.start_date = request_data['start_date']
            leave_request.end_date = request_data['end_date']
            leave_request.reason = request_data['reason']
            leave_request.status = request_data['status']
            leave_request.emergency_contact = request_data.get('emergency_contact', '')
            leave_request.teacher_note = request_data.get('teacher_note', '')
            leave_request.attachment_url = request_data.get('attachment_url', '')
            leave_request.approved_by = request_data.get('approved_by')
            leave_request.approved_at = request_data.get('approved_at')
            leave_request.rejected_reason = request_data.get('rejected_reason', '')
            leave_request.created_at = request_data['created_at']
            leave_request.updated_at = request_data['updated_at']
            requests.append(leave_request)
        
        return requests
