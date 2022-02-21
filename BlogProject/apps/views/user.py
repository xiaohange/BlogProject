from flask import Blueprint, request, render_template, redirect, url_for, session  # session 令牌
# 导入User
from apps.models.blogmodels import User
from exts import db
# 导入记录上一次路由信息的变量
import urlpath
# 导入项目路径头文件
import basepath
import os  # 对文件系统进行操作的模块
import uuid  # 生成唯一标识模块

'''
模块的导入时, 只有第一次导入的时候加载模块中的内容, 并生成一个.pyc描述文件, 之后再导入的时候不会加载模块中的内容了, 
直接使用的是.pyc描述文件的中的内容
'''

user_bp = Blueprint('user', __name__, url_prefix='/user')


# 注册
@user_bp.route('/register/', methods=['GET', 'POST'])
def register():
    # 点击注册get请求, 渲染注册页面
    if request.method == 'GET':
        # 只获取注册界面
        return render_template('register.html')
    else:  # 点击注册, 提交数据, 获取数据信息
        # 获取post提交的数据
        print(f'{request.form}')
        name = request.form.get('username')
        psw = request.form.get('psw')
        phone = request.form.get('phone')
        # 创建对象
        user = User(name, psw, phone)
        # 添加
        db.session.add(user)
        # 提交
        db.session.commit()
        return redirect(url_for('user.login'))


# 检验用户名是否存在(用户名不允许重复)
@user_bp.route('/checkname/', methods=['POST'])
def check_name():
    print(request.form)
    # 获取用户名
    username = request.form.get('username')
    # 进行查询 根据username在数据库中进行查询, 获取第一条数据
    data = User.query.filter(User.username == username).first()
    print(data)
    if data:
        return {'code': 200, 'msg': '用户名已存在'}
    else:
        return {'code': 201, 'msg': '用户名不存在'}

    return 'username ok'


@user_bp.route('/checkphone/', methods=['POST'])
def check_phone():
    # 获取手机号
    phone = request.form.get('phone')
    # 查询
    data = User.query.filter(User.phone == phone).first()
    print(data)
    if data:
        return {'code': 200, 'msg': '手机号已存在'}
    else:
        return {'code': 201, 'msg': '手机号不存在'}
    return 'phone ok'


# 设置登录对应的路由信息
@user_bp.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', message='')
    else:
        print(request.form)
        # 提取数据 根据数据查询
        username = request.form.get('username')
        password = request.form.get('psw')
        # 数据查询
        user = User.query.filter(User.username == username, User.password == password).first()
        print(user)
        if user is None:
            return render_template('login.html', message='用户名或者密码错误')
        else:
            # 保存用户的信息 ---- 证明是哪个用户登录的
            session['username'] = username  # 把用户名存储了
            print(session)
            print(urlpath.current_url)
            return redirect(urlpath.current_url)


# 退出登录
@user_bp.route('/exit/')
def exit():
    # 移除存储的用户登录状态
    session.pop('username')
    print(session)
    return redirect(url_for('index'))


# 修改头像
@user_bp.route('/updateicon/', methods=['POST', 'GET'])
def updateicon():
    if request.method == 'GET':
        return render_template('updateicon.html')
    else:
        print(request.form)
        # 接受图片数据
        print(request.files)
        # 把文件存储本地
        # 1. 先获取到数据
        icon_file = request.files.get('icon') # icon_file.file_name 拿到文件名

        if icon_file.filename != '':
            # 2. 设置文件存储路径 __file__ 当前文件
            # 路径拼接
            # 生成图片唯一标识
            imgage_id = uuid.uuid4()
            # 根据图片id设置一个图片名称
            # icon_file.filename.rfind('.') 查找.第一次出现的位置
            # [dot_pos:] 提取字串, 从指定位置到最后
            dot_pos = icon_file.filename.rfind('.')
            image_name = str(imgage_id) + icon_file.filename[dot_pos:]

            save_path = os.path.join(basepath.basedir, 'static/icon', image_name)
            print(save_path)
            # 把数据保存到指定位置
            icon_file.save(save_path)

            # 注意当前用户头像发生变化 数据里需要处理一下
            user = User.query.filter(User.username == session.get('username')).first()
            user.user_icon = 'icon/' + image_name
            # 提交
            db.session.commit()


        return redirect(url_for('blog.blogindex'))