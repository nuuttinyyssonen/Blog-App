from flask import Blueprint, redirect, render_template, url_for, request
from ...extensions.extensions import db
from ...models.models import Posts

singlePost_bp = Blueprint('singlePost_bp', __name__)

@singlePost_bp.route('/posts/<id>', methods=['GET', 'POST'])
def singlePost(id):
    post = Posts.query.filter_by(id=id)
    if request.method == 'POST':
        Posts.query.filter_by(id=id).delete()
        db.session.commit()
        return redirect(url_for('posts_bp.posts'))
    return render_template('./post/singlepost.html', post=post, id=id)