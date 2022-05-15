from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime

from flask import Flask
from flask import request
from flask import jsonify
from werkzeug.serving import WSGIRequestHandler
import json
WSGIRequestHandler.protocol_version = "HTTP/1.1"

USER = "divisonofficer"
PW = "RcbQhScwkfD58Zq"
URL = "database-1.cr2bsidmj0be.ap-northeast-2.rds.amazonaws.com"
PORT = "5432"
DB = "postgres"

engine= create_engine("postgresql://{}:{}@{}:{}/{}".format(USER, PW, URL,PORT, DB))
db_session= scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base= declarative_base()
Base.query= db_session.query_property()


class User(Base):
    __tablename__ = 'userdatas'
    userId = Column(String(32), primary_key=True)
    passWd = Column(String(32))
    def __init__(self, userId = None, passWd = None):
        self.userId = userId
        self.passWd = passWd

class News(Base):
    __tablename__ = 'newsv2'
    
    author = Column(String(256))

    title = Column(String(256))

    description = Column(String(512))

    url = Column(String(512), primary_key = True)

    urlToImage = Column(String(512))

    publishedAt = Column(DateTime)

    def __init__(self, url = None, author = None, title = None, description = None,urlToImage = None,publishedAt = None) :
        self.url = url;
        self.author = author
        self.title = title
        self.description = description
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt

   

class Scrap(Base):
    __tablename__ = 'scrap'

    userId = Column(String(32), primary_key = True)

    url = Column(String(512), primary_key = True)

    category = Column(String(32))
    
    def __init__(self, userId = None, url = None, category = None):
        self.userId = userId
        self.url = url
        self.category = category



Base.metadata.create_all(bind=engine) 




app = Flask(__name__)

timeFormat = "%Y-%m-%dT%H:%M:%SZ"
 
@app.route("/user/add", methods=['POST'])
def add_user():
    content = request.get_json(silent=True)
    userId = content["userId"]
    passWd = content["passWd"]
    if db_session.query(User).filter_by(userId = userId).first() is None:
        u = User(userId = userId, passWd= passWd)
        db_session.add(u)
        db_session.commit()
        return jsonify(success=True), 200
    else:
        return jsonify(success=False), 200
@app.route("/user/login", methods = ['POST'])
def login():
    content = request.get_json(silent=True)
    userId = content["userId"]
    passWd = content["passWd"]
    if db_session.query(User).filter_by(userId = userId).first() is None:
        
        return jsonify(success=False), 400
    else:
        u = db_session.query(User).filter_by(userId = userId).first()
        if u.passWd == passWd:
            return jsonify(success = True), 200

        return jsonify(success=False), 400

#post MutableList<NewsData>
@app.route("/news/post", methods = ['POST'])
def post_news():
    contents = request.get_json(silent=True)
    for content in contents['newsList']:
        url = content['url']
        if db_session.query(News).filter_by(url = url).first() is None:
            title = content['title']
            if 'author' in content :
                author = content['author']
            else:
                author = None
            if 'urlToImage' in content:
                urlToImage = content['urlToImage']
            else :
                urlToImage = None
            if 'description' in content:
                description = content['description']
            else :
                description = None
            publishedAt = datetime.strptime(content['publishedAt'],timeFormat)
            n = News(url = url, author=author,title=title,description=description,urlToImage=urlToImage,publishedAt=publishedAt)
            db_session.add(n)
    
    db_session.commit()
    return jsonify(success = True), 200
@app.route("/news/get", methods = ['POST'])
def get_news():
    content = request.get_json(silent=True)
    url = content['url']
    news = db_session.query(News).filter_by(url = url).first()
    if(news is None):
        return jsonify(success = False), 201
    n = {}
    n['url'] = news.url
    n['urlToImage'] = news.urlToImage
    n['description'] = news.description
    n['publishedAt'] = news.publishedAt.strftime(timeFormat)
    n['author'] = news.author
    n['title'] = news.title
    return jsonify(n), 200



@app.route("/news/scrap",methods = ['POST'])
def scrap_news():
    content = request.get_json(silent=True)
    url = content['url']
    userId = content['userId']
    category = content['category']
    if db_session.query(Scrap).filter_by(url = url).filter_by(userId = userId).first() is None:
        s = Scrap(userId = userId, url = url, category = category)
        db_session.add(s)
        db_session.commit()
    return jsonify(success = True), 200

@app.route("/news/scrap/get", methods = ['GET'])
def get_scrap_news():
    userId = request.args.get('userId')
    posts = db_session.query(Scrap).filter_by(userId = userId)
    ret = []
    for post in posts:
        news = db_session.query(News).filter_by(url = post.url).first()
        n = {}
        n['url'] = news.url
        n['urlToImage'] = news.urlToImage
        n['description'] = news.description
        n['publishedAt'] = news.publishedAt.strftime(timeFormat)
        n['author'] = news.author
        n['title'] = news.title
        n['category'] = post.category
        ret.append(n)
    return jsonify(ret), 200

@app.route("/news/scrap/delete", methods = ['POST'])
def delete_scrap_news():
    content = request.get_json(silent=True)
    userId = content['userId']
    url = content['url']
    s = db_session.query(Scrap).filter_by(url = url).filter_by(userId = userId)
    if s is None:
        return jsonify(success = False), 200
    db_session.delete(s)
    return jsonify(success = True), 200



if __name__ == "__main__":
    app.run(host='localhost', port=8888)