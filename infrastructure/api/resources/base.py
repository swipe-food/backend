from __future__ import absolute_import

from flask_restplus import Resource


class BaseResource(Resource):
    path: str
