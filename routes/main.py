from flask import Blueprint, render_template, current_app, request
from models import Post, Settings
from extensions import db

main = Blueprint('main', __name__)

def get_settings():
    return Settings.query.first()

@main.route('/')
def index():
    settings = get_settings()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts, settings=settings)

@main.route('/about')
def about():
    settings = get_settings()
    return render_template('about.html', settings=settings) 