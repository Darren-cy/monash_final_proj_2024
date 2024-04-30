from flask_restful import Resource  # type: ignore


class DocumentResource(Resource):
    def get(self, id=None):
        if id is None:
            return {"msg": "List of documents"}
        return {"msg": f'Document {id}'}
