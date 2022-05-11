from sqlalchemy import create_engine 
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, Integer, String

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

class Article(Base):
    __tablename__ = 'article'
    
    author = Column(String(32))

    title = Column(String(128))

    description = Column(String(512))

    url = Column(String(128), primary_key = True)

    urlToImage = Column(String(128))

    publishedAt = Column(String(32))

    def __init__(self, url = None, author = None, title = None, description = None,urlToImage = None,publishedAt = None) :
        self.url = url;
        self.author = author
        self.title = title
        self.description = description
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt

   

class Scrap(Base):
    __tablename__ = 'scrap'

    id = Column(String(64), primary_key = True)

    url = Column(String(128), primary_key = True)

    category = Column(String(32))
    
    def __init__(self, id = None, url = None, category = None):
        self.id = id
        self.url = url
        self.category = category



Base.metadata.create_all(bind=engine) 




app = Flask(__name__)
 
@app.route("/adduser", methods=['POST'])
def add_user():
    content = request.get_json(silent=True)
    name = content["name"]
    passwd = content["passwd"]
    if db_session.query(User).filter_by(name=name).first() is None:
        u = User(name=name, passwd=passwd)
        db_session.add(u)
        db_session.commit()
        return jsonify(success=True)
    else:
        return jsonify(success=False)

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