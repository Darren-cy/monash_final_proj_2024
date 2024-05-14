from http import HTTPStatus
from werkzeug.security import check_password_hash

from flask import abort, jsonify
from flask_restful import Resource  # type: ignore
from flask_restful.reqparse import RequestParser  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from email_validator import EmailNotValidError, validate_email
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from dms.models import User
from dms import jwt_blocklist, db


parser = RequestParser()
parser.add_argument("email", required=True)
parser.add_argument("password", required=True)


def abort_on_invalid_credentials():
    abort(
        HTTPStatus.UNAUTHORIZED, "The email or password is incorrect.")


class SessionResource(Resource):
    def post(self):
        args = parser.parse_args()
        email = args['email']
        password = args['password']
        try:
            emailInfo = validate_email(email, check_deliverability=False)
            email = emailInfo.normalized
        except EmailNotValidError:
            abort_on_invalid_credentials()

        statement = select(User).where(User.email == email)
        dbsession = db.session
        try:
            user = dbsession.scalars(statement).one()
        except NoResultFound:
            abort_on_invalid_credentials()

        if not check_password_hash(user.password, password):
            abort_on_invalid_credentials()

        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)

    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        jwt_blocklist.set(jti, "", expire=900)
        return {"message": "Logged out."}
