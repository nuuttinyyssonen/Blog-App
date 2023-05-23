from flask import Blueprint, redirect, render_template, session, request, url_for
from ...extensions.extensions import db
from ...models.models import Posts

blog_bp = Blueprint('blog_bp', __name__)

@blog_bp.route('/blog', methods=['GET', 'POST'])
def blog():

    if request.method == 'POST':
        blog_text = Posts(post=request.form.get('blog'), author=session['username'], title=request.form.get('title'))
        db.session.add(blog_text)
        db.session.commit()
        return redirect(url_for('blog_bp.blog'))
    
    return render_template('./main/blog.html')