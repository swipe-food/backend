from flask import request

from domain.services.category import AbstractCategoryService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import CategorySchema, RecipeSchema, UserSchema


class CategoryNameResource(BaseResource):
    path = '/name/<string:category_name>'

    @staticmethod
    @dump_schema(schema=CategorySchema())
    def get(category_name):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_by_name(category_name)


class CategoryResource(BaseResource):
    path = '/<string:category_id>'

    @staticmethod
    @dump_schema(schema=CategorySchema())
    def get(category_id):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_by_id(category_id)


class CategoryRecipesResource(BaseResource):
    path = '/<string:category_id>/recipes'

    @staticmethod
    @dump_schema(schema=RecipeSchema(many=True))
    def get(category_id):
        svc: AbstractCategoryService = request.services['category']
        limit = request.args.get("limit")

        return svc.get_recipes(category_id, limit)


class CategoryUsersResource(BaseResource):
    path = '/<string:category_id>/users'

    @staticmethod
    @dump_schema(schema=UserSchema(many=True))
    def get(category_id):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_liked_users(category_id)


class CategoriesResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=CategorySchema(many=True))
    def get():
        svc: AbstractCategoryService = request.services['category']
        limit = request.args.get("limit")

        return svc.get_all(limit)
