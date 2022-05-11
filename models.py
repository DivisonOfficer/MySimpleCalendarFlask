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

    description = db.Column(db.String(512))

    url = db.Column(db.String(128), primary_key = True)

    urlToImage = db.Column(db.String(128))

    publishedAt = db.Column(db.String(32))

    def __init__(self, url = "", author = "", title = "", description = "",urlToImage = "",publishedAt = "") :
        self.url = url;
        self.author = author
        self.title = title
        self.description = description
        self.urlToImage = urlToImage
        self.publishedAt = publishedAt

   

class Scrap(db.Model):
    __tablename__ = 'scrap'

    id = db.Column(db.String(64), primary_key = True)

    url = db.Column(db.String(128), primary_key = True)

    category = db.Column(db.String(32))
    
    def __init__(self, id = "", url = "", category = ""):
        self.id = id
        self.url = url
        self.category = category

