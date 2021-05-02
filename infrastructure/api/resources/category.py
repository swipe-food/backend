from flask import request

from domain.services.category import AbstractCategoryService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import category_schema, category_list_schema, recipe_list_schema, user_list_schema


class CategoryNameResource(BaseResource):
    path = '/name/<string:category_name>'

    @staticmethod
    @dump_schema(schema=category_schema)
    def get(category_name):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_by_name(category_name)


class CategoryResource(BaseResource):
    path = '/<string:category_id>'

    @staticmethod
    @dump_schema(schema=category_schema)
    def get(category_id):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_by_id(category_id)


class CategoryRecipesResource(BaseResource):
    path = '/<string:category_id>/recipes'

    @staticmethod
    @dump_schema(schema=recipe_list_schema)
    def get(category_id):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_recipes(category_id)


class CategoryUsersResource(BaseResource):
    path = '/<string:category_id>/users'

    @staticmethod
    @dump_schema(schema=user_list_schema)
    def get(category_id):
        svc: AbstractCategoryService = request.services['category']

        return svc.get_liked_users(category_id)


class CategoriesResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=category_list_schema)
    def get():
        svc: AbstractCategoryService = request.services['category']
        limit = request.args.get("limit")

        return svc.get_all(limit)
