from http import HTTPStatus

from email_validator import EmailNotValidError, validate_email
from flask import abort, jsonify
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_restful import Resource  # type: ignore
from flask_restful.reqparse import RequestParser  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from dms import db, jwt_blocklist
from dms.models import User

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
            user: User = dbsession.scalars(statement).one()
        except NoResultFound:
            abort_on_invalid_credentials()

        if not user.check_password_hash(password):
            abort_on_invalid_credentials()

        access_token = create_access_token(identity=user)
        return jsonify(access_token=access_token)

    @jwt_required()
    def delete(self):
        jti = get_jwt()['jti']
        jwt_blocklist.set(jti, "", expire=900)
        return {"message": "Logged out."}
