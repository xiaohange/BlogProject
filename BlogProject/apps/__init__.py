# 创建flask应用app
from flask import Flask
# 导入配置文件
import settings
# 导入数据库
from exts import db
# 导入蓝图板块
from apps.views.user import user_bp
from apps.views.blog import blog_bp
# 导入保护类
from flask_wtf.csrf import CSRFProtect


# 声明一个方法, 创建app
def create_app():
    '''
    因为创建flask应用对象的位置发生了变化, 没有和模板文件夹在同一个目录, 所以要进行修改
    '''
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # 设置应用的配置信息 --- 在配置文件中夹在配置信息
    app.config.from_pyfile('../settings.py')
    # 将数据库与项目关联
    db.init_app(app)
    # 创建保护对象 保护app
    CSRFProtect(app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(blog_bp)
    return app