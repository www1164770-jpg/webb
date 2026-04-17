"""一次性脚本：清空并重新写入所有网站数据"""
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app import app
from models import db, Category, Website

with app.app_context():
    print("清空旧数据...")
    db.session.query(Website).delete()
    db.session.commit()
    db.session.query(Category).delete()
    db.session.commit()

    print("写入分类...")
    cat_names = ['学习', '开发工具', '娱乐', 'AI工具', '工具']
    for name in cat_names:
        db.session.add(Category(name=name))
    db.session.commit()

    print("写入网站...")
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
        {'name': '慕课网', 'url': 'https://www.imooc.com', 'description': 'IT技能学习平台', 'category': '学习'},
        {'name': '极客时间', 'url': 'https://time.geekbang.org', 'description': '技术人员学习平台', 'category': '学习'},
        {'name': '网易公开课', 'url': 'https://open.163.com', 'description': '免费公开课平台', 'category': '学习'},
        {'name': 'B站学习区', 'url': 'https://www.bilibili.com/v/knowledge', 'description': 'B站知识学习频道', 'category': '学习'},
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
        cat = Category.query.filter_by(name=site_data['category']).first()
        if cat:
            db.session.add(Website(
                name=site_data['name'],
                url=site_data['url'],
                description=site_data['description'],
                category_id=cat.id
            ))
    db.session.commit()
    print(f"完成！共写入 {len(websites)} 个网站")
