from decorator import decorator
from marshmallow import Schema

from domain.exceptions import ProgrammingError


@decorator
def dump_schema(f, schema: Schema = None, *args, **kwargs):
    if schema is None:
        raise ProgrammingError("No Schema specified")
    elif not isinstance(schema, Schema):
        raise ProgrammingError("schema must be of type marshmallow.Schema")
    func_response = f(*args, **kwargs)
    if isinstance(func_response, tuple):
        return schema.dump(func_response[0]), func_response[1]
    return schema.dump(func_response)
