from flask_restful import abort
from marshmallow import ValidationError

from backend.api.resources import schema


class CommonSerialize:
    def _deserialize_data(
        self, user_schema, json_data, partial=False
    ) -> dict:
        deserialized_data = {}
        try:
            deserialized_data = getattr(
                schema, user_schema
            )().load(json_data, partial=partial)
        except ValidationError as e:
            abort(400, message={'fields': e.messages})

        return deserialized_data

    def _serialize_data(
        self, user_schema, item, many=False
    ):
        serialized_data = getattr(schema, user_schema)().dump(item, many=many)
        return serialized_data
