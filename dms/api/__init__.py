from flask import Blueprint
from flask_restful import Api  # type: ignore

from .session import SessionResource
from .user import UserResource
from .document import DocumentResource, DocumentDownloadResource

bp = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(bp)

api.add_resource(UserResource, "/user/<int:id>")
api.add_resource(SessionResource, "/session")
api.add_resource(DocumentResource, "/document", "/document/<int:id>")
api.add_resource(DocumentDownloadResource, "/document/<int:id>/download")
