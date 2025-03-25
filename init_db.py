"""
Database initialization script for Brevity blog
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from models import User, Post, Settings

app = create_app()

with app.app_context():
    # Check if we need to update schema
    try:
        # Try to query for slug column to see if it exists
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('post')]
        
        # If slug doesn't exist, we need to recreate or migrate
        if 'slug' not in columns:
            print("Adding slug column to Post table...")
            # For this simple script, we'll just recreate the tables
            # In production, you'd use flask-migrate to handle this properly
            db.drop_all()
            db.create_all()
            print("Database schema updated with new slug field.")
    except Exception as e:
        print(f"Error checking schema: {e}")
        # Just create all tables if there was an error
        db.create_all()
    
    # Check if settings exist, create if not
    if not Settings.query.first():
        settings = Settings(
            site_name="Brevity",
            site_description="A simple micro-blog engine powered by Python and Flask",
            posts_per_page=10,
            allow_registration=True
        )
        db.session.add(settings)
        
        print("Initial settings created.")
    
    # Check if admin user exists, create one if not
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", email="admin@example.com")
        admin.set_password("adminpassword")  # You should change this!
        db.session.add(admin)
        
        # Add a sample post
        post = Post(
            title="Welcome to Brevity",
            content="""
# Welcome to Brevity

This is a simple micro-blog engine powered by Python and Flask.

## Features

- Markdown support
- User authentication
- Simple and clean interface

Enjoy your new blog!
            """,
            is_published=True,
            slug="welcome-to-brevity",
            author=admin
        )
        db.session.add(post)
        
        print("Admin user and sample post created.")
    
    db.session.commit()
    
    print("Database initialization complete!") 