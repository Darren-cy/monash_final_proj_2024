from flask import Flask, render_template, send_from_directory, request
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os

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


from . import auth, api
app.register_blueprint(auth.bp)
app.register_blueprint(api.bp)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        # Create a folder named uploads in the static folder
        os.makedirs('dms/static/uploads/', exist_ok=True)
        file.save('dms/static/uploads/' + file.filename)
        return 'File uploaded successfully', 200
    except Exception as e:
        return str(e), 400
