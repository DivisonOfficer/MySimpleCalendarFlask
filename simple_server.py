

from flask import Flask
from flask import request
from flask import jsonify
from flask import Response
import os
import random

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
@app.route("/monte-carlo/pi", methods = ['GET'])
def get_monte_pi():
    n = int(request.args.get('n'))
    global pi
    m = 0
    for i in range(n) :
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0 :
            m = m + 1
    pi = m / n * 4
    ret = {}
    ret["pi"] = pi
    return jsonify (ret), 200

@app.route("/get/pi", methods = ['GET'])
def get_pi():
    global pi
    ret = {}
    ret["pi"] = pi
    return jsonify (ret), 200

@app.route("/update/pi", methods=['POST'])
def update_pi():
    global pi
    content = request.get_json(silent=True)
    new_pi = content["pi"]
    pi = new_pi
    return jsonify(success=True), 200

@app.route("/adduser", methods=['POST'])
def update_name():
    content = request.get_json(silent=True)
    
    username = content["username"]
    age = content["age"]

    global users
    exist = False
    for usr in users:
        if usr[0] == username:
            exist = True

    if exist is False:
        users.append ([username, age])
        return jsonify(success=True)
    else:
        return jsonify(success=False)
    
if __name__ == "__main__":
    app.run(host='localhost', port=8888)
