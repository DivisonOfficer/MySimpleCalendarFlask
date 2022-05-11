from pydoc import describe
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(64), primary_key = True)
    

class Article(db.Model):
    __tablename__ = 'article'
    
    author = db.Column(db.String(32))

    title = db.Column(db.String(128))

    describtion = db.Column(db.String(512))

    url = db.Column(db.String(128), primary_key = True)

    urlToImage = db.Column(db.String(128))

    publishedAt = db.Column(db.String(32))


