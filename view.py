# coding = utf-8
'''view file'''
from flask import Flask, render_template, url_for


app = Flask(__name__)


@app.route('/')
def index():
    '''Index Page'''
    return render_template('index.html')


@app.route('/blog')
def blog():
    '''blog page'''
    return render_template('blog.html')


@app.route('/article')
def article():
    return render_template('article.html')


if __name__ == '__main__':
    app.run()
