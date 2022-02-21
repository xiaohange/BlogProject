from flask import url_for
current_url = None   # 记录当前路由, 默认是空
print(f'urlpath模块下的内容')

'''
记录登录之前要访问的路由是什么
当登录成功之后, 直接定位到对应的路由处
'''