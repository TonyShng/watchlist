from flask import Flask, url_for, escape, render_template, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import os
import sys

app = Flask(__name__)

# 在扩展类实例化前加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'dev'   # 等同于 app.secret_key = 'dev'

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


class User(db.Model):  # 表名将会是 user (自动生成，小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 user (自动生成，小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


# 模版上下文处理函数
@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)  # 需要返回字典， 等同于 return {'user': user}


@app.errorhandler(404)   # 传入要处理的错误代码
def page_not_found(e):   # 接收异常对象作为参数
    return render_template('404.html'), 404  # 返回模版和状态码


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', movies=movies)
# return '<h1>Hello RainTwo!</h1><img src="http://helloflask.com/totoro.gif">'


# 编辑电影
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 返回对应主键的记录，如果没有找到，则返回404错误响应

    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面

        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页

    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


# 删除电影
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页

@app.route('/home')
def home():
    return 'Welcome to My Watchlist!'


@app.route('/user/<name>')
def user_page(name):
    return 'User: %s' % escape(name)  # escape 防止输入的数据包含恶意代码 对name变量进行转义处理


@app.route('/test')
def test_url_for():
    # print(url_for('hello'))
    # print(url_for('user_page', name='greyli'))
    # print(url_for('test_url_for'))
    return 'Test page'

