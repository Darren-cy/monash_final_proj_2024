from flask import Blueprint
from flask_restful import Api  # type: ignore


from .user import UserResource
from .document import DocumentResource, DocumentDownloadResource
from .author import AuthorResource
from .assessment import AssessmentResource
from .submission import SubmissionResource, AssessmentSubmissionResource
from .result import SubmissionResultResource


bp = Blueprint('api', __name__, url_prefix='/api/v1.0')
api = Api(bp)

api.add_resource(UserResource, "/user/<int:id>")
# api.add_resource(SessionResource, "/session")
api.add_resource(DocumentResource, "/document", "/document/<int:id>")
api.add_resource(DocumentDownloadResource, "/document/<int:id>/download")
api.add_resource(AuthorResource, "/person", "/person/<int:id>")
api.add_resource(AssessmentResource, "/assessment", "/assessment/<int:id>")
api.add_resource(SubmissionResource, "/submission", "/submission/<int:id>")
api.add_resource(AssessmentSubmissionResource,
                 "/assessment/<int:id>/submission")

api.add_resource(SubmissionResultResource, "/submission/<int:id>/mark")
