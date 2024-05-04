from flask_restful import Resource  # type: ignore
from marshmallow import Schema, fields
from sqlalchemy import select

from dms import db
from dms.models import Submission

from .assessment import (AssessmentSchema, CriterionSchema, DocumentSchema,
                         UserSchema)


class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class ResultSchema(Schema):
    value = fields.Integer()
    marker = fields.Nested(UserSchema, dump_only=True)
    marked = fields.DateTime(dump_only=True)
    criterion = fields.Nested(CriterionSchema(only=["name", "min", "max"]))


class SubmissionSchema(Schema):
    id = fields.Integer(dump_only=True)
    ctime = fields.DateTime(dump_only=True, attribute="submitted")
    assessment_id = fields.Integer(load_only=True, data_key="assessment")
    assessment = fields.Nested(AssessmentSchema(
        only=["id", "name", "minMarks", "maxMarks"]))
    totalMarks = fields.Integer(dump_only=True)
    attachments = fields.Nested(DocumentSchema(many=True))
    authors = fields.Nested(AuthorSchema(many=True))
    results = fields.Nested(ResultSchema(many=True, only=["criterion", "value"]))


submission_schema = SubmissionSchema()
submissions_schema = SubmissionSchema(many=True)


class SubmissionResource(Resource):
    def _get_submission(self, id):
        return submission_schema.dump(db.get_or_404(Submission, id))

    def _get_submissions(self):
        query = select(Submission)
        submissions = db.session.scalars(query)
        return submissions_schema.dump(submissions)

    def get(self, id=None):
        if id is None:
            return self._get_submissions()
        return self._get_submission(id)

    def post(self):
        raise NotImplementedError


class AssessmentSubmissionResource(Resource):
    def get(self, id):
        raise NotImplementedError

    def post(self, id):
        raise NotImplementedError
