from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models.user import User
from flask_jwt_extended import jwt_required
from datetime import datetime
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__)

# 🔧 工具函式：安全地轉換日期
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    except:
        return None

# ✅ 新增使用者
@user_bp.route('/api/users', methods=['POST'])
@jwt_required()
def create_user():
    data = request.get_json()
    print("📥 收到新增資料:", data)

    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'msg': '帳號已存在'}), 400

    if not data.get('password'):
        return jsonify({'msg': '密碼為必填'}), 400

    try:
        new_user = User(
            username=data.get('username'),
            password_hash=generate_password_hash(data.get('password')),
            declare_name=data.get('declare_name'),
            department_id=data.get('department_id'),
            practice_start=parse_date(data.get('practice_start')),
            practice_end=parse_date(data.get('practice_end')),
            onboard=datetime.utcnow(),
            resignation_day=None if data.get('status') == '在職' else datetime.utcnow(),
            role='staff'
        )

        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': '使用者新增成功'}), 201

    except Exception as e:
        db.session.rollback()
        print("❌ 新增使用者錯誤:", e)
        return jsonify({'msg': '新增失敗', 'error': str(e)}), 500

# ✅ 取得所有使用者（使用者管理頁）
@user_bp.route('/api/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            'id': u.id,
            'username': u.username,
            'role': u.role,
            'declare_name': u.declare_name,
            'department': u.department.dpname if u.department else None,
            'department_id': u.department_id,
            'practice_start': u.practice_start.isoformat() if u.practice_start else '',
            'practice_end': u.practice_end.isoformat() if u.practice_end else '',
            'status': '在職' if not u.resignation_day else '離職'
        })
    return jsonify(result)

# ✅ 取得單一使用者（支援 /users/:id 頁面）
@user_bp.route('/api/users/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '找不到使用者'}), 404

    # 判斷是否需要詳細資料
    detail = request.args.get('detail', 'false').lower() == 'true'

    if detail:
        # 詳細個人頁資料（UserProfile.vue 使用）
        return jsonify({
            'id': user.id,
            'username': user.username,
            'declare_name': user.declare_name,
            'department': {
                'id': user.department.dpid,
                'name': user.department.dpname
            } if user.department else None,
            'practice_start': user.practice_start.isoformat() if user.practice_start else None,
            'practice_end': user.practice_end.isoformat() if user.practice_end else None,
            'status': '在職' if not user.resignation_day else '離職',
            'phone': user.phone,
            'email': user.email,
            'address': user.address,
            'photo_url': user.photo_url,
            'licenses': [
                {
                    'id': lic.id,
                    'type': lic.license_type,
                    'name': lic.license_name,
                    'start_date': lic.start_date.isoformat() if lic.start_date else None,
                    'end_date': lic.end_date.isoformat() if lic.end_date else None,
                    'bonus': lic.bonus
                }
                for lic in user.licenses
            ],
            'job_description': user.job_description
        })
    else:
        # 一般使用者管理資料
        return jsonify({
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'declare_name': user.declare_name,
            'department_id': user.department_id,
            'practice_start': user.practice_start.isoformat() if user.practice_start else '',
            'practice_end': user.practice_end.isoformat() if user.practice_end else '',
            'status': '在職' if not user.resignation_day else '離職'
        })

# ✅ 更新使用者
@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '找不到使用者'}), 404

    data = request.get_json()
    print("📥 更新資料:", data)

    try:
        user.username = data.get('username', user.username)
        user.role = data.get('role', user.role)
        user.department_id = data.get('department_id', user.department_id)
        user.declare_name = data.get('declare_name', user.declare_name)
        user.practice_start = parse_date(data.get('practice_start')) or user.practice_start
        user.practice_end = parse_date(data.get('practice_end')) or user.practice_end
        user.resignation_day = None if data.get('status') == '在職' else datetime.utcnow()

        db.session.commit()
        return jsonify({'msg': '使用者更新成功'})

    except Exception as e:
        db.session.rollback()
        print("❌ 更新使用者錯誤:", e)
        return jsonify({'msg': '更新失敗', 'error': str(e)}), 500

# ✅ 刪除使用者
@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'msg': '找不到使用者'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'msg': '使用者刪除成功'})


