from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from models import Post, Settings
from extensions import db
from markdown import markdown

posts = Blueprint('posts', __name__)

def get_settings():
    return Settings.query.first()

@posts.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('posts.view', slug=post.slug))
    settings = get_settings()
    return render_template('posts/create.html', settings=settings)

@posts.route('/<slug>')
def view(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    settings = get_settings()
    return render_template('posts/view.html', post=post, settings=settings)

# Keep backward compatibility with ID-based URLs
@posts.route('/id/<int:post_id>')
def view_by_id(post_id):
    post = Post.query.get_or_404(post_id)
    return redirect(url_for('posts.view', slug=post.slug))

@posts.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('posts.view', slug=post.slug))
    settings = get_settings()
    return render_template('posts/edit.html', post=post, settings=settings)

@posts.route('/<slug>/delete', methods=['POST'])
@login_required
def delete(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully')
    return redirect(url_for('main.index')) 