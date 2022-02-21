from flask_script import Manager
# 导入构建flask应用的方法
from apps import create_app
from flask_migrate import Migrate, MigrateCommand
# 导入数据库
from exts import db
from flask import render_template, url_for, redirect
import urlpath
# 引入要映射的模型, 不然数据库迁移时找不到
from apps.models.blogmodels import User
from apps.models.blogmodels import Blog

# 获取app
app = create_app()
# 把app交给manager管理
manager = Manager(app)
# 设置数据库迁移相关信息
mirgrate = Migrate(app, db)
# 将迁移的操作使用命令的形式 交给manager
manager.add_command('database', MigrateCommand)

# 设置主路由
@app.route('/')
def index():
    urlpath.current_url = url_for('index')
    return redirect(url_for('blog.blogindex'))


if __name__ == '__main__':
    manager.run()