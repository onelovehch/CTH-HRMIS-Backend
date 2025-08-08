from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models.department import Department
from flask_jwt_extended import jwt_required

department_bp = Blueprint('department', __name__)

# 建立新部門
@department_bp.route('/api/departments', methods=['POST'])
@jwt_required()
def create_department():
    data = request.get_json()

    if Department.query.filter_by(dpname=data.get('dpname')).first():
        return jsonify({'msg': '部門已存在'}), 400

    new_dp = Department(
        dpname=data.get('dpname'),
        father_db=data.get('father_db'),
        child_db=data.get('child_db'),
        cost=data.get('cost'),
        organization_id=data.get('organization_id'),
        first_manager_id=data.get('first_manager_id'),
        second_manager_id=data.get('second_manager_id')
    )

    db.session.add(new_dp)
    db.session.commit()
    return jsonify({'msg': '部門建立成功'}), 201

# 查詢全部部門
@department_bp.route('/api/departments', methods=['GET'])
@jwt_required()
def get_departments():
    departments = Department.query.all()
    result = []
    for dp in departments:
        result.append({
            'dpid': dp.dpid,
            'dpname': dp.dpname,
            'cost': dp.cost,
            'creat_at': dp.creat_at.isoformat() if dp.creat_at else None,
            'organization': {
                'id': dp.organization.id if dp.organization else None,
                'name': dp.organization.orgname if dp.organization else '未指定'
            },
            'first_manager': {
                'id': dp.first_manager.id if dp.first_manager else None,
                'name': dp.first_manager.declare_name if dp.first_manager else '未指定'
            },
            'second_manager': {
                'id': dp.second_manager.id if dp.second_manager else None,
                'name': dp.second_manager.declare_name if dp.second_manager else '未指定'
            }
        })
    return jsonify(result)

# 查詢單一部門
@department_bp.route('/api/departments/<int:dpid>', methods=['GET'])
@jwt_required()
def get_department(dpid):
    dp = Department.query.get(dpid)
    if not dp:
        return jsonify({'msg': '找不到此部門'}), 404

    return jsonify({
        'dpid': dp.dpid,
        'dpname': dp.dpname,
        'cost': dp.cost,
        'creat_at': dp.creat_at.isoformat() if dp.creat_at else None,
        'organization': {
            'id': dp.organization.id if dp.organization else None,
            'name': dp.organization.orgname if dp.organization else '未指定'
        },
        'first_manager': {
            'id': dp.first_manager.id if dp.first_manager else None,
            'name': dp.first_manager.declare_name if dp.first_manager else '未指定'
        },
        'second_manager': {
            'id': dp.second_manager.id if dp.second_manager else None,
            'name': dp.second_manager.declare_name if dp.second_manager else '未指定'
        }
    })

# 更新部門
@department_bp.route('/api/departments/<int:dpid>', methods=['PUT'])
@jwt_required()
def update_department(dpid):
    dp = Department.query.get(dpid)
    if not dp:
        return jsonify({'msg': '查無此部門'}), 404

    data = request.get_json()
    dp.dpname = data.get('dpname', dp.dpname)
    dp.cost = data.get('cost', dp.cost)
    dp.organization_id = data.get('organization_id', dp.organization_id)
    dp.first_manager_id = data.get('first_manager_id', dp.first_manager_id)
    dp.second_manager_id = data.get('second_manager_id', dp.second_manager_id)
    db.session.commit()

    return jsonify({'msg': '部門更新成功'})

# 刪除部門
@department_bp.route('/api/departments/<int:dpid>', methods=['DELETE'])
@jwt_required()
def delete_department(dpid):
    dp = Department.query.get(dpid)
    if not dp:
        return jsonify({'msg': '查無此部門'}), 404

    db.session.delete(dp)
    db.session.commit()
    return jsonify({'msg': '部門刪除成功'})

# 查詢某公司下所有部門
@department_bp.route('/api/organizations/<int:org_id>/departments', methods=['GET'])
@jwt_required()
def get_departments_by_org(org_id):
    departments = Department.query.filter_by(organization_id=org_id).all()
    result = []
    for dp in departments:
        result.append({
            'dpid': dp.dpid,
            'dpname': dp.dpname,
            'cost': dp.cost,
            'creat_at': dp.creat_at.isoformat() if dp.creat_at else None,
            'organization': {
                'id': dp.organization.id if dp.organization else None,
                'name': dp.organization.orgname if dp.organization else '未指定'
            },
            'first_manager': {
                'id': dp.first_manager.id if dp.first_manager else None,
                'name': dp.first_manager.declare_name if dp.first_manager else '未指定'
            },
            'second_manager': {
                'id': dp.second_manager.id if dp.second_manager else None,
                'name': dp.second_manager.declare_name if dp.second_manager else '未指定'
            }
        })
    return jsonify(result)



