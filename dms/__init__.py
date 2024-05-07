from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Load the environment variables
load_dotenv()
# Create the Flask app
app = Flask(__name__, instance_relative_config=True,
            static_folder='static', template_folder='templates')
# Enable CORS
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)

# Initialize the JWT manager
jwt = JWTManager(app)

# Load the configuration
app.config.from_object('dms.config.DevelopmentConfig')

# Initialize the database
db = SQLAlchemy(app)

# Initialize the migration engine
migrate = Migrate(app, db)

# Create the user model
from .models import *

# Create the database tables
with app.app_context():
    db.create_all()
    db.session.commit()
# Register the index route


@app.route('/')
def index():
    return render_template('dashboard.html')


from dms import auth
from dms.api import user_api
from dms.api import display_upload_api
from dms import api
app.register_blueprint(api.bp)
app.register_blueprint(auth.bp)
app.register_blueprint(user_api.bp)
app.register_blueprint(display_upload_api.bp)



@jwt.user_identity_loader
def user_to_id(user):
    return user.id


@jwt.user_lookup_loader
def jwt_to_user(jwt_header, jwt_data):
    from .models import User
    id = jwt_data["sub"]
    return User.query.filter_by(id=id).one_or_none()