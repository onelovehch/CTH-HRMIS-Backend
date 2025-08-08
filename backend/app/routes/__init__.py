from .auth import auth_bp
from .department import department_bp
from .organization import organization_bp
from .user import user_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(organization_bp)
    app.register_blueprint(user_bp)