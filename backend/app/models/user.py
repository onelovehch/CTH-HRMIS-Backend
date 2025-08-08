from backend.app import db
from datetime import datetime


class User(db.Model):    #定義一個 Python 類別 User，繼承自 SQLAlchemy 的 Model，代表資料庫中的一個資料表。
    __tablename__ = 'users'


    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(10), unique = True, nullable = False)
    password_hash = db.Column(db.String(100), nullable = False)
    role = db.Column(db.Enum('doctor','admin','staff'), default = 'staff')
    department_id = db.Column(db.Integer, db.ForeignKey('departments.dpid'))
    department = db.relationship('Department', backref = 'users', foreign_keys =[department_id])
    create_at = db.Column(db.DateTime, default = datetime.utcnow)
    declare_name = db.Column(db.String(10)) #申報姓名
    declare_id = db.Column(db.String(10))
    practice_start = db.Column(db.Date)
    practice_end = db.Column(db.Date)
    onboard = db.Column(db.DateTime)
    resignation_day = db.Column(db.DateTime)
    first_managed_departments = db.relationship(
        'Department',
        foreign_keys = 'Department.first_manager_id',
        back_populates = 'first_manager',
        lazy = 'dynamic')
    second_managed_departments = db.relationship(
        'Department',
        foreign_keys = 'Department.second_manager_id',
        back_populates = 'second_manager',
        lazy = 'dynamic')
   
    def __repr__(self):
        return f'User {self.username}'


