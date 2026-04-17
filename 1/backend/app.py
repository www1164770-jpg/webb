import os
# Flask：Web框架核心；request：获取请求参数；jsonify：把Python数据转成JSON返回给前端
# send_from_directory：从指定目录发送文件（用于托管前端页面）
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS      # 处理跨域，允许前端页面访问后端接口
from config import Config        # 导入配置文件（数据库连接等）
from models import db, Category, Website, User  # 导入数据库模型

# ============================================================
# 初始化 Flask 应用
# static_folder：指定静态文件目录为 frontend 文件夹
# static_url_path=''：让前端文件可以直接通过根路径访问
# ============================================================
app = Flask(__name__, static_folder='../frontend', static_url_path='/static_files')
app.config.from_object(Config)   # 加载配置（数据库URI、密钥等）

# 允许所有来源的跨域请求（开发环境使用，生产环境应限制来源）
CORS(app, origins="*")

# 将数据库与 Flask 应用绑定
db.init_app(app)

# ============================================================
# 应用启动时执行：创建数据库、建表、初始化数据
# app_context() 是 Flask 的应用上下文，数据库操作必须在其中执行
# ============================================================
with app.app_context():
    import pymysql
    
    db_name = 'navdb'  # 数据库名称
    
    # 第一步：用 pymysql 直接连接 MySQL，创建数据库（如果不存在）
    # 因为 SQLAlchemy 连接时数据库必须已存在，所以要先手动创建
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='weiyijie748',  # 直接使用密码
            port=3306
        )
        with conn.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"Database {db_name} created successfully!")
        conn.close()
    except Exception as e:
        print(f"Error creating database: {e}")
    
    # 第二步：根据 models.py 中定义的模型，自动创建对应的数据库表
    db.create_all()
    
    # --------------------------------------------------------
    # 初始化分类数据
    # force_init_categories=True 时会清空并重新写入分类
    # force_init_categories=False 时只在分类表为空时才写入
    # --------------------------------------------------------
    force_init_categories = False
    if Category.query.count() == 0 or force_init_categories:
        if force_init_categories:
            # 先删网站（因为网站有外键依赖分类，必须先删子表）
            db.session.query(Website).delete()
            db.session.commit()
            db.session.query(Category).delete()
            db.session.commit()
        
        # 写入5个默认分类
        categories = ['学习', '开发工具', '娱乐', 'AI工具', '工具']
        for cat_name in categories:
            category = Category(name=cat_name)
            db.session.add(category)  # 添加到会话（还未写入数据库）
        db.session.commit()           # 提交事务，真正写入数据库
    
    # --------------------------------------------------------
    # 初始化网站数据
    # force_init=True 时会清空并重新写入所有网站
    # force_init=False 时只在网站表为空时才写入
    # --------------------------------------------------------
    force_init = False
    if Website.query.count() == 0 or force_init:
        if force_init:
            db.session.query(Website).delete()
            db.session.commit()
        
        # 预设网站列表，每条包含名称、地址、描述、所属分类
        websites = [
            # 学习
            {'name': '百度', 'url': 'https://www.baidu.com', 'description': '中国最大的搜索引擎', 'category': '学习'},
            {'name': 'Google', 'url': 'https://www.google.com', 'description': '全球最大的搜索引擎', 'category': '学习'},
            {'name': 'MDN Web Docs', 'url': 'https://developer.mozilla.org', 'description': 'Web开发权威文档', 'category': '学习'},
            {'name': '菜鸟教程', 'url': 'https://www.runoob.com', 'description': '编程入门学习网站', 'category': '学习'},
            {'name': 'W3School', 'url': 'https://www.w3school.com.cn', 'description': 'Web开发学习网站', 'category': '学习'},
            {'name': '知乎', 'url': 'https://www.zhihu.com', 'description': '知识问答社区', 'category': '学习'},
            {'name': 'Wikipedia', 'url': 'https://zh.wikipedia.org', 'description': '自由的百科全书', 'category': '学习'},
            {'name': 'Coursera', 'url': 'https://www.coursera.org', 'description': '在线课程学习平台', 'category': '学习'},
            {'name': 'B站学习区', 'url': 'https://www.bilibili.com/v/knowledge', 'description': 'B站知识学习频道', 'category': '学习'},
            {'name': '慕课网', 'url': 'https://www.imooc.com', 'description': 'IT技能学习平台', 'category': '学习'},
            {'name': '极客时间', 'url': 'https://time.geekbang.org', 'description': '技术人员学习平台', 'category': '学习'},
            {'name': '网易公开课', 'url': 'https://open.163.com', 'description': '免费公开课平台', 'category': '学习'},
            # 开发工具
            {'name': 'GitHub', 'url': 'https://github.com', 'description': '全球最大代码托管平台', 'category': '开发工具'},
            {'name': 'Stack Overflow', 'url': 'https://stackoverflow.com', 'description': '编程问答社区', 'category': '开发工具'},
            {'name': 'LeetCode', 'url': 'https://leetcode.cn', 'description': '算法练习平台', 'category': '开发工具'},
            {'name': 'CSDN', 'url': 'https://www.csdn.net', 'description': '程序员技术社区', 'category': '开发工具'},
            {'name': '掘金', 'url': 'https://juejin.cn', 'description': '开发者技术社区', 'category': '开发工具'},
            {'name': 'Gitee', 'url': 'https://gitee.com', 'description': '国内代码托管平台', 'category': '开发工具'},
            {'name': 'CodePen', 'url': 'https://codepen.io', 'description': '前端代码在线编辑', 'category': '开发工具'},
            {'name': 'npm', 'url': 'https://www.npmjs.com', 'description': 'Node.js包管理平台', 'category': '开发工具'},
            {'name': 'Docker Hub', 'url': 'https://hub.docker.com', 'description': 'Docker镜像仓库', 'category': '开发工具'},
            {'name': 'Postman', 'url': 'https://www.postman.com', 'description': 'API调试工具', 'category': '开发工具'},
            {'name': 'SegmentFault', 'url': 'https://segmentfault.com', 'description': '技术问答社区', 'category': '开发工具'},
            {'name': 'PyPI', 'url': 'https://pypi.org', 'description': 'Python包索引', 'category': '开发工具'},
            # 娱乐
            {'name': 'Bilibili', 'url': 'https://www.bilibili.com', 'description': '国内最大视频弹幕网站', 'category': '娱乐'},
            {'name': 'YouTube', 'url': 'https://www.youtube.com', 'description': '全球最大视频平台', 'category': '娱乐'},
            {'name': '爱奇艺', 'url': 'https://www.iqiyi.com', 'description': '在线视频平台', 'category': '娱乐'},
            {'name': '腾讯视频', 'url': 'https://v.qq.com', 'description': '在线视频平台', 'category': '娱乐'},
            {'name': '优酷', 'url': 'https://www.youku.com', 'description': '在线视频平台', 'category': '娱乐'},
            {'name': '网易云音乐', 'url': 'https://music.163.com', 'description': '音乐流媒体平台', 'category': '娱乐'},
            {'name': 'QQ音乐', 'url': 'https://y.qq.com', 'description': '音乐流媒体平台', 'category': '娱乐'},
            {'name': '酷狗音乐', 'url': 'https://www.kugou.com', 'description': '音乐流媒体平台', 'category': '娱乐'},
            {'name': '抖音', 'url': 'https://www.douyin.com', 'description': '短视频平台', 'category': '娱乐'},
            {'name': '快手', 'url': 'https://www.kuaishou.com', 'description': '短视频平台', 'category': '娱乐'},
            {'name': '微博', 'url': 'https://weibo.com', 'description': '社交媒体平台', 'category': '娱乐'},
            {'name': '小红书', 'url': 'https://www.xiaohongshu.com', 'description': '生活方式分享平台', 'category': '娱乐'},
            {'name': '淘宝', 'url': 'https://www.taobao.com', 'description': '网上购物平台', 'category': '娱乐'},
            {'name': '京东', 'url': 'https://www.jd.com', 'description': '网上购物平台', 'category': '娱乐'},
            {'name': '拼多多', 'url': 'https://www.pinduoduo.com', 'description': '社交电商平台', 'category': '娱乐'},
            {'name': '美团', 'url': 'https://www.meituan.com', 'description': '外卖生活服务平台', 'category': '娱乐'},
            {'name': '饿了么', 'url': 'https://www.ele.me', 'description': '外卖配送平台', 'category': '娱乐'},
            {'name': 'Steam', 'url': 'https://store.steampowered.com', 'description': '游戏数字发行平台', 'category': '娱乐'},
            # AI工具
            {'name': 'ChatGPT', 'url': 'https://chat.openai.com', 'description': 'OpenAI AI聊天助手', 'category': 'AI工具'},
            {'name': 'Claude', 'url': 'https://claude.ai', 'description': 'Anthropic AI助手', 'category': 'AI工具'},
            {'name': 'Gemini', 'url': 'https://gemini.google.com', 'description': 'Google AI助手', 'category': 'AI工具'},
            {'name': '文心一言', 'url': 'https://yiyan.baidu.com', 'description': '百度AI对话助手', 'category': 'AI工具'},
            {'name': '通义千问', 'url': 'https://tongyi.aliyun.com', 'description': '阿里云AI助手', 'category': 'AI工具'},
            {'name': '讯飞星火', 'url': 'https://xinghuo.xfyun.cn', 'description': '科大讯飞AI助手', 'category': 'AI工具'},
            {'name': 'Midjourney', 'url': 'https://www.midjourney.com', 'description': 'AI图像生成工具', 'category': 'AI工具'},
            {'name': 'Stable Diffusion', 'url': 'https://stability.ai', 'description': 'AI图像生成模型', 'category': 'AI工具'},
            {'name': 'GitHub Copilot', 'url': 'https://github.com/features/copilot', 'description': 'AI代码补全工具', 'category': 'AI工具'},
            {'name': 'Hugging Face', 'url': 'https://huggingface.co', 'description': 'AI模型社区平台', 'category': 'AI工具'},
            {'name': 'Kimi', 'url': 'https://kimi.moonshot.cn', 'description': '月之暗面AI助手', 'category': 'AI工具'},
            {'name': '豆包', 'url': 'https://www.doubao.com', 'description': '字节跳动AI助手', 'category': 'AI工具'},
            # 工具
            {'name': '谷歌翻译', 'url': 'https://translate.google.com', 'description': '在线翻译工具', 'category': '工具'},
            {'name': '百度翻译', 'url': 'https://fanyi.baidu.com', 'description': '在线翻译工具', 'category': '工具'},
            {'name': '在线工具', 'url': 'https://tool.lu', 'description': '开发者在线工具集合', 'category': '工具'},
            {'name': '腾讯文档', 'url': 'https://docs.qq.com', 'description': '在线协作文档', 'category': '工具'},
            {'name': '百度网盘', 'url': 'https://pan.baidu.com', 'description': '云存储服务', 'category': '工具'},
            {'name': '阿里云盘', 'url': 'https://www.aliyundrive.com', 'description': '阿里云存储服务', 'category': '工具'},
            {'name': '高德地图', 'url': 'https://www.amap.com', 'description': '地图导航服务', 'category': '工具'},
            {'name': '百度地图', 'url': 'https://map.baidu.com', 'description': '地图导航服务', 'category': '工具'},
            {'name': '滴滴出行', 'url': 'https://www.didiglobal.com', 'description': '打车出行平台', 'category': '工具'},
            {'name': '12306', 'url': 'https://www.12306.cn', 'description': '火车票购票平台', 'category': '工具'},
            {'name': '天气网', 'url': 'https://www.weather.com.cn', 'description': '天气预报查询', 'category': '工具'},
            {'name': 'Notion', 'url': 'https://www.notion.so', 'description': '全能笔记协作工具', 'category': '工具'},
            {'name': '语雀', 'url': 'https://www.yuque.com', 'description': '阿里知识库工具', 'category': '工具'},
            {'name': 'ProcessOn', 'url': 'https://www.processon.com', 'description': '在线流程图绘制', 'category': '工具'},
        ]
        
        for site_data in websites:
            # 根据分类名称查找对应的分类对象
            category = Category.query.filter_by(name=site_data['category']).first()
            if category:
                website = Website(
                    name=site_data['name'],
                    url=site_data['url'],
                    description=site_data.get('description', ''),
                    category_id=category.id  # 存分类的ID（外键）
                )
                db.session.add(website)
        
        db.session.commit()
        print(f"Added {len(websites)} websites")


