# 用户
from flask import url_for

from exts import db


class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(11), unique=True)
    # 表示用户的头像的路径
    user_icon = db.Column(db.String(100))
    # 这个用户发表了哪些博客
    '''
    这些博客的类型
    backref='属性名' 反向关系
        这个属性名隐式添加在博客类型中的
            博客对象可以通过这个属性, 获取到发表博客的用户信息 
    '''
    blogs = db.relationship('Blog', backref='user')

    # 用户点赞了哪些博客
    like_blogs = db.relationship('Blog', secondary='like')
    def __init__(self, username, password, phone):
        self.username = username
        self.password = password
        self.phone = phone
#         url_for('static', filename='icon/default.jeg')


# 博客模型
class Blog(db.Model):
    # 博客id
    bid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 博客标题
    title = db.Column(db.String(100), nullable=False)
    # 缩略内容
    thum_content = db.Column(db.Text, nullable=False)
    # 完整内容
    content = db.Column(db.Text, nullable=False)
    # 谁发表的 ---- 外键 ---- 联系两张表
    # db.ForeignKey('user.uid') 这个键是一个外键, 关联的哪张表中的哪个字段, 将两张表练习起来
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))

    # like_users 点赞的用户有哪些
    '''
    点赞的用户类型
    secondary 设置的是通过哪张表体现出来的联系性
    '''
    like_users = db.relationship('User', secondary='like')

    def __init__(self, title, content, uid):
        self.title = title
        self.thum_content = content[0:100] + '......' if len(content) > 100 else content
        self.content = content
        self.uid = uid


# 点赞 ---- 关联的是哪些用户点赞了博客, 博客被哪些用户点赞了
class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 用户id --- 用户表中的id
    uid = db.Column(db.Integer, db.ForeignKey('user.uid'))
    # 博客id --- 博客表中的id
    bid = db.Column(db.Integer, db.ForeignKey('blog.bid'))
    def __init__(self, uid, bid):
        self.uid = uid
        self.bid = bid
