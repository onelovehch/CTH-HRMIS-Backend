from backend.app import db
from backend.app.models.user import User
from datetime import datetime

class Department(db.Model):
    __tablename__ = 'departments'

    dpid = db.Column(db.Integer, primary_key = True)
    dpname = db.Column(db.String(20),unique = True, nullable = False)
    father_db = db.Column(db.Integer, nullable = True) #父部門
    child_db = db.Column(db.Integer) #子部門
    cost = db.Column(db.Enum('Y','N'), nullable = False) #是否計算成本
    creat_at = db.Column(db.DateTime, default = datetime.utcnow)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable = True) #要改回FALSE
    organization = db.relationship('Organization', backref = 'departments')
    first_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    second_manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    first_manager = db.relationship(
        'User', 
        foreign_keys=[first_manager_id], 
        back_populates='first_managed_departments')
    second_manager = db.relationship(
        'User', 
        foreign_keys=[second_manager_id], 
        back_populates='second_managed_departments')

    def __repr__(self):
        return f'department {self.dpname}'