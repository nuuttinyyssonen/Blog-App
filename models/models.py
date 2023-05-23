from ..extensions.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), index=True, unique=True)
    username = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(88))

    def set_password_hash(self, password):
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Posts(db.Model):
    __tablename__ = 'Posts'

    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.String(10000), index=True, unique=False)
    author = db.Column(db.String(180), index=True, unique=False)
    title = db.Column(db.String(300), index=True, unique=False)
