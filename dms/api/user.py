from http import HTTPStatus

from flask import current_app
from flask_restful import Resource  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from dms.models import User


class UserResource(Resource):
    def get(self, id):
        session = current_app.db.session
        query = select(User).where(User.id == id)
        try:
            user = session.scalars(query).one()
        except NoResultFound:
            return {"error": "User not found."}, HTTPStatus.NOT_FOUND
        else:
            return {"id": user.id, "name": user.name, "email": user.email}

    def post(self):
        return {"msg": "Not implemented"}, HTTPStatus.METHOD_NOT_ALLOWED

    def put(self):
        return {"msg": "Not implemented"}, HTTPStatus.METHOD_NOT_ALLOWED
