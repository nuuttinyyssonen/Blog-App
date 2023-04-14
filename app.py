from flask import Flask, render_template, redirect, url_for, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse
from flask_login import LoginManager, login_user, UserMixin, logout_user
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import BooleanField
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_mail import Mail, Message
from decouple import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'nuutti.project@gmail.com'
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = 'nuutti.project@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

mail = Mail(app)

s = URLSafeTimedSerializer('ThisIsSecret')

login = LoginManager(app)
login.login_view = 'login'

@app.before_first_request
def create_tables():
    db.create_all()

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

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


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        session['username'] = request.form.get('username')

        if user is None or not user.check_password(request.form.get('password')):
            print('Invalid Password or Username')
            redirect(url_for('login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('blog')
        return redirect(next_page)

    return render_template('login.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():

    if request.method == 'POST':
        user = User(email=request.form.get('email'), username=request.form.get('username'))
        user.set_password_hash(request.form.get('password'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signin.html')

@app.route('/reset', methods=['GET', 'POST'])
def reset():
    if request.method == 'POST':
        email = request.form.get('email')
        token = s.dumps(email, salt='password-reset')
        msg = Message('Password Reset', sender='nuutti.project@gmail.com', recipients=[email])
        link = url_for('password_reset', token=token, _external=True)
        msg.body = 'Your link is {}'.format(link)
        mail.send(msg)
    
    return render_template('reset.html')

@app.route('/password_reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    try:
        email = s.loads(token, salt='password-reset', max_age=3600)
    except SignatureExpired:
        return '<h1>The token is expired</h1>'

@app.route('/blog', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        blog_text = Posts(post=request.form.get('blog'), author=session['username'], title=request.form.get('title'))
        db.session.add(blog_text)
        db.session.commit()
        return redirect(url_for('blog'))
    
    return render_template('blog.html')

@app.route('/posts/', methods=['GET', 'POST'])
def posts():
    posts = Posts.query.filter_by(author=session['username'])
    post = db.session.query(db.session.query(Posts).filter_by(title=request.form.get('search')).exists()).scalar()
    if request.method == 'POST':
        inputValue = request.form.get('search')
        searcBtn = request.form.get('searchBtn', False)
        blogPosts = Posts.query
        global blogPost
        blogPost = blogPosts.filter(Posts.title.like('%' + inputValue + '%'))
        return redirect(url_for('search'))

    return render_template('posts.html', posts=posts)

@app.route('/posts/<id>', methods=['GET', 'POST'])
def singlePost(id):
    post = Posts.query.filter_by(id=id)
    if request.method == 'POST':
        Posts.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('posts'))
    return render_template('singlepost.html', post=post, id=id)

@app.route('/search')
def search():
    return render_template('search.html', blogPost=blogPost)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))