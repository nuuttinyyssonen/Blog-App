from flask import Blueprint, url_for, redirect, render_template, session, request
from werkzeug.urls import url_parse
from flask_login import login_user
from ...extensions.extensions import login
from ...models.models import User

login_bp = Blueprint('login_bp', __name__)

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

@login_bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        session['username'] = request.form.get('username')

        if user is None or not user.check_password(request.form.get('password')):
            print('Invalid Password or Username')
            redirect(url_for('login_bp.login'))
        
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('blog_bp.blog')
        return redirect(next_page)

    return render_template('./auth/login.html')