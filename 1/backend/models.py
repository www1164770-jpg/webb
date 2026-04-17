from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 分类模型
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    websites = db.relationship('Website', backref='category', lazy=True)

# 网站模型 —— user_id 可为空，NULL 表示公共网站，有值表示用户私有收藏
class Website(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    # user_id 为 NULL 时是公共网站（所有人可见），有值时是该用户的私有收藏
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 第三方登录相关字段
    wechat_openid = db.Column(db.String(100), unique=True, nullable=True)
    qq_openid = db.Column(db.String(100), unique=True, nullable=True)
    github_id = db.Column(db.String(100), unique=True, nullable=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=True)
    # 用户的私有网站列表
    websites = db.relationship('Website', backref='owner', lazy=True)
