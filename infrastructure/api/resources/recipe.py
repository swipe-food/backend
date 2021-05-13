from flask import request

from domain.services.recipe import AbstractRecipeService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import RecipeSchema


class RecipeNameResource(BaseResource):
    path = '/name/<string:recipe_name>'

    @staticmethod
    @dump_schema(schema=RecipeSchema())
    def get(recipe_name):
        svc: AbstractRecipeService = request.services['recipe']

        return svc.get_by_name(recipe_name)


class RecipeResource(BaseResource):
    path = '/<string:recipe_id>'

    @staticmethod
    @dump_schema(schema=RecipeSchema())
    def get(recipe_id):
        svc: AbstractRecipeService = request.services['recipe']

        return svc.get_by_id(recipe_id)


