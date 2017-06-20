# coding = utf-8
from flask import Flask, render_template, url_for, jsonify, request
from flask_restful import reqparse, Api, Resource
from model import *


app = Flask(__name__)
api = Api(app)
app.secret_key = 'liangchuannan'
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


@app.route('/article/<int:id>')
def article(id):
	article = articles[id-1]
	return render_template('article.html', article=article)


class CommentList(Resource):
	def get(self):
		return comments

	def post(self):
		parser = reqparse.RequestParser()
		parser.add_argument('user', type = str, required = True,help = 'No user provided')
		parser.add_argument('date', type = str, required = True,help = 'No user provided')
		parser.add_argument('content', type = str, required = True,help = 'No user provided')
		args = parser.parse_args()
		args['id'] = comments[-1]['id'] + 1
		comments.append(args)
		return {'id': args['id']}


api.add_resource(CommentList, '/comments')






if __name__ == '__main__':
    app.run()
