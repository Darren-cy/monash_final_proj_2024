from typing import Sequence
from flask import abort
from flask_restful import Resource, fields, marshal_with  # type: ignore
from flask_restful.reqparse import RequestParser  # type: ignore
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus

from dms import db
from dms.models import Author

author_fields = {
    "id": fields.Integer,
    "name": fields.String,
    "uri": fields.Url,
}

authorParser = RequestParser()
authorParser.add_argument("name", required=True)


class AuthorResource(Resource):
    @marshal_with(author_fields)
    def _get_authors(self) -> Sequence[Author]:
        query = select(Author)
        authors = db.session.scalars(query).all()
        return authors

    @marshal_with(author_fields)
    def _get_author(self, id) -> Author:
        return db.get_or_404(Author, id)

    def get(self, id=None):
        if id is None:
            return self._get_authors()
        return self._get_author(id)

    @marshal_with(author_fields)
    def post(self) -> Author:
        args = authorParser.parse_args()
        name = args["name"]
        author = Author(name=name)
        try:
            db.session.add(author)
            db.session.commit()
        except IntegrityError:
            abort(HTTPStatus.BAD_REQUEST, "Unable to create user")
        return author
