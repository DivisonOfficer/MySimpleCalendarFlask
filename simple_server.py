

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response

import os
import random
from models import User, Article, Scrap, db

# This line is for solving flask's CORS error
# You need 'pip install flask_cors' to use flask_cors
#from flask_cors import CORS
from werkzeug.serving import WSGIRequestHandler
import json
WSGIRequestHandler.protocol_version = "HTTP/1.1"

app = Flask(__name__)

# This line is for solving flask's CORS error
#CORS(app)

global users
users = []

global pi
pi = 0.0

# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'

db.init_app(app)
db.app = app
db.create_all()


@app.route("/getuser", methods=['GET'])
def get_name():
    name = request.args.get('name')
    
    global users
    exist = False
    ret = {}
    for usr in users:
        if usr[0] == name:
            ret["username"] = usr[0]
            ret["age"] = usr[1]
            
            exist = True
            break
    
    # return jsonify(maze=string.decode('utf-8', 'ignore'))
    return jsonify (ret)

@app.route("/scrap/post", methods = ['POST'])
def scrap_post():
    content = request.get_json(silent=True)
    url = content["url"]
    category = content["category"]
    id = content["id"]
    scrap = Scrap(url, id, category)
    db.session.add(scrap)
    db.session.commit()
    
    return jsonify(success=True), 200

@app.route("scrap/get", method = ['GET'])
def get_scrap_post():
    userId = request.args.get('id')
    scrap = session.query(User).from_statement(
                    "SELECT * FROM scrap WHERE id=:id").\
                    params(id=userId).all()
    ret = {}
    ret['article'] = []
    for item in scrap :
        article = session.query(Article).from_statement(
            "SELECT * FROM article WHERE url=:url").\
                params(url = item.url).all()
        ret['article'].append(article)
    
    return jsonify(ret), 200

# article : List<NewsData>
@app.rout("article/post", method = ['POST'])
def article_post():
    content = request.get_json(silent=true)
    for item in content["article"]:
        





    
if __name__ == "__main__":
    app.run(host='localhost', port=8888)
