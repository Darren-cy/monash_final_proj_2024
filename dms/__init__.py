import os

from dotenv import load_dotenv
from flask import Flask, current_app, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from diskcache import Cache  # type: ignore

db: SQLAlchemy = SQLAlchemy()
jwt: JWTManager = JWTManager()
jwt_blocklist = Cache(r"d:\blocklist")


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # Create the app directory if it doesn't already exist
    try:
        os.makedirs(app.instance_path)
    except FileExistsError:
        pass
    global db
    # Initialize the database
    db.init_app(app)

    # Create the user model
    from .models import User, Document

    # Create the database tables
    with app.app_context():
        db.create_all()
        db.session.commit()
        current_app.db = db

    # Set up the JWT manager
    jwt.init_app(app)

    # Register the index route
    @app.route('/')
    def index():
        return render_template('dashboard.html')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import document
    app.register_blueprint(document.bp)

    from . import api
    app.register_blueprint(api.bp)
    return app


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jti = jwt_payload["jti"]
    token_in_blocklist = jwt_blocklist.get(jti)
    return token_in_blocklist is not None
