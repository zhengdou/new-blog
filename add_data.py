from random import choice
from view import app, db
from model import *

AMOUNT = 10
TAGS = ['python', 'vim', 'web', 'mysql']

def add_data():
    with app.app_context():
        for i in xrange(AMOUNT):
        	title = 'title' + str(i+1)
        	category = choice(TAGS)
        	tags = 'python,vim'
        	md_content = '# ' + title
        	article = Article(title=title, category=category, tags=tags, md_content=md_content)

        	Category_category = Category.query.filter_by(name=category).first()
        	if not Category_category:
        		Category_category = Category(name=category)
        	else:
        		Category_category.amount += 1
        	db.session.add(article)
        	db.session.add(Category_category)
        	db.session.commit()
    print 'success'


if __name__ == '__main__':
    add_data()