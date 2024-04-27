from flask_restful import Resource  # type: ignore
from flask import current_app
from dms.models import User
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from http import HTTPStatus

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
