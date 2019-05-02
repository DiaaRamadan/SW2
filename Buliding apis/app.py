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

        quizs = session.query(quiz).filter(intersted.interested.like('%'+quiz.field+'%'))
        if quizs != '':
            return jsonify(quizs=[q.serilize for q in quizs])
        else:
            return jsonify(['no data'])
    return jsonify(data=['Error type'])


@app.route('/recommend/user/<int:user_id>/job')
def recommend_company(user_id):
    userInfo = session.query(user).filter_by(id=user_id).one()
    if userInfo.type == str(1):
        user_intr = session.query(intersted).filter_by(id=user_id).one()
        all_like_intersted = session.query(intersted).filter(intersted.interested.like('%'+user_intr.interested+'%')).all()
        for intr in all_like_intersted:
           needed_companies = session.query(user).filter_by(id=intr.user_id).all()
           if needed_companies != '':
               for company in needed_companies:
                   if(company.type == str(2)):

                        return jsonify(data=[company.serilize])

        else:
            return jsonify(['no data'])
    else:
        return jsonify(data=['error Type'])

@app.route('/recommend/company/<int:user_id>/user')
def recommend_user(user_id):
    userInfo = session.query(user).filter_by(id=user_id).one()
    if userInfo.type == str(2):
        user_intr = session.query(intersted).filter_by(id=user_id).one()
        all_like_intersted = session.query(intersted).filter(intersted.interested.like('%'+user_intr.interested+'%')).all()
        for intr in all_like_intersted:
           needed_companies = session.query(user).filter_by(id=intr.user_id).all()
           if needed_companies != '':
               for company in needed_companies:
                   if(company.type == str(1)):

                        return jsonify(data=[company.serilize])

        else:
            return jsonify(['no data'])
    else:
        return jsonify(data=['error Type'])

if __name__ == '__main__':
    app.secret_key = 'Super_secret_key'
    app.debug = True
    app.run(port=5001)
