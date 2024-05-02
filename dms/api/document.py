import os.path
from datetime import datetime, timezone
from uuid import uuid4
from flask_restful import Resource, fields, marshal_with  # type: ignore
from flask_restful.reqparse import RequestParser  # type: ignore
from dms.models import Document
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from flask import current_app, abort
import werkzeug.datastructures
from mimetypes import guess_type
from werkzeug.utils import secure_filename
from http import HTTPStatus
from flask_jwt_extended import jwt_required, current_user

FILE_UPLOAD_PATH = r"d:\projects\fitproject\instance\uploads"

document_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String(attribute="mime"),
    "ctime": fields.DateTime(attribute="uploaded")
}

parser = RequestParser()
parser.add_argument(
    'file', location='files', type=werkzeug.datastructures.FileStorage,
    required=True)


class DocumentResource(Resource):
    @marshal_with(document_fields)
    def _get_documents(self):
        query = Select(Document)
        session = current_app.db.session
        documents = session.scalars(query).all()
        return documents

    @marshal_with(document_fields)
    def _get_document(self, id):
        return current_app.db.get_or_404(Document, id)

    def get(self, id=None):
        if id is None:
            return self._get_documents()
        return self._get_document(id)

    @jwt_required()
    @marshal_with(document_fields)
    def post(self):
        args = parser.parse_args()
        file = args['file']
        print(file.mimetype)
        print(guess_type(file.filename))
        mime = (file.mimetype or guess_type(file.filename)[0]
                or "application/octet-stream")
        filename = secure_filename(file.filename)
        uuid = uuid4()
        uploaded = datetime.now(tz=timezone.utc)
        document = Document(
            filename=str(uuid), name=filename, uploaded=uploaded, mime=mime,
            owner=current_user)
        session = current_app.db.session
        try:
            session.add(document)
            file.save(os.path.join(FILE_UPLOAD_PATH, document.filename))
            session.commit()
        except (IntegrityError, FileExistsError, FileNotFoundError) as e:
            session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        else:
            return document
