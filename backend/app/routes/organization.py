from flask import Blueprint, request, jsonify
from backend.app import db
from backend.app.models.organization import Organization
from flask_jwt_extended import jwt_required

organization_bp = Blueprint('organization', __name__)

#建立組織
@organization_bp.route('/api/organizations', methods = ['POST'])
@jwt_required()
def create_organization():
    data = request.get_json()
    orgname = data.get('orgname')
    father_org = data.get('father_org')
    level = data.get('level')

    if Organization.query.filter_by(orgname = orgname).first():
        return jsonify({'msg':'組織名稱已存在'}), 400
    
    org = Organization(orgname = orgname, father_org = father_org, level = level)
    db.session.add(org)
    db.session.commit()
    return jsonify({'msg': '組織建立成功'}), 201
    
# 查全部組織
@organization_bp.route('/api/organizations', methods = ['GET'])
@jwt_required()
def get_organizations():
    orgs = Organization.query.all()
    return jsonify([
        {
            'id': o.id,
            'orgname': o.orgname,
            'father_org': o.father_org,
            'level': o.level,
            'creat_at': o.creat_at.isoformat()
        }
        for o in orgs
    ])

# 查單一組織
@organization_bp.route('/api/organizations/<int:id>', methods = ['GET'])
@jwt_required()
def get_organization(id):
    o = Organization.query.get(id)
    if not o:
        return jsonify({'msg': '找不到此組織'}), 404

    return jsonify({
        'id': o.id,
        'orgname': o.orgname,
        'father_org': o.father_org,
        'level': o.level,
        'creat_at': o.creat_at.isoformat()
    })


# 更新
@organization_bp.route('/api/organizations/<int:id>', methods = ['PUT'])
@jwt_required()
def update_organization(id):
    org = Organization.query.get(id)
    if not org:
        return jsonify({'msg': '找不到此組織'}), 404

    data = request.get_json()
    org.orgname = data.get('orgname', org.orgname)
    org.father_org = data.get('father_org', org.father_org)
    org.level = data.get('level', org.level)

    db.session.commit()
    return jsonify({'msg': '組織更新成功'})

# 刪除
@organization_bp.route('/api/organizations/<int:id>', methods = ['DELETE'])
@jwt_required()
def delete_organization(id):
    org = Organization.query.get(id)
    if not org:
        return jsonify({'msg': '找不到此組織'}), 404

    db.session.delete(org)
    db.session.commit()
    return jsonify({'msg': '組織已刪除'})

#組織圖階層樹狀
@organization_bp.route('/api/organizations/tree', methods = ['GET'])
@jwt_required()
def get_organization_tree():
    def build_tree(parent_id):
        nodes = Organization.query.filter_by(father_org = parent_id).all()
        tree = []
        for node in nodes:
            tree.append({
                'id' : node.id,
                'orgname' : node.orgname,
                'level' : node.level,
                'child' : build_tree(node.id)
            })
        return tree
    
    root_nodes  =Organization.query.filter_by(father_org = None).all()
    if not root_nodes:
        return jsonify([]), 200

    tree = []
    for root in root_nodes:
        tree.append({
            'id' : root.id,
            'orgname' : root.orgname,
            'level' : root.level,
            'child' :build_tree(root.id)
        })
    return jsonify(tree)
