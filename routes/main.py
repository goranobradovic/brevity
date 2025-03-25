from flask import Blueprint, render_template, current_app, request
from models import Post
from extensions import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts)

@main.route('/about')
def about():
    return render_template('about.html') 