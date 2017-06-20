# coding=utf-8
from datetime import datetime
import re
from flask_sqlalchemy import SQLAlchemy
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html


DB_URI = 'mysql://root:19930614@localhost/blog'
db = SQLAlchemy()


class HighlightRenderer(mistune.Renderer):
    def block_code(self, code, lang):
        if not lang:
            return '\n<pre><code>%s</code></pre>\n'\
                %mistune.escape(code)
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = html.HtmlFormatter()
        return highlight(code, lexer, formatter)

def m2h(md_string):
    '''
        make markdown content to html content
    '''
    renderer = HighlightRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(md_string)

def delHtmlTag(html_content):
    '''
    delete html tags, used for summary
    '''
    r = re.compile(r'<[^>]+>', re.S)
    return r.sub('', html_content)
    

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True)
    category = db.Column(db.String(32), default='未分类')
    tags = db.Column(db.String(128), nullable=True)
    summary = db.Column(db.Text)
    md_content = db.Column(db.Text)
    html_content = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    read_amount = db.Column(db.Integer, default=0)
    
    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        target.html_content = m2h(value)

    @staticmethod
    def on_changed_html_content(target, value, oldvalue, initiator):
        html = delHtmlTag(value)
        if len(html) > 200:
            target.summary = html[:200]
        else:
            target.summary = html

    def __repr__(self):
        return '<Article %r>'%self.title 

db.event.listen(Article.md_content, 'set', Article.on_changed_content)
db.event.listen(Article.html_content, 'set', Article.on_changed_html_content)


class Category(db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32), unique=True)
    amount = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Category %r>'%self.name


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    user = db.Column(db.String(128))
    head = db.Column(db.String(128), default='/static/defaulthead.jpg')
    reply_user = db.Column(db.String(128), nullable=True)
    content = db.Column(db.Text)
    hide = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Comment %r>'%self.name
