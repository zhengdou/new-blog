# coding = utf-8
from flask import Flask, render_template, url_for, jsonify, request, redirect, abort
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
	article = Article.query.filter_by(title=name).first()
	if not article:
		return abort(404)
	return render_template('article.html', article=article)


class Post(Resource):
	def get(self):
		id = request.args.get('id', None)
		if not id:
			return {'message': 'no id'}, 400
		article = Article.query.get_or_404(id)
		return article

	def put(self):
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
			resp = []
			for comment in comments:
				resp.append({'id':comment.id, 'reply_user':comment.reply_user, 'user':comment.user, 'date':comment.date.strftime("%Y-%m-%d %H:%M:%S"), 'content':comment.content})
			return resp
		else:
			return {'message': 'article id is wrong'}, 400

	def post(self):
		article_id = request.args.get('article_id', None)
		parser = reqparse.RequestParser()
		parser.add_argument('user', required = True,help = 'No user provided')
		parser.add_argument('reply_user', required = True,help = 'No user provided')
		parser.add_argument('content', required = True,help = 'No user provided')
		args = parser.parse_args()
		comment = Comment(article_id=article_id, reply_user=args['reply_user'], user=args['user'], content=args['content'])
		db.session.add(comment)
		db.session.commit()
		new_comment = Comment.query.filter_by(article_id = article_id, user = args['user']).\
			order_by(Comment.date.desc()).first()
		return {'id':new_comment.id, 'date':new_comment.date.strftime("%Y-%m-%d %H:%M:%S")}


api.add_resource(CommentList, '/api/comments')
api.add_resource(Post, '/api/article')






if __name__ == '__main__':
    app.run()
