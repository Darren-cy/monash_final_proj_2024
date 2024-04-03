from flask import Flask, render_template, g, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


# Load the environment variables
load_dotenv()
# Create the Flask app
app = Flask(__name__, instance_relative_config=True)
# Enable CORS
CORS(app)

# Load the configuration
app.config.from_object('dms.config.DevelopmentConfig')

# Initialize the database
db = SQLAlchemy(app)

# Initialize the migration engine
migrate = Migrate(app, db)

# Create the user model
from .models import User

# Create the database tables
with app.app_context():
    try:
        db.create_all()
        db.session.commit()
        current_app.db = db
    except:
        pass
# Register the index route

@app.route('/')
def index():
    return render_template('dashboard.html')

from . import auth
app.register_blueprint(auth.bp)

