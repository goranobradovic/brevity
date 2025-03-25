from flask import Flask, render_template
import os
from dotenv import load_dotenv
from extensions import db, migrate, login_manager

# Load environment variables
load_dotenv()

# Create app
def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///brevity.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Import routes and models (must be after db initialization to avoid circular imports)
    from routes.main import main
    from routes.auth import auth
    from routes.posts import posts
    from models import User, Post, Settings

    # Register blueprints
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(posts)

    # Create tables
    with app.app_context():
        db.create_all()

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        settings = Settings.query.first()
        return render_template('errors/404.html', settings=settings), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        settings = Settings.query.first()
        return render_template('errors/500.html', settings=settings), 500

    # Favicon route
    @app.route('/favicon.ico')
    def favicon():
        return app.send_static_file('favicon.ico')

    @app.route('/favicon.svg')
    def favicon_svg():
        return app.send_static_file('favicon.svg')

    return app

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True) 