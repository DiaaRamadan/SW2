from database import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from flask import Flask,jsonify
app = Flask(__name__)


Base = declarative_base()

engine = create_engine('sqlite:///database.db',
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool, echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/users', methods=['post'])
def index():
    userInfo = session.query(user).all()
    return jsonify(Users=[User.serilize for User in userInfo])

@app.route('/recommend/user/<int:user_id>/quiz')
def user_quizs(user_id):

    userInfo = session.query(user).filter_by(id=user_id).one()

    if userInfo.type == str(1):
        getIntersted = session.query(intersted).filter_by(user_id=user_id).first()

        quizs = session.query(quiz).filter(intersted.interested.like('%'+quiz.field+'%'))
        return jsonify(quizs=[q.serilize for q in quizs])
    return 'error type'


if __name__ == '__main__':
    app.secret_key = 'Super_secret_key'
    app.debug = True
    app.run(port=5001)
