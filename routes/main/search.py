from flask import render_template, Blueprint, session
from ...models.models import Posts

search_bp = Blueprint('search_bp', __name__)

@search_bp.route('/search')
def search():
    searched_post = session['searchValue']
    blogPosts = Posts.query
    blogPost = blogPosts.filter(Posts.title.like('%' + searched_post + '%'))
    return render_template('./main/search.html', blogPost=blogPost)