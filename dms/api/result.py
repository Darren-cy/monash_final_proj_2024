from flask_restful import Resource  # type: ignore


class SubmissionResultResource(Resource):
    def get(self, id=None):
        raise NotImplementedError

    def post(self):
        raise NotImplementedError
