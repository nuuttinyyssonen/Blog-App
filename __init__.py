from flask import Flask
from .extensions.extensions import db, login
from decouple import config
from .routes.auth.login import login_bp
from .routes.auth.signup import signup_bp
from .routes.auth.logout import logout_bp
from .routes.main.blog import blog_bp
from .routes.main.search import search_bp
from .routes.post.allposts import posts_bp
from .routes.post.singlepost import singlePost_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db.init_app(app)
login.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.register_blueprint(login_bp)
app.register_blueprint(signup_bp)
app.register_blueprint(blog_bp)
app.register_blueprint(search_bp)
app.register_blueprint(posts_bp)
app.register_blueprint(singlePost_bp)
app.register_blueprint(logout_bp)