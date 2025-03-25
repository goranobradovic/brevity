import logging
from flask import Blueprint, render_template, current_app, request
from models import Post, Settings
from extensions import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

def get_settings():
    return Settings.query.first()

@main.route('/')
def index():
    settings = get_settings()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    logger.info('Rendering index page with {} posts'.format(len(posts)))
    return render_template('index.html', posts=posts, settings=settings)

@main.route('/about')
def about():
    settings = get_settings()
    logger.info('Rendering about page')
    return render_template('about.html', settings=settings)
