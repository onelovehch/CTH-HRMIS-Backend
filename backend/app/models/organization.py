from backend.app import db
from datetime import datetime


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key = True)
    orgname = db.Column(db.String(20), unique = True, nullable = False)
    father_org = db.Column(db.Integer) #父公司
    level = db.Column(db.Enum('Operations Center','Campus','Branch'), nullable = False)
    creat_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'Organization{self.orgname}'

