from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import dms.models as models
from dms import db, jwt
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies, \
    unset_jwt_cookies, jwt_required
from flask_cors import CORS

bp = Blueprint('user_api', __name__, url_prefix='/api/v1.0')
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@bp.route('/register', methods=['POST'])
def register():
    try: 
        username = request.json.get('username')
        password = request.json.get('password')
        email = request.json.get('email')

        if not username or not password or not email:
            return jsonify({"error": "Username, password and email are required"}), 409

        user = models.User.query.filter_by(name=username).first()
        if user:
            return jsonify({"error": f"Username {username} is already registered."}), 409

        hash_password = generate_password_hash(password)
        user = models.User(name=username, password=hash_password, email=email)
        models.db.session.add(user)
        models.db.session.commit()

        return jsonify({"message": "User registered successfully"}), 200
    except Exception as e:
        return jsonify({"error": {e}}), 400


@bp.route('/refresh-token', methods=['POST', 'GET'])
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    res = jsonify(accessToken=access_token)
    set_access_cookies(res, access_token)
    return res, 200


@bp.route('/login', methods=['POST'])
def login():
    try: 
        username = request.json.get('username')
        password = request.json.get('password')

        # Get the user from the database
        user = models.User.query.filter_by(name=username).first()
        if not user:
            return jsonify({"error": "Invalid username or password"}), 400
        
        password_hash = user.password
        if check_password_hash(password_hash, password):
            access_token = create_access_token(identity=username)
            res = jsonify(accessToken=access_token)
            set_access_cookies(res, access_token)
            return res, 200
        else:
            return jsonify({"error": "Invalid username or password"}), 400
    except Exception as e:
        return jsonify({"error": {e}}), 400


@bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        res = jsonify({"message": "Logout successful"})
        unset_jwt_cookies(res)
        return res, 200
    except Exception as e:
        return jsonify({"error": {e}}), 400


@bp.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    try:
        current_user = get_jwt_identity()
        user = models.User.query.filter_by(name=current_user).first()
        return jsonify({"username": user.name, "email": user.email}), 200
    except Exception as e:
        return jsonify({"error": {e}}), 400