from flask import Blueprint, request, session, redirect, url_for, render_template
import urlpath
from apps.models.blogmodels import User, Blog, Like
from exts import db
from sqlalchemy import and_, or_, desc

blog_bp = Blueprint('blog', __name__, url_prefix='/blog')


# 1. 发表博客
@blog_bp.route('/publish/', methods=['POST', 'GET'])
def publish():
    if request.method == 'GET':
        # 使用 session 存储登录状态
        if session.get('username'):
            return render_template('publish.html')
        else:
            # 到登录页
            # 记录跳转之前的路由
            urlpath.current_url = url_for('blog.publish')
            print(urlpath.current_url)
            return redirect(url_for('user.login'))
    else:
        print(request.form)
        # 获取发表博客的用户
        user = User.query.filter(User.username == session.get('username')).first()
        # 获取用户发表的信息
        title = request.form.get('title')
        content = request.form.get('content')
        # 创建博客对象
        blog = Blog(title, content, user.uid)
        # 添加
        db.session.add(blog)
        # 提交
        db.session.commit()
        return redirect(url_for('index'))


# 首页内容展示
@blog_bp.route('/index/')
def blogindex():
    # 查询所有的博客, 把它渲染到首页上
    # blogs = Blog.query.order_by(desc(Blog.bid)).all()
    # print(blogs)
    # 分页显示
    '''
    page : 当前页码
    perpage : 每页的数据量
    返回: 根据设定的页面和每页显示量, 常见一个页码器对象
    这个对象的一些属性:
            items ---- 当前页下的数据元素集合
            page ---- 当前页码
            per_page ---- 当前页数据量
            has_prev ---- 判断是否有上一页
            has_next ---- 判断是否有下一页
            prev_num ---- 上一页页码
            next_num ---- 下一页页码
            iter_pages() ---- 页码器中的页码数们
    '''
    # 获取页码
    curpage = int(request.args.get('currentpage', 1))  # 当没有currentpage传递的时候, 拿的是第一页的数据
    paginate = Blog.query.order_by(Blog.bid.desc()).paginate(page=curpage, per_page=5)
    print(paginate)

    '''
    如果用户登录状态下, 获取这个用户点赞的那些博客, 传到new_index.html
    否则传空
    '''
    if session.get('username'):
        user = User.query.filter(User.username == session.get('username')).first()
        # 获取这个用户点赞的那些博客id
        print(user.like_blogs)
        like_bids = [blog.bid for blog in user.like_blogs]
        '''
        推导式:
        [blog.bid for blog in user.like_blogs]
        
        等同于:
        like_bids = []
        for blog.bid in user.like_blogs:
            like_bids.append(blog.bid)
        '''
        return render_template('new_index.html', paginate=paginate, like_bids=like_bids)
    else:
        return render_template('new_index.html', paginate=paginate)



# 点赞的路由
@blog_bp.route('/like/')
def like():
    # 请求路由的时候, 如果用户没有登录 ---- 进行登录 ---- 登录完成回到首页 -----
    # 有登录信息, 进行点赞, 两个数据: 谁点赞的, 点的哪篇博客
    if session.get('username'):
        # 登录状态 获取数据
        user = User.query.filter(User.username == session.get('username')).first()
        # 获取博客id
        bid = int(request.args.get('bid'))
        blog = Blog.query.get(bid)
        print(request.args)
        # 创建like对象
        like = Like(user.uid, bid)
        # 添加
        db.session.add(like)
        # 提交
        db.session.commit()
        print(f'当前用户点赞的博客{user.like_blogs}')
        print(f'当前博客的喜爱者有{blog.like_users}')
        return redirect(url_for('blog.blogindex'))
    else:
        # 记录登录前路由
        urlpath.current_url = url_for('blog.blogindex')
        # 跳转到登录界面
        return redirect(url_for('user.login'))


# 取消点赞
@blog_bp.route('/unlike/')
def unlike():
    user = User.query.filter(User.username == session.get('username')).first()
    # 获取博客id
    bid = int(request.args.get('bid'))
    blog = Blog.query.get(bid)
    # 查询这条记录
    liker = Like.query.filter(Like.uid == user.uid, Like.bid == bid).first()
    # 删除
    db.session.delete(liker)
    db.session.commit()
    return redirect(url_for('blog.blogindex'))


'''
既接受点赞的请求, 也接受取消点赞的请求
'''
@blog_bp.route('/likeorunlike/')
def likeorunlike():
    # 获取操作博客的id
    bid = int(request.args.get('bid'))
    # 根据bid 获取博客对象
    blog = Blog.query.get(bid)
    # 获取用户信息
    user = User.query.filter(User.username == session.get('username')).first()
    '''
    区分, 用户是要点赞, 还是取消点赞
    '''
    # 声明一个标记, 假设没有
    flag = False
    # 查询点赞者, 里面有没有当前登录着, 有就是取消点赞, 没有就是点赞操作
    for user1 in blog.like_users:
        if session.get('username') == user1.username:
            flag = True
            break  # 结束遍历, 结束查找
    if flag is True:
        # 取消点赞
        # 查询这条记录
        liker = Like.query.filter(Like.uid == user.uid, Like.bid == bid).first()
        # 删除
        db.session.delete(liker)
        db.session.commit()
        return {'code': 201, 'likenum': len(blog.like_users)}
    else:
        # 进行点赞
        like1 = Like(user.uid, bid)
        # 添加
        db.session.add(like1)
        # 提交
        db.session.commit()
        return {'code': 200, 'likenum': len(blog.like_users)}


# 点击用户名进入对应人主页
@blog_bp.route('/userindex/')
def userindex():
    username = request.args.get('username')
    user = User.query.filter(User.username == username).first()
    print(f'这个人发表的所有博客{user.blogs}')
    return render_template('userindex.html', blogs=user.blogs)


# 搜素博客
@blog_bp.route('/search/')
def search():
    print(request.args)
    # 获取搜索词
    search_keyword = request.args.get('keyword')
    # 查询关键词是否包含在标题或内容中
    blogs = Blog.query.order_by(Blog.bid.desc()).filter(or_(Blog.title.contains(search_keyword), Blog.content.contains(search_keyword))).all()

    return render_template('search.html', blogs=blogs)


# 删除自己发表的博客
@blog_bp.route('/deleteblog/', methods=['POST'])
def deleteblog():
    # 要删除的博客id
    bid = int(request.form.get('bid'))
    # 要删除的博客
    blog = Blog.query.get(bid)
    # 删除
    db.session.delete(blog)
    # 提交
    db.session.commit()
    return '删除成功'