from datetime import datetime
from http import HTTPStatus

from flask import abort, request
from flask_jwt_extended import current_user, jwt_required
from flask_restful import Resource  # type: ignore
from marshmallow import Schema, fields
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from dms import db
from dms.models import Assessment, Criterion


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class DocumentSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class CriterionSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    min = fields.Integer(required=True)
    max = fields.Integer(required=True)


class AssessmentSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    ctime = fields.DateTime(attribute="created", dump_only=True)
    rubric = fields.Nested(DocumentSchema, dump_only=True)
    rubric_id = fields.Integer(data_key="rubric", load_only=True)
    criteria = fields.List(fields.Nested(CriterionSchema), required=True)
    owner = fields.Nested(UserSchema, dump_only=True)
    minMarks = fields.Int(dump_only=True)
    maxMarks = fields.Int(dump_only=True)


class AssessmentResource(Resource):
    def _get_assessment(self, id):
        return AssessmentSchema().dump(db.get_or_404(Assessment, id))

    def _get_assessments(self):
        query = select(Assessment)
        assessments = db.session.scalars(query)
        return AssessmentSchema(exclude=["criteria"], many=True).dump(
            assessments)

    def get(self, id=None):
        if id is None:
            return self._get_assessments()
        return self._get_assessment(id)

    @jwt_required()
    def post(self) -> Assessment:
        assessmentParser = AssessmentSchema()
        args = assessmentParser.load(request.get_json())
        name = args["name"]
        rubric_id = args["rubric_id"]
        criteria = []
        for criterion in args["criteria"]:
            try:
                criteria.append(Criterion(**criterion))
            except ValueError as e:
                abort(HTTPStatus.UNPROCESSABLE_ENTITY,
                      {criterion["name"], str(e)})
        assessment = Assessment(
            name=name, rubric_id=rubric_id, created=datetime.now(),
            criteria=list(criteria), owner_id=current_user.id)
        dbsession = db.session
        try:
            dbsession.add(assessment)
            dbsession.commit()
        except IntegrityError:
            dbsession.rollback()
            abort(HTTPStatus.BAD_REQUEST, {"msg": "Unable to add assessment"})
        return AssessmentSchema().dump(assessment), HTTPStatus.CREATED
