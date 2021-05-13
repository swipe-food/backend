from flask import request

from domain.services.user import AbstractUserService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import UserSchema, MatchResponseSchema, CategoryLikeSchema, RecipeSchema


class UserResource(BaseResource):
    path = '/<string:user_id>'

    @staticmethod
    @dump_schema(schema=UserSchema())
    def get(user_id):
        svc: AbstractUserService = request.services['user']

        return svc.get_by_id(user_id)

    @staticmethod
    @dump_schema(schema=UserSchema())
    def put(user_id):
        svc: AbstractUserService = request.services['user']
        user_json = request.get_json()
        user_request_schema = UserSchema()
        user_data = user_request_schema.load(user_json)

        return svc.update(user_id, user_data), 200

    @staticmethod
    def delete(user_id):
        svc: AbstractUserService = request.services['user']
        svc.delete(user_id)
        return {'message': 'User successfully deleted'}, 200


class UsersResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=UserSchema(many=True))
    def get():
        svc: AbstractUserService = request.services['user']
        limit = request.args.get("limit")

        return svc.get_all(limit)

    @staticmethod
    @dump_schema(schema=UserSchema())
    def post():
        svc: AbstractUserService = request.services['user']
        user_json = request.get_json()
        user_request_schema = UserSchema()
        user_data = user_request_schema.load(user_json)

        return svc.add(user_data), 201


class UserEMailResource(BaseResource):
    path = '/email/<string:user_email>'

    @staticmethod
    @dump_schema(schema=UserSchema())
    def get(user_email):
        svc: AbstractUserService = request.services['user']

        return svc.get_by_email(user_email)


class UserConfirmResource(BaseResource):
    path = '/<string:user_id>/confirm'

    @staticmethod
    def post(user_id):
        svc: AbstractUserService = request.services['user']
        svc.confirm(user_id)
        return {'message': 'User confirmed'}, 201


class UserAddLanguageResource(BaseResource):
    path = '/<string:user_id>/languages'

    @staticmethod
    def post(user_id):
        svc: AbstractUserService = request.services['user']
        language_json = request.get_json()

        svc.add_language(user_id, language_json["id"])
        return {'message': 'Language added to User'}, 201


class UserRemoveLanguageResource(BaseResource):
    path = '/<string:user_id>/languages/<string:language_id>'

    @staticmethod
    def delete(user_id, language_id):
        svc: AbstractUserService = request.services['user']

        svc.remove_language(user_id, language_id)
        return {'message': 'Language removed'}


class UserMatchesResource(BaseResource):
    path = '/<string:user_id>/matches'

    @staticmethod
    @dump_schema(schema=MatchResponseSchema(many=True))
    def get(user_id):
        svc: AbstractUserService = request.services['user']
        limit = request.args.get("limit")

        return svc.get_matches(user_id, limit)


class UserRecipeResource(BaseResource):
    path = '/<string:user_id>/recipes'

    @staticmethod
    def post(user_id):
        svc: AbstractUserService = request.services['user']
        recipe_json = request.get_json()

        svc.add_seen_recipe(user_id, recipe_json["id"])
        return {'message': 'Recipe as seen marked'}, 201

    @staticmethod
    @dump_schema(schema=RecipeSchema(many=True))
    def get(user_id):
        svc: AbstractUserService = request.services['user']
        limit = request.args.get("limit")

        return svc.get_unseen_recipes(user_id, limit)


class UserCategoryLikeResource(BaseResource):
    path = '/<string:user_id>/liked_categories'

    @staticmethod
    def post(user_id):
        svc: AbstractUserService = request.services['user']
        category_json = request.get_json()

        svc.add_category_like(user_id, category_json["id"])
        return {'message': 'Category liked'}, 201

    @staticmethod
    @dump_schema(schema=CategoryLikeSchema(many=True))
    def get(user_id):
        svc: AbstractUserService = request.services['user']
        limit = request.args.get("limit")

        return svc.get_liked_categories(user_id, limit)


class UserRemoveCategoryLikeResource(BaseResource):
    path = '/<string:user_id>/liked_categories/<string:category_like_id>'

    @staticmethod
    def delete(user_id, category_like_id):
        svc: AbstractUserService = request.services['user']

        svc.remove_category_like(user_id, category_like_id)
        return {'message': 'Category Like removed'}