# ============================================================
# API 路由定义
# 每个路由对应一个 URL，处理前端发来的请求并返回 JSON 数据
# ============================================================

# 托管前端页面：访问 http://localhost:5000 时返回 index.html
@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

# 获取所有分类 —— GET /api/categories
# 前端用来渲染顶部的分类标签
@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()  # 查询所有分类
    return jsonify([{'id': cat.id, 'name': cat.name} for cat in categories])

# 获取网站列表 —— GET /api/websites
# 支持分页（page/per_page）和按分类筛选（category_id）
# 已登录用户看到：公共网站 + 自己的私有收藏；未登录只看公共网站
@app.route('/api/websites', methods=['GET'])
def get_websites():
    category_id = request.args.get('category_id')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))

    # 获取当前登录用户ID（从 Token 中解析，失败则为 None）
    current_user_id = None
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        try:
            payload = jwt.decode(auth_header[7:], JWT_SECRET, algorithms=['HS256'])
            current_user_id = payload.get('user_id')
        except Exception:
            pass

    # 构建查询：公共网站(user_id=NULL) + 当前用户私有收藏
    from sqlalchemy import or_
    base_query = Website.query.filter(
        or_(Website.user_id == None, Website.user_id == current_user_id)
    )
    if category_id:
        base_query = base_query.filter_by(category_id=category_id)

    pagination = base_query.paginate(page=page, per_page=per_page, error_out=False)
    websites = pagination.items

    return jsonify({
        'websites': [{
            'id': site.id,
            'name': site.name,
            'url': site.url,
            'description': site.description,
            'category_id': site.category_id,
            'category_name': site.category.name,
            'is_private': site.user_id is not None  # 标记是否为私有收藏
        } for site in websites],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'has_next': pagination.has_next
    })

