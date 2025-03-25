from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from models import Post, Settings

posts_bp = Blueprint('posts', __name__)

@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    settings = Settings.get_settings()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        is_published = 'is_published' in request.form
        
        if not title:
            flash('Title is required', 'danger')
            return render_template('posts/create.html', settings=settings, post=request.form)
        
        post = Post(title=title, content=content, is_published=is_published, author=current_user)
        db.session.add(post)
        db.session.commit()
        
        flash('Post created successfully', 'success')
        return redirect(url_for('posts.view', slug=post.slug))
    
    return render_template('posts/create.html', settings=settings)

@posts_bp.route('/<slug>')
def view(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    settings = Settings.get_settings()
    
    if not post.is_published and (not current_user.is_authenticated or current_user.id != post.user_id):
        abort(404)
    
    return render_template('posts/view.html', post=post, settings=settings)

# Keep backward compatibility with ID-based URLs
@posts_bp.route('/id/<int:post_id>')
def view_by_id(post_id):
    post = Post.query.get_or_404(post_id)
    return redirect(url_for('posts.view', slug=post.slug))

@posts_bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    settings = Settings.get_settings()
    
    if current_user.id != post.user_id:
        abort(403)
    
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.is_published = 'is_published' in request.form
        
        if not post.title:
            flash('Title is required', 'danger')
            return render_template('posts/edit.html', post=post, settings=settings)
        
        db.session.commit()
        flash('Post updated successfully', 'success')
        return redirect(url_for('posts.view', slug=post.slug))
    
    return render_template('posts/edit.html', post=post, settings=settings)

@posts_bp.route('/<slug>/delete', methods=['POST'])
@login_required
def delete(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    
    if current_user.id != post.user_id:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully', 'success')
    return redirect(url_for('main.index')) 