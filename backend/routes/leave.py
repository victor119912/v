from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.leave_request import LeaveRequest
from models.user import User
from datetime import datetime

leave_bp = Blueprint('leave', __name__)

@leave_bp.route('/types', methods=['GET'])
@jwt_required()
def get_leave_types():
    """取得請假類型清單"""
    leave_types = [
        {'id': 'sick', 'name': '病假', 'description': '因生病需要請假'},
        {'id': 'personal', 'name': '事假', 'description': '因私人事務需要請假'},
        {'id': 'family', 'name': '家事假', 'description': '因家庭事務需要請假'},
        {'id': 'funeral', 'name': '喪假', 'description': '因家屬過世需要請假'},
        {'id': 'maternity', 'name': '產假', 'description': '因生產需要請假'},
        {'id': 'emergency', 'name': '緊急假', 'description': '因緊急事件需要請假'}
    ]
    
    return jsonify({
        'leave_types': leave_types
    }), 200

@leave_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_leave():
    """申請請假"""
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # 檢查必要欄位
        required_fields = ['leave_type', 'start_date', 'end_date', 'reason']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'message': f'缺少必要欄位: {field}'}), 400
        
        # 驗證日期
        is_valid, date_message = LeaveRequest.validate_dates(
            data['start_date'], 
            data['end_date']
        )
        if not is_valid:
            return jsonify({'message': date_message}), 400
        
        # 轉換日期格式
        try:
            start_date = datetime.fromisoformat(data['start_date'].replace('Z', '+00:00'))
            end_date = datetime.fromisoformat(data['end_date'].replace('Z', '+00:00'))
        except Exception as e:
            return jsonify({'message': f'日期格式錯誤: {str(e)}'}), 400
        
        # 建立請假申請
        leave_request = LeaveRequest(
            user_id=user_id,
            leave_type=data['leave_type'],
            start_date=start_date,
            end_date=end_date,
            reason=data['reason'],
            emergency_contact=data.get('emergency_contact', '')
        )
        
        request_id = leave_request.save()
        
        return jsonify({
            'message': '請假申請提交成功',
            'request_id': request_id,
            'leave_request': leave_request.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'message': f'申請請假失敗: {str(e)}'}), 500

@leave_bp.route('/my-requests', methods=['GET'])
@jwt_required()
def get_my_requests():
    """取得我的請假申請記錄"""
    try:
        user_id = get_jwt_identity()
        
        # 取得查詢參數
        status = request.args.get('status')  # pending, approved, rejected
        limit = request.args.get('limit', type=int)
        
        # 查找請假申請
        requests = LeaveRequest.find_by_user_id(user_id, limit=limit, status=status)
        
        # 轉換為字典格式
        requests_data = [req.to_dict() for req in requests]
        
        return jsonify({
            'requests': requests_data,
            'total': len(requests_data)
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'取得請假記錄失敗: {str(e)}'}), 500

@leave_bp.route('/pending', methods=['GET'])
@jwt_required()
def get_pending_requests():
    """獲取待審核申請 (僅限老師和管理員)"""
    try:
        current_user = get_jwt_identity()
        user = User.find_by_email(current_user)
        
        if not user:
            return jsonify({'message': '使用者不存在'}), 404
            
        # 檢查權限 - 僅老師和管理員可以查看
        if user.role not in ['teacher', 'admin']:
            return jsonify({'message': '沒有權限查看待審核申請'}), 403
            
        # 獲取所有待審核申請
        requests = LeaveRequest.find_all_pending()
        
        # 轉換為JSON格式並加入申請人資訊
        requests_data = []
        for request in requests:
            request_dict = request.to_dict()
            # 添加申請人資訊
            applicant = User.find_by_id(request.user_id)
            if applicant:
                request_dict['applicant'] = {
                    'name': applicant.name,
                    'email': applicant.email,
                    'student_id': applicant.student_id
                }
            requests_data.append(request_dict)
            
        return jsonify({
            'message': '獲取待審核申請成功',
            'requests': requests_data
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'獲取待審核申請失敗: {str(e)}'}), 500

@leave_bp.route('/request/<request_id>', methods=['GET'])
@jwt_required()
def get_request_detail(request_id):
    """取得請假申請詳細資訊"""
    try:
        user_id = get_jwt_identity()
        current_user = User.find_by_id(user_id)
        
        # 查找請假申請
        leave_request = LeaveRequest.find_by_id(request_id)
        if not leave_request:
            return jsonify({'message': '請假申請不存在'}), 404
        
        # 檢查權限（只有申請人和管理員可以查看）
        if str(leave_request.user_id) != user_id and current_user.role not in ['teacher', 'admin']:
            return jsonify({'message': '無權限查看此請假申請'}), 403
        
        # 如果是管理員查看，加入申請人資訊
        request_data = leave_request.to_dict()
        if current_user.role in ['teacher', 'admin']:
            applicant = User.find_by_id(str(leave_request.user_id))
            if applicant:
                request_data['applicant'] = {
                    'name': applicant.name,
                    'email': applicant.email,
                    'student_id': applicant.student_id
                }
        
        return jsonify({
            'request': request_data
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'取得請假申請詳情失敗: {str(e)}'}), 500

@leave_bp.route('/approve/<request_id>', methods=['POST'])
@jwt_required()
def approve_request(request_id):
    """核准請假申請（僅老師和管理員）"""
    try:
        user_id = get_jwt_identity()
        current_user = User.find_by_id(user_id)
        
        # 檢查權限
        if current_user.role not in ['teacher', 'admin']:
            return jsonify({'message': '無權限審核請假申請'}), 403
        
        # 查找請假申請
        leave_request = LeaveRequest.find_by_id(request_id)
        if not leave_request:
            return jsonify({'message': '請假申請不存在'}), 404
        
        if leave_request.status != 'pending':
            return jsonify({'message': '此請假申請已被處理'}), 400
        
        data = request.get_json() or {}
        teacher_note = data.get('teacher_note', '')
        
        # 更新申請狀態
        leave_request.update(
            status='approved',
            approved_by=user_id,
            approved_at=datetime.utcnow(),
            teacher_note=teacher_note
        )
        
        return jsonify({
            'message': '請假申請已核准',
            'request': leave_request.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'核准請假申請失敗: {str(e)}'}), 500

@leave_bp.route('/reject/<request_id>', methods=['POST'])
@jwt_required()
def reject_request(request_id):
    """拒絕請假申請（僅老師和管理員）"""
    try:
        user_id = get_jwt_identity()
        current_user = User.find_by_id(user_id)
        
        # 檢查權限
        if current_user.role not in ['teacher', 'admin']:
            return jsonify({'message': '無權限審核請假申請'}), 403
        
        # 查找請假申請
        leave_request = LeaveRequest.find_by_id(request_id)
        if not leave_request:
            return jsonify({'message': '請假申請不存在'}), 404
        
        if leave_request.status != 'pending':
            return jsonify({'message': '此請假申請已被處理'}), 400
        
        data = request.get_json() or {}
        rejected_reason = data.get('rejected_reason', '')
        teacher_note = data.get('teacher_note', '')
        
        if not rejected_reason:
            return jsonify({'message': '請提供拒絕原因'}), 400
        
        # 更新申請狀態
        leave_request.update(
            status='rejected',
            approved_by=user_id,
            approved_at=datetime.utcnow(),
            rejected_reason=rejected_reason,
            teacher_note=teacher_note
        )
        
        return jsonify({
            'message': '請假申請已拒絕',
            'request': leave_request.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'message': f'拒絕請假申請失敗: {str(e)}'}), 500