# 添加网站 —— POST /api/websites
@app.route('/api/websites', methods=['POST'])
def add_website():
    data = request.json

    # 获取当前登录用户ID
    current_user_id = None
    auth_header = request.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        try:
            payload = jwt.decode(auth_header[7:], JWT_SECRET, algorithms=['HS256'])
            current_user_id = payload.get('user_id')
        except Exception:
            pass

    new_website = Website(
        name=data['name'],
        url=data['url'],
        description=data.get('description', ''),
        category_id=data['category_id'],
        user_id=current_user_id  # 登录用户添加的为私有收藏，游客添加为公共
    )
    db.session.add(new_website)
    db.session.commit()
    return jsonify({'id': new_website.id, 'name': new_website.name})

# 修改网站 —— PUT /api/websites/<id>
# <int:id> 表示从URL中获取整数类型的id参数
@app.route('/api/websites/<int:id>', methods=['PUT'])
def update_website(id):
    website = Website.query.get(id)  # 根据ID查找网站
    if not website:
        return jsonify({'error': 'Website not found'}), 404  # 找不到返回404
    
    data = request.json
    # 用 .get() 方法：如果前端没传该字段，保留原来的值
    website.name = data.get('name', website.name)
    website.url = data.get('url', website.url)
    website.description = data.get('description', website.description)
    website.category_id = data.get('category_id', website.category_id)
    
    db.session.commit()
    return jsonify({'id': website.id, 'name': website.name})

