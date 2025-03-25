from flask import Blueprint, render_template, current_app, request
from models import Post, Settings
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    settings = Settings.get_settings()
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(is_published=True).order_by(Post.created_at.desc()) \
        .paginate(page=page, per_page=settings.posts_per_page)
    return render_template('index.html', posts=posts, settings=settings)

@main_bp.route('/about')
def about():
    settings = Settings.get_settings()
    return render_template('about.html', settings=settings) 