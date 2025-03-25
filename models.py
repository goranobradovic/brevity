from extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import markdown
import re
from slugify import slugify
from sqlalchemy import event

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def html_content(self):
        return markdown.markdown(self.content, extensions=['fenced_code', 'tables', 'mdx_math'], 
                               extension_configs={
                                   'mdx_math': {
                                       'enable_dollar_delimiter': True,
                                       'add_preview': True
                                   }
                               })
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    def generate_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1
        while Post.query.filter_by(slug=slug).first() is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

@event.listens_for(Post.title, 'set')
def update_slug_on_title_change(target, value, oldvalue, initiator):
    if value != oldvalue:
        target.slug = target.generate_slug()

@event.listens_for(Post, 'before_insert')
def set_slug_before_insert(mapper, connection, target):
    if not target.slug:
        target.slug = target.generate_slug()

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(100), default='Brevity')
    site_description = db.Column(db.Text, default='A simple micro-blog engine')
    posts_per_page = db.Column(db.Integer, default=10)
    allow_registration = db.Column(db.Boolean, default=True)
    
    @classmethod
    def get_settings(cls):
        """Get the settings or create default if not exists"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings 