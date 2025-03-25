from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
import markdown
import re
from sqlalchemy import event

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), nullable=False, unique=True, index=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_published = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @property
    def html_content(self):
        return markdown.markdown(self.content, extensions=['fenced_code', 'tables'])
    
    def __repr__(self):
        return f'<Post {self.title}>'
    
    @staticmethod
    def generate_slug(target, value, oldvalue, initiator):
        """Generate a URL-friendly slug from the title."""
        if value and (not target.slug or value != oldvalue):
            # Convert to lowercase and replace spaces with hyphens
            slug = re.sub(r'[^\w\s-]', '', value.lower())
            slug = re.sub(r'[\s_-]+', '-', slug)
            slug = slug.strip('-')
            
            # Make sure slug is unique
            original_slug = slug
            count = 1
            while Post.query.filter_by(slug=slug).first() is not None:
                slug = f"{original_slug}-{count}"
                count += 1
            
            target.slug = slug

# Set up the event listener to generate slug before inserting/updating Post
event.listen(Post.title, 'set', Post.generate_slug, retval=False)

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