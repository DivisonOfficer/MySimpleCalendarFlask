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
    __tablename__ = 'users'
    userId = Column(String(32), primary_key=True)
    def __init__(self, userId = None):
        self.userId = userId

class News(Base):
    __tablename__ = 'news'
    
    author = Column(String(32))

    title = Column(String(128))

    description = Column(String(512))

    url = Column(String(128), primary_key = True)

    urlToImage = Column(String(128))

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

    url = Column(String(128), primary_key = True)

    category = Column(String(32))
    
    def __init__(self, userId = None, url = None, category = None):
        self.userId = userId
        self.url = url
        self.category = category



Base.metadata.create_all(bind=engine) 




app = Flask(__name__)

timeFormat = "%Y-%m-%dT%H:%M:%SZ"
 
@app.route("/adduser", methods=['POST'])
def add_user():
    content = request.get_json(silent=True)
    userId = content["userId"]
    if db_session.query(User).filter_by(userId = userId).first() is None:
        u = User(userId = userId)
        db_session.add(u)
        db_session.commit()
        return jsonify(success=True), 200
    else:
        return jsonify(success=False), 200
#post MutableList<NewsData>
@app.route("/news/post", method = ['POST'])
def post_news():
    contents = request.get_json(silent=True)
    for content in contents:
        url = content['url']
        if db_session.query(News).filter_by(url = url).first() is None:
            urlToImage = content['urlToImage']
            description = content['description']
            title = content['title']
            author = content['author']
            publishedAt = datetime.strptime(content['publishedAt'],timeFormat)
            n = News(url = url, author=author,title=title,description=description,urlToImage=urlToImage,publishedAt=publishedAt)
            db_session.add(n)
    
    db_session.commit()
    return jsonify(success = True), 200

@app.rout("/news/scrap",method = ['POST'])
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

@app.rout("/news/scrap/get", method = ['GET'])
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

@app.rout("/news/scrap/delete", method = ['POST'])
def delete_scrap_news():
    content = request.get_json(silent=True)
    userId = content['userId']
    url = content['url']
    s = db_session.query(Scrap).filter_by(url = url).filter_by(userId = userId)
    if s is None:
        return jsonify(success = False), 200
    db_session.delete(s)
    return jsonify(success = True), 200




@app.route("/login", methods=['POST'])
def login():
    content = request.get_json(silent=True)
    name = content["name"]
    passwd = content["passwd"]
    check = False
    result = db_session.query(User).all()
    for i in result:
        if i.name== name and i.passwd== passwd:
            check = True
    return jsonify(success=check)


if __name__ == "__main__":
    app.run(host='localhost', port=8888)