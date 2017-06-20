from view import app, db
from model import *

def init():
    with app.app_context():
        db.drop_all()
        db.create_all()
        print 'init success'

if __name__ == '__main__':
    init()
