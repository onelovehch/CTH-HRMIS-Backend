from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from backend.config import Config
import os

# 初始化外部套件
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__, static_folder="../../frontend/dist", static_url_path="/")
    app.config.from_object(config_class)

    # 初始化套件
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)

    # 載入 Blueprint 路由模組
    from backend.app.routes import register_routes
    register_routes(app)

    # 前端首頁路由
    @app.route('/')
    def index():
        return send_from_directory(app.static_folder, 'index.html')

    # 404 fallback（支援 Vue Router History 模式）
    @app.errorhandler(404)
    def not_found(e):
        return send_from_directory(app.static_folder, 'index.html')

    return app

