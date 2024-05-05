from flask_restful import Resource  # type: ignore
from dms.models import Submission, Result
from dms import db
from .submission import ResultSchema
from flask import request
from datetime import datetime
from flask_jwt_extended import jwt_required, current_user


class SubmissionResultResource(Resource):
    def get(self, id=None):
        submission = db.get_or_404(Submission, id)
        return ResultSchema(many=True).dump(submission.results)

    @jwt_required()
    def post(self, id):
        submission: Submission = db.get_or_404(Submission, id)
        results = ResultSchema(many=True).load(request.json)
        marker = current_user
        marked = datetime.now()
        for result in results:
            submission.results.append(
                Result(
                    criterion_id=result["criterion_id"],
                    value=result["value"],
                    marker=marker,
                    marked=marked
                )
            )
        db.session.commit()
        return ResultSchema(many=True).dump(submission.results)
