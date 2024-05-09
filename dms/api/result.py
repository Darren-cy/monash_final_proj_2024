from flask import request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource  # type: ignore
from datetime import datetime
from dms import db
from dms.models import Result, Submission
from .schemas import MarksSchema


class SubmissionResultResource(Resource):
    def get(self, id=None):
        submission = db.get_or_404(Submission, id)
        return MarksSchema().dump(submission)

    @jwt_required()
    def post(self, id):
        submission: Submission = db.get_or_404(Submission, id)
        marks = MarksSchema().load(request.json)
        marker = current_user
        marked = datetime.now()
        for result in marks["results"]:
            submission.results.append(
                Result(
                    criterion_id=result["criterion_id"],
                    value=result["value"],
                    comment=result["comment"],
                    marker=marker,
                    marked=marked
                )
            )
        if "feedback" in marks:
            submission.feedback = marks["feedback"]
        db.session.commit()
        return MarksSchema().dump(submission)
