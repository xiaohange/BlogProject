# 配置信息文件
# 开发环境
ENV = 'development'

# 调试模式
DEBUG = True

# 数据库连接驱动
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/blogdb'

# 是否追踪
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 给跨站请求伪造保护设置令牌秘钥, 也是 session令牌
SECRET_KEY = '2e2189u43WD2R323243fewvwvwevbhytjuasip56qwfgrthrerweqderthrewrbfewmvieormvmrepmoewcovmew9320478'