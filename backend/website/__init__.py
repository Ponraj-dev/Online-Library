from datetime import timedelta
from os import path
from flask import Flask, jsonify, request, make_response
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
# from .celery_worker import create_celery_app
from config import DevelopmentConfig
from flask_cors import CORS
from flask_caching import Cache

# from celery import Celery

db = SQLAlchemy()
cache = Cache()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"


    CORS(app, resources={r"/*": {"origins": "http://localhost:8080", "allow_headers": "Content-Type, Authorization"}}, supports_credentials=True)
    cache.init_app(app)
    db.init_app(app)
    jwt = JWTManager(app)

    # celery =  create_celery_app(app)
    # celery.set_default()

    # Initialize Celery

    from .users import create_default_admin
    from .views import views
    from .users import auth_bp
    from .books import books_bp
    from .profile_1 import profile_bp
    from .Libraryregister import register_bp
    from .section import section_bp
    from .task import report_bp

    with app.app_context():
        create_database()

    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(section_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(views, url_prefix="/")

    @app.before_request
    def handle_options_request():
        if request.method == "OPTIONS":
            return _build_cors_preflight_response()


    return app

def create_database():
    if not path.exists(DB_NAME):
        db.create_all()
        from .users import create_default_admin
        create_default_admin()
        print("Created Database!")

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "http://localhost:8080")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    return response



