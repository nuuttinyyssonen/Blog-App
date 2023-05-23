from flask import Blueprint, session, request, redirect, url_for, render_template
from ...extensions.extensions import db
from ...models.models import Posts

posts_bp = Blueprint('posts_bp', __name__)


@posts_bp.route('/posts/', methods=['GET', 'POST'])
def posts():
    posts = Posts.query.filter_by(author=session['username'])
    post = db.session.query(db.session.query(Posts).filter_by(title=request.form.get('search')).exists()).scalar()
    if request.method == 'POST':
        inputValue = request.form.get('search')
        session['searchValue'] = inputValue
        return redirect(url_for('search_bp.search'))

    return render_template('./post/posts.html', posts=posts)