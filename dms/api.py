from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, timezone
import dms.models as models
from dms import db, jwt
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies, \
    unset_jwt_cookies, jwt_required
from flask_cors import CORS

bp = Blueprint('api', __name__, url_prefix='/api/v1.0')
CORS(bp, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@bp.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        return jsonify({"error": "Username is required"}), 400
    elif not password:
        return jsonify({"error": "Password is required"}), 400

    user = models.User.query.filter_by(name=username).first()
    if user:
        return jsonify({"error": f"Username {username} is already registered."}), 400

    user = models.User(username, password, username + "@example.com")
    models.db.session.add(user)
    models.db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200


@bp.route('/refresh-token', methods=['POST', 'GET'])
def refresh_token():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    res = jsonify(accessToken=access_token)
    set_access_cookies(res, access_token)
    return res, 200


@bp.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if username == 'test' and password == 'test':
        access_token = create_access_token(identity=username)
        return jsonify(accessToken=access_token), 200

    return jsonify({"error": "Invalid username or password"}), 400


@bp.route('/logout', methods=['POST'])
def logout():
    res = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(res)
    return res, 200


@bp.route('/protected', methods=['GET', 'POST'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(foo='bar',user = current_user), 200
