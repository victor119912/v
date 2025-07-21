from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # 基本設定
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # MongoDB 設定
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
    app.config['MONGODB_DATABASE'] = os.getenv('MONGODB_DATABASE')
    
    # 初始化擴充套件
    CORS(app)
    JWTManager(app)
    
    # 註冊藍圖
    from routes.auth import auth_bp
    from routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
