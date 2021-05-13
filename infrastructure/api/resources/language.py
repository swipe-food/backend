from flask import request

from domain.services.language import AbstractLanguageService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import LanguageSchema


class LanguageResource(BaseResource):
    path = '/<string:language_id>'

    @staticmethod
    @dump_schema(schema=LanguageSchema())
    def get(language_id):
        svc: AbstractLanguageService = request.services['language']

        return svc.get_by_id(language_id)


class LanguagesResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=LanguageSchema(many=True))
    def get():
        svc: AbstractLanguageService = request.services['language']
        limit = request.args.get("limit")

        return svc.get_all(limit)