# 删除网站 —— DELETE /api/websites/<id>
@app.route('/api/websites/<int:id>', methods=['DELETE'])
def delete_website(id):
    website = Website.query.get(id)
    if not website:
        return jsonify({'error': 'Website not found'}), 404
    
    db.session.delete(website)
    db.session.commit()
    return jsonify({'message': 'Website deleted'})

# ============================================================
# 用户认证相关接口
# ============================================================
import jwt
import functools
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# JWT 密钥，生产环境应放到环境变量里
JWT_SECRET = os.environ.get('JWT_SECRET', 'nav-jwt-secret-2024')
JWT_EXPIRE_HOURS = 24  # Token 有效期 24 小时

# ---- login_required 装饰器 ----
def login_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': '未登录，请先登录'}), 401
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.current_user_id = payload['user_id']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token 已过期，请重新登录'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token 无效'}), 401
        return f(*args, **kwargs)
    return decorated

# ---- 注册接口 ----
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    email = (data.get('email') or '').strip()
    if not username or not password or not email:
        return jsonify({'error': '用户名、密码和邮箱不能为空'}), 400
    if len(password) < 6:
        return jsonify({'error': '密码长度不能少于6位'}), 400
    if '@' not in email:
        return jsonify({'error': '邮箱格式不正确'}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已被注册'}), 409
    if User.query.filter_by(email=email).first():
        return jsonify({'error': '邮箱已被注册'}), 409
    hashed = generate_password_hash(password)
    user = User(username=username, password_hash=hashed, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': '注册成功', 'username': username}), 201

# ---- 登录接口 ----
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''
    if not username or not password:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'error': '用户名或密码错误'}), 401
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
    return jsonify({'message': '登录成功', 'token': token, 'username': user.username})

