from datetime import datetime
from http import HTTPStatus

from flask import abort, request
from flask_restful import Resource  # type: ignore
from marshmallow import Schema, fields
from sqlalchemy import select

from dms import db
from dms.models import Assessment, Author, Document, Submission

from .assessment import (AssessmentSchema, CriterionSchema, DocumentSchema,
                         UserSchema)


class AuthorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class ResultSchema(Schema):
    value = fields.Integer()
    marker = fields.Nested(UserSchema, dump_only=True)
    marked = fields.DateTime(dump_only=True)
    criterion = fields.Nested(CriterionSchema(), dump_only=True)
    criterion_id = fields.Integer(load_only=True, data_key="criterion")


class SubmissionSchema(Schema):
    id = fields.Integer(dump_only=True)
    ctime = fields.DateTime(dump_only=True, attribute="submitted")
    # assessment_id = fields.Integer(load_only=True, data_key="assessment")
    assessment = fields.Nested(AssessmentSchema(
        only=["id", "name", "minMarks", "maxMarks"]), dump_only=True)
    totalMarks = fields.Integer(dump_only=True)
    attachments = fields.Nested(DocumentSchema(many=True), dump_only=True)
    attachment_ids = fields.List(
        fields.Integer(), load_only=True, data_key="attachments")
    authors = fields.Nested(AuthorSchema(many=True), dump_only=True)
    author_ids = fields.List(
        fields.Integer(), load_only=True, data_key="authors")
    results = fields.Nested(
        ResultSchema(many=True, only=["criterion", "value"]), dump_only=True)


submission_schema = SubmissionSchema()
submissions_schema = SubmissionSchema(
    many=True, exclude=["results", "attachments"])


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


class AssessmentSubmissionResource(Resource):
    def get(self, id):
        assessment = db.get_or_404(Assessment, id)
        return submissions_schema.dump(assessment.submissions)

    def post(self, id):
        assessment = db.session.get(Assessment, id)
        if not assessment:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  f"Assessment {id} does not exist.")
        args = submission_schema.load(request.json)
        try:
            authors = get_all(db.session, Author, args["author_ids"])
        except ValueError:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY, "Not all authors exist.")
        try:
            attachments = get_all(db.session, Document, args["attachment_ids"])
        except ValueError:
            abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                  "Not all attachments exist.")
        submission = Submission(
            submitted=datetime.now(),
            assessment=assessment,
            authors=authors,
            attachments=attachments
        )
        db.session.add(submission)
        db.session.commit()
        return submission_schema.dump(submission)


def get_all(session, entity, ids):
    query = select(entity).filter(entity.id.in_(ids))
    entities = session.scalars(query).all()
    if len(entities) != len(ids):
        raise ValueError("Not all IDs exist in database")
    return entities
