from marshmallow import fields


class CustomStringField(fields.Field):
    """This custom marshmallow field serializes and deserializes a object.

     It is e.g. used to serialize/deserialize a domain.model.base.Immutable object.
     """

    def _deserialize(self, value, *args, **kwargs):
        return value

    def _serialize(self, value, *args, **kwargs):
        return str(value)