# ---- 获取当前用户信息 ----
@app.route('/api/me', methods=['GET'])
@login_required
def get_me():
    user = User.query.get(request.current_user_id)
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email})

# ---- AI 智能推荐接口 ----
@app.route('/api/ai_recommend', methods=['POST'])
def ai_recommend():
    try:
        from openai import OpenAI
        import json
        data = request.json
        query = (data.get('query') or '').strip()
        if not query:
            return jsonify({'error': '请输入搜索内容'}), 400
        api_key = os.environ.get('DASHSCOPE_API_KEY')
        if not api_key:
            return jsonify({'error': '未配置 DASHSCOPE_API_KEY 环境变量'}), 500
        client = OpenAI(api_key=api_key, base_url='https://dashscope.aliyuncs.com/compatible-mode/v1')
        system_prompt = '你是网站推荐助手，根据用户需求推荐3-5个网站，严格返回JSON格式：{"recommendations":[{"title":"名称","url":"https://...","reason":"理由"}]}'
        response = client.chat.completions.create(
            model='qwen-turbo',
            messages=[{'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': f'我需要：{query}'}],
            response_format={'type': 'json_object'},
            temperature=0.7, max_tokens=1000
        )
        return jsonify(json.loads(response.choices[0].message.content))
    except Exception as e:
        print(f'AI推荐接口错误: {e}')
        return jsonify({'error': 'AI 服务暂时不可用'}), 500

# ============================================================# 第三方登录相关接口# ============================================================
import requests

# ---- 微信登录接口 ----
@app.route('/api/login/wechat', methods=['POST'])
def wechat_login():
    try:
        data = request.json
        code = data.get('code')
        if not code:
            return jsonify({'error': '缺少code参数'}), 400
        
        # 这里需要替换为真实的微信开发参数
        app_id = os.environ.get('WECHAT_APP_ID', 'your-wechat-app-id')
        app_secret = os.environ.get('WECHAT_APP_SECRET', 'your-wechat-app-secret')
        
        # 调用微信API获取openid
        response = requests.get(
            'https://api.weixin.qq.com/sns/jscode2session',
            params={
                'appid': app_id,
                'secret': app_secret,
                'js_code': code,
                'grant_type': 'authorization_code'
            }
        )
        result = response.json()
        
        if 'errcode' in result:
            return jsonify({'error': f'微信登录失败: {result.get("errmsg")}'}), 400
        
        openid = result.get('openid')
        if not openid:
            return jsonify({'error': '获取openid失败'}), 400
        
        # 查找或创建用户
        user = User.query.filter_by(wechat_openid=openid).first()
        if not user:
            # 创建新用户
            username = f'wechat_{openid[:8]}'
            password = os.urandom(16).hex()  # 生成随机密码
            email = f'{openid}@wechat.com'
            hashed = generate_password_hash(password)
            user = User(
                username=username,
                password_hash=hashed,
                email=email,
                wechat_openid=openid
            )
            db.session.add(user)
            db.session.commit()
        
        # 生成token
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return jsonify({'message': '登录成功', 'token': token, 'username': user.username})
    except Exception as e:
        print(f'微信登录错误: {e}')
        return jsonify({'error': '微信登录失败'}), 500

