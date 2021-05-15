from flask import request

from domain.services.match import AbstractMatchService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import MatchResponseSchema, MatchRequestSchema

match_request_schema = MatchRequestSchema()


class MatchResource(BaseResource):
    path = '/<string:match_id>'

    @staticmethod
    @dump_schema(schema=MatchResponseSchema())
    def get(match_id):
        svc: AbstractMatchService = request.services['match']

        return svc.get_by_id(match_id)

    @staticmethod
    @dump_schema(schema=MatchResponseSchema())
    def put(match_id):
        svc: AbstractMatchService = request.services['match']
        match_json = request.get_json()

        match_data = match_request_schema.load(match_json)

        return svc.update(match_id, match_data), 200

    @staticmethod
    def delete(match_id):
        svc: AbstractMatchService = request.services['match']
        svc.delete(match_id)
        return {'message': 'Match successfully deleted'}, 200


class MatchesResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=MatchResponseSchema())
    def post():
        svc: AbstractMatchService = request.services['match']
        match_json = request.get_json()
        match_data = match_request_schema.load(match_json)

        return svc.add(match_data), 201
