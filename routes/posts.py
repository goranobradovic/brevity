import logging
from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import Post, Settings
from extensions import db
from markdown import markdown

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

posts = Blueprint('posts', __name__)

def get_settings():
    return Settings.query.first()

def get_posts():
    return Post.query.order_by(Post.created_at.desc()).all()

@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        logger.info('Post created: {}'.format(title))
        return redirect(url_for('posts.view', slug=post.slug))
    settings = get_settings()
    logger.info('Rendering create post page')
    return render_template('posts/create.html', settings=settings)

@posts.route('/posts/<slug>')
def view(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    settings = get_settings()
    logger.info('Viewing post: {}'.format(post.title))
    return render_template('posts/view.html', post=post, settings=settings)

# Keep backward compatibility with ID-based URLs
@posts.route('/id/<int:post_id>')
def view_by_id(post_id):
    post = Post.query.get_or_404(post_id)
    return redirect(url_for('posts.view', slug=post.slug))

@posts.route('/posts/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        logger.error('Unauthorized edit attempt for post: {}'.format(post.title))
        abort(403)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        logger.info('Post edited: {}'.format(post.title))
        return redirect(url_for('posts.view', slug=post.slug))
    settings = get_settings()
    logger.info('Rendering edit page for post: {}'.format(post.title))
    return render_template('posts/edit.html', post=post, settings=settings)

@posts.route('/posts/<slug>/delete', methods=['POST'])
@login_required
def delete(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        logger.error('Unauthorized delete attempt for post: {}'.format(post.title))
        abort(403)
    db.session.delete(post)
    db.session.commit()
    logger.info('Post deleted: {}'.format(post.title))
    flash('Post deleted successfully')
    return redirect(url_for('main.index')) 