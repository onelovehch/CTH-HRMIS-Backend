import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('secret_key','defaultsecret')
    SQLALCHEMY_DATABASE_URI = os.getenv('database_uri')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #JWT設定
    JWT_SECRET_KEY = os.getenv('jws_secret_key','defaultsecret')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    #CORS設定
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    DEBUT = True