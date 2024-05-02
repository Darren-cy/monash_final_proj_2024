from flask_restful import Resource  # type: ignore


class SubmissionResource(Resource):
    def get(self, id=None):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError


class AssessmentSubmissionResource(Resource):
    def get(self, id):
        raise NotImplementedError

    def post(self, id):
        raise NotImplementedError
