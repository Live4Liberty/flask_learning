from flask import Flask
from flask import escape, url_for, redirect, render_template

app = Flask(__name__)


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


name = 'Hubery'
movies = [
    {'title': 'Dead Poets Society', 'year': '1989'}
    , {'title': 'A Perfect World', 'year': '1993'}
    , {'title': 'The Pork of Music', 'year': '2012'}
]


@app.route('/index')
def index():
    return render_template('index.html', name=name, movies=movies)


if __name__ == "__main__":
    app.run()


