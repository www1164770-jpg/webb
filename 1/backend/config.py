# 配置文件

import os

class Config:
    # 数据库配置
    _mysql_password = 'weiyijie748'  # 直接使用密码
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://root:{_mysql_password}@localhost:3306/navdb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 应用配置
    SECRET_KEY = 'your-secret-key'
    
    # CORS配置
    CORS_HEADERS = 'Content-Type'
