from flask import Blueprint, request, jsonify #建立「模組化的路由群組」、取得前端送來的資料、回傳 JSON 格式的 HTTP 回應
from backend.app import db ##匯入 db 資料庫物件，用來新增或查詢資料
from backend.app.models.user import User #匯入User 模型，代表 users 資料表
from werkzeug.security import generate_password_hash, check_password_hash #安全處理密碼：將密碼加密（存入 DB），以及登入時驗證密碼
from flask_jwt_extended import create_access_token #建立 JWT token，在登入成功後回傳給用戶端

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods = ['POST']) #當前端對 /api/register 發出 POST 請求時，執行底下的 register() 函式
def register():
    data = request.get_json() #從 request 的 JSON 中取出註冊資料
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'staff')

    if User.query.filter_by(username = username).first():
        return jsonify({'msg' : '使用者已存在'}), 400 #若資料庫中已存在同帳號，回傳錯誤訊息，HTTP 狀態碼 400
    
    new_user = User(     #立新使用者物件，密碼使用加密後版本儲存
        username = username,
        password_hash = generate_password_hash(password),
        role = role
    )
    db.session.add(new_user)
    db.session.commit()  #將新使用者寫入資料庫中
    return jsonify({'msg' : '註冊成功'}),201 #回傳註冊成功

@auth_bp.route('/api/login', methods = ['POST']) #當前端對 /api/login 發出 POST 請求時，執行底下的 login() 
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password') #從前端送來的 JSON 中取出帳密

    user = User.query.filter_by(username = username).first()
    if not user or user.password_hash != password:
        return jsonify({'msg'  : '帳號或密碼錯誤'}), 401  #查詢該使用者是否存在，並驗證密碼是否正確，若失敗，回傳 401 錯誤
    
   
    access_token = create_access_token(identity = str(user.id))#若成功，使用flask_jwt_extended產生一組JWT Token,identity自定義要包進token的資料（id和role）
    return jsonify({'access_token' : access_token})