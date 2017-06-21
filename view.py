# coding = utf-8
from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask_restful import reqparse, Api, Resource
from model import *


app = Flask(__name__)
api = Api(app)
app.secret_key = 'temp secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
PER_PAGE = 4


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    page = request.args.get('page', '1')
    pagination = Article.query.order_by(Article.date.desc()).paginate(int(page), PER_PAGE, True)
    categorys = Category.query.all()
    return render_template('blog.html', pagination=pagination, categorys=categorys)


@app.route('/article/<name>')
def article(name):
	article = Article.query.get_or_404(title=name)
	return render_template('article.html', article=article)


class Article(Resource):
	def get(self, name):
		article = Article.query.get_or_404(title=name)
		return {'article': article}

	def put(self, name):
		params = ['title', 'category', 'tags', 'md_content']
		parser = reqparse.RequestParser()
		for param in params:
			parser.add_argument(param, type = str, required = True,help = 'No '+param+' provided')
		article = Article()
		args = parser.parse_args()
		for key, value in args.items():
			article[key] = value
		try:
			db.session.add(article)
			db.session.commit()
			return redirect('/article/name')
		except Exception, e:
			return {'message': e}, 400



class CommentList(Resource):
	def get(self):
		article_id = request.args.get('article_id', None)
		if article_id:
			comments = Comment.query.filter_by(article_id=article_id).all()
			return {'comments': comments}
		else:
			return {'message': 'article id is wrong'}, 400

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user', type = str, required = True,help = 'No user provided')
		parser.add_argument('date', type = str, required = True,help = 'No user provided')
		parser.add_argument('content', type = str, required = True,help = 'No user provided')
		args = parser.parse_args()
		args['id'] = comments[-1]['id'] + 1
		comments.append(args)
		return {'id': args['id']}


api.add_resource(CommentList, '/api/comments')
api.add_resource(Article, '/api/article/<name>')






if __name__ == '__main__':
    app.run()
