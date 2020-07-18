import os
import sys

import click

from flask import Flask
from flask import escape, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)


@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息


class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    # 全局的两个变量移动到这个函数内
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'}
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


@app.route("/")
@app.route("/home")
def hello():
    return "<h1>Welcome to My Watchlist!</h1>"


@app.route("/mises")
def mises():
    return "<h1>Welcome to My Watchlist!</h1>", 302, {'location': 'https://mises.org'}


@app.route("/austrian")
def austrian():
    return redirect('https://mises.com')


@app.route("/hayek")
def hayek():
    return redirect(url_for('mises'))

# URL内定义变量，规避恶意代码
@app.route("/user/<name>")
def user_page(name):
    return "User: %s" % escape(name)


@app.route("/AynRand/")
def hello_aynrand():
    return "<h1>Hello Ayn Rand!</h1><img src='https://static.ffx.io/images/$zoom_0.2015%2C$multiply_2.1164%2C$" \
           "ratio_1%2C$width_378%2C$x_0%2C$y_67/t_crop_custom/e_sharpen:25%2Cq_85%2Cf_auto/" \
           "1ed9787e5cb2615285bd3f969531a00096de1775'>"


@app.route("/Totoro/")
def hello_totoro():
    return "<h1>Hello Totoro!</h1><img src='http://helloflask.com/totoro.gif'>"


@app.route("/ali")
def ali():
    return "<h1>my alilyun host</h1><img src=url_for('static', filename='aliyun.png')>"


@app.route('/test')
def test_url_for():
    # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
    print(url_for('hello'))  # 输出：/
    # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
    print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
    print(url_for('user_page', name='peter'))  # 输出：/user/peter
    print(url_for('test_url_for'))  # 输出：/test
    # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
    print(url_for('test_url_for', num=2))  # 输出：/test?num=2
    return 'Test page'


"""
name = 'Hubery'
movies = [
    {'title': 'Dead Poets Society', 'year': '1989'}
    , {'title': 'A Perfect World', 'year': '1993'}
    , {'title': 'The Pork of Music', 'year': '2012'}
]
"""


@app.route('/index')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)


if __name__ == "__main__":
    app.run()


