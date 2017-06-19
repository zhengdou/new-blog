# coding = utf-8
from flask import Flask, render_template, url_for, jsonify, request
from flask_restful import reqparse, Api, Resource


app = Flask(__name__)
api = Api(app)





articles = [
		{
			'id': 1,
			'title': 'first article',
			'summary': 'first summary',
			'content': 'first content',
			'date': '2010-10-10',
			'tags': 'first,python',
			'read': 10
		},
		{
			'id': 2,
			'title': 'second article',
			'summary': 'second summary',
			'content': 'second content',
			'date': '2010-10-10',
			'tags': 'first,python',
			'read': 10
		},
		{
			'id': 3,
			'title': 'third article',
			'summary': 'third summary',
			'content': 'third content',
			'date': '2010-10-10',
			'tags': 'first,python',
			'read': 10
		}
	]
categorys = [
		{
			'name': 'python',
			'amount': 10
		},
		{
			'name': 'vim',
			'amount': 20
		},
		{
			'name': 'flask',
			'amount': 8
		}
	]
comments = [
		{
			'id': 0,
			'user': 'zheng',
			'date': '2012-10-11',
			'content': 'zheng comment this article'
		},
		{
			'id': 1,
			'user': 'ang',
			'date': '2013-6-11',
			'content': 'ang comment this article'
		},
		{
			'id': 2,
			'user': 'tmy',
			'date': '2017-6-5',
			'content': 'tmy comment this article'
		}
	]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/blog')
def blog():
    return render_template('blog.html', articles=articles, categorys=categorys)


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
