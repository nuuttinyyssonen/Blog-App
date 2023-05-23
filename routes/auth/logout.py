from flask import url_for, redirect, Blueprint
from flask_login import logout_user

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login_bp.login'))