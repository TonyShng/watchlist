from flask import Flask, url_for, escape, render_template
from flask_sqlalchemy import SQLAlchemy
import os
import sys

app = Flask(__name__)

# 在扩展类实例化前加载配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app


class User(db.Model):  # 表名将会是 user (自动生成，小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 user (自动生成，小写处理)
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    print(user, movies)
    return render_template('index.html', user=user, movies=movies)
# return '<h1>Hello RainTwo!</h1><img src="http://helloflask.com/totoro.gif">'

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
