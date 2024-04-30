from flask_restful import Resource, fields, marshal_with  # type: ignore
from dms.models import Document
from sqlalchemy import Select
from flask import current_app


document_fields = {
    'id': fields.String,
    'name': fields.String,
    'type': fields.String(attribute="mime"),
    "ctime": fields.DateTime(attribute="uploaded")
}

documents_fields = {
    "documents": fields.List(fields.Nested(document_fields))
}


class DocumentResource(Resource):
    @marshal_with(document_fields, envelope="documents")
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
