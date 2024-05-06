from flask_restful import Resource  # type: ignore
from dms.models import Submission, Result
from dms import db
from .submission import ResultSchema, AssessmentSchema
from flask import request
from datetime import datetime
from flask_jwt_extended import jwt_required, current_user
from marshmallow import Schema, fields


class MarksSchema(Schema):
    assessment = fields.Nested(AssessmentSchema, dump_only=True, only=["name", "id", "minMarks", "maxMarks"])
    results = fields.Nested(ResultSchema, many=True, required=True)
    feedback = fields.String()


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
                    comment = result["comment"],
                    marker=marker,
                    marked=marked
                )
            )
        if "feedback" in marks:
            submission.feedback = marks["feedback"]
        db.session.commit()
        return MarksSchema().dump(submission)