# ---- QQ登录接口 ----
@app.route('/api/login/qq', methods=['POST'])
def qq_login():
    try:
        data = request.json
        code = data.get('code')
        if not code:
            return jsonify({'error': '缺少code参数'}), 400
        
        # 这里需要替换为真实的QQ开发参数
        app_id = os.environ.get('QQ_APP_ID', 'your-qq-app-id')
        app_secret = os.environ.get('QQ_APP_SECRET', 'your-qq-app-secret')
        redirect_uri = os.environ.get('QQ_REDIRECT_URI', 'http://localhost:5000/api/login/qq/callback')
        
        # 调用QQ API获取access_token
        response = requests.get(
            'https://graph.qq.com/oauth2.0/token',
            params={
                'grant_type': 'authorization_code',
                'client_id': app_id,
                'client_secret': app_secret,
                'code': code,
                'redirect_uri': redirect_uri
            }
        )
        
        # 解析响应
        import urllib.parse
        params = urllib.parse.parse_qs(response.text)
        access_token = params.get('access_token', [None])[0]
        if not access_token:
            return jsonify({'error': '获取access_token失败'}), 400
        
        # 调用QQ API获取openid
        response = requests.get(
            'https://graph.qq.com/oauth2.0/me',
            params={
                'access_token': access_token
            }
        )
        
        # 解析响应
        import json
        result = json.loads(response.text[10:-4])  # 去掉回调函数包装
        openid = result.get('openid')
        if not openid:
            return jsonify({'error': '获取openid失败'}), 400
        
        # 查找或创建用户
        user = User.query.filter_by(qq_openid=openid).first()
        if not user:
            # 创建新用户
            username = f'qq_{openid[:8]}'
            password = os.urandom(16).hex()  # 生成随机密码
            email = f'{openid}@qq.com'
            hashed = generate_password_hash(password)
            user = User(
                username=username,
                password_hash=hashed,
                email=email,
                qq_openid=openid
            )
            db.session.add(user)
            db.session.commit()
        
        # 生成token
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return jsonify({'message': '登录成功', 'token': token, 'username': user.username})
    except Exception as e:
        print(f'QQ登录错误: {e}')
        return jsonify({'error': 'QQ登录失败'}), 500

# ---- 手机号登录接口 ----
@app.route('/api/login/phone', methods=['POST'])
def phone_login():
    try:
        data = request.json
        phone_number = data.get('phone_number')
        code = data.get('code')
        if not phone_number or not code:
            return jsonify({'error': '缺少手机号或验证码'}), 400
        
        # 这里需要替换为真实的短信验证码验证逻辑
        # 例如调用短信服务API验证验证码
        # 这里简化处理，假设验证码为123456
        if code != '123456':
            return jsonify({'error': '验证码错误'}), 400
        
        # 查找或创建用户
        user = User.query.filter_by(phone_number=phone_number).first()
        if not user:
            # 创建新用户
            username = f'phone_{phone_number[-4:]}'
            password = os.urandom(16).hex()  # 生成随机密码
            email = f'{phone_number}@phone.com'
            hashed = generate_password_hash(password)
            user = User(
                username=username,
                password_hash=hashed,
                email=email,
                phone_number=phone_number
            )
            db.session.add(user)
            db.session.commit()
        
        # 生成token
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return jsonify({'message': '登录成功', 'token': token, 'username': user.username})
    except Exception as e:
        print(f'手机号登录错误: {e}')
        return jsonify({'error': '手机号登录失败'}), 500

# ---- GitHub登录接口 ----
@app.route('/api/login/github', methods=['POST'])
def github_login():
    try:
        data = request.json
        code = data.get('code')
        if not code:
            return jsonify({'error': '缺少code参数'}), 400
        
        # 这里需要替换为真实的GitHub开发参数
        client_id = os.environ.get('GITHUB_CLIENT_ID', 'your-github-client-id')
        client_secret = os.environ.get('GITHUB_CLIENT_SECRET', 'your-github-client-secret')
        
        # 调用GitHub API获取access_token
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            json={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code
            }
        )
        result = response.json()
        access_token = result.get('access_token')
        if not access_token:
            return jsonify({'error': '获取access_token失败'}), 400
        
        # 调用GitHub API获取用户信息
        response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        user_info = response.json()
        github_id = str(user_info.get('id'))
        if not github_id:
            return jsonify({'error': '获取GitHub用户信息失败'}), 400
        
        # 查找或创建用户
        user = User.query.filter_by(github_id=github_id).first()
        if not user:
            # 创建新用户
            username = f'github_{user_info.get("login", "user")}'
            password = os.urandom(16).hex()  # 生成随机密码
            email = user_info.get('email', f'{github_id}@github.com')
            hashed = generate_password_hash(password)
            user = User(
                username=username,
                password_hash=hashed,
                email=email,
                github_id=github_id
            )
            db.session.add(user)
            db.session.commit()
        
        # 生成token
        payload = {
            'user_id': user.id,
            'username': user.username,
            'exp': datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
        return jsonify({'message': '登录成功', 'token': token, 'username': user.username})
    except Exception as e:
        print(f'GitHub登录错误: {e}')
        return jsonify({'error': 'GitHub登录失败'}), 500

# 程序入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
