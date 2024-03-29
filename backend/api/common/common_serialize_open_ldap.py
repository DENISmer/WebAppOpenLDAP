import pprint

from flask_restful import abort
from marshmallow import ValidationError

from backend.api.resources import schema


class CommonSerializer:
    def deserialize_data(
        self, user_schema, data, partial=False
    ) -> dict:
        deserialized_data = {}
        try:
            deserialized_data = getattr(
                schema, user_schema
            )().load(data, partial=partial)
        except ValidationError as e:
            abort(
                400,
                message='Invalid attributes',
                fields=e.messages,
                status=400
            )

        return deserialized_data

    def serialize_data(
        self, user_schema, item, many=False
    ):
        serialized_data = getattr(schema, user_schema)().dump(item, many=many)
        return serialized_data
