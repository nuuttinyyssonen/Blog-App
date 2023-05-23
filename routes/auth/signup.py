from flask import Blueprint, render_template, request, redirect, url_for, flash
from ...models.models import User
from ...extensions.extensions import db

signup_bp = Blueprint('signup_bp', __name__)

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':

        try:
            user = User(email=request.form.get('email'), username=request.form.get('username'))
            user.set_password_hash(request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login_bp.login'))
        except:
            flash('This email or username is already in use!')
            return redirect(url_for('signup_bp.signup'))

    return render_template('./auth/signin.html')