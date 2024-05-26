import os.path
from datetime import datetime, timezone
from http import HTTPStatus
from mimetypes import guess_type
from uuid import uuid4

import werkzeug.datastructures
from flask import abort, current_app, send_from_directory
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource, fields, marshal_with  # type: ignore
from flask_restful.reqparse import RequestParser  # type: ignore
from sqlalchemy import Select
from sqlalchemy.exc import IntegrityError
from werkzeug.utils import secure_filename

from dms.models import Document
from dms import db

# FILE_UPLOAD_PATH = r"d:\projects\fitproject\instance\uploads"

document_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'type': fields.String(attribute="mime"),
    'size': fields.Integer(attribute="filesize"),
    "ctime": fields.DateTime(attribute="uploaded"),
    "owner": fields.Nested({
        "id": fields.Integer,
        "name": fields.String,
    }),
    "downloadURL": fields.Url("api.documentdownloadresource"),
}

postParser = RequestParser()
postParser.add_argument(
    'file', location='files', type=werkzeug.datastructures.FileStorage,
    required=True)


class DocumentResource(Resource):
    @marshal_with(document_fields)
    def _get_documents(self):
        query = Select(Document)
        session = db.session
        documents = session.scalars(query).all()
        return documents

    @marshal_with(document_fields)
    def _get_document(self, id):
        return db.get_or_404(Document, id)

    def get(self, id=None):
        if id is None:
            return self._get_documents()
        return self._get_document(id)

    @jwt_required()
    @marshal_with(document_fields)
    def post(self):
        args = postParser.parse_args()
        file = args['file']
        mime = (file.mimetype or guess_type(file.filename)[0]
                or "application/octet-stream")
        filename = secure_filename(file.filename)
        uuid = uuid4()
        uploaded = datetime.now(tz=timezone.utc)
        document = Document(
            filename=str(uuid), name=filename, uploaded=uploaded, mime=mime,
            owner=current_user)
        session = db.session
        try:
            session.add(document)
            file.save(os.path.join(current_app.config["FILE_UPLOAD_PATH"], document.filename))
            document.filesize = file.tell()
            session.commit()
        except (IntegrityError, FileExistsError, FileNotFoundError) as e:
            session.rollback()
            abort(HTTPStatus.INTERNAL_SERVER_ERROR, str(e))
        else:
            return document


class DocumentDownloadResource(Resource):
    def get(self, id):
        document: Document = db.get_or_404(Document, id)
        return send_from_directory(
            current_app.config["FILE_UPLOAD_PATH"], document.filename, mimetype=document.mime,
            download_name=document.name, last_modified=document.uploaded)
