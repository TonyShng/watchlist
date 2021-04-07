
from flask import Flask, url_for, escape

app = Flask(__name__)

@app.route('/')
def hello():
	return '<h1>Hello RainTwo!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/home')
def home():
	return 'Welcome to My Watchlist!'


@app.route('/user/<name>')
def user_page(name):
	return 'User: %s' %escape(name)  # escape 防止输入的数据包含恶意代码 对name变量进行转义处理


@app.route('/test')
def test_url_for():
	# print(url_for('hello'))
	# print(url_for('user_page', name='greyli'))
	# print(url_for('test_url_for'))
	return 'Test page'





