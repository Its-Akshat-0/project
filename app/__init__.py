from flask import Flask, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta

# Initialize extensions globally
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'admin_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Session cookie security
    # NOTE: SESSION_COOKIE_SECURE requires HTTPS to actually send the Secure flag.
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    # Make sessions expire after 30 minutes of inactivity
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    # Initialize app with extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models *inside* the function (prevents circular import)
    from app import models

    # Register Blueprints
    from app.routes.auth import auth
    app.register_blueprint(auth)

    # Initialize Flask-Login
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # user_loader must be registered after models are imported
    @login_manager.user_loader
    def load_user(user_id):
        try:
            return models.Users.query.get(int(user_id))
        except Exception:
            return None

    # Security: prevent caching of HTML pages so browser 'Back' won't show protected pages after logout
    @app.after_request
    def add_security_headers(response):
        try:
            content_type = response.headers.get('Content-Type', '')
            if content_type.startswith('text/html'):
                response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
                response.headers['Pragma'] = 'no-cache'
                response.headers['Expires'] = '0'
        except Exception:
            # If anything goes wrong, don't break the response path.
            pass
        return response

    @app.route('/')
    def home():
        if 'admin' in session:
            return redirect(url_for('auth.admin_dashboard'))
        return redirect(url_for('auth.login'))

    return app
