from __future__ import annotations

from typing import List
from uuid import UUID

from common.exceptions import InvalidValueException
from infrastructure.log import Logger
from infrastructure.storage.sql.model import DBRecipe, DBUser
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_no_result_found_exception
from infrastructure.storage.sql.repositories.user_context.user import UserRepository
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate import User
from user_context.domain.repositories.recipe import AbstractRecipeRepository


def create_recipe_repository(database: PostgresDatabase) -> RecipeRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(RecipeRepository, 'database must be a PostgresDatabase')
    return RecipeRepository(database=database)


class RecipeRepository(AbstractRecipeRepository):

    def __init__(self, database: PostgresDatabase):
        self._db = database
        self._logger = Logger.create(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_no_result_found_exception
    def get_by_name(self, recipe_name: str) -> Recipe:
        db_recipe: DBRecipe = self._db.session.query(DBRecipe).filter(DBRecipe.name == recipe_name).one()
        recipe = db_recipe.to_user_context_entity()
        self._logger.debug("get recipe by name", recipe_id=recipe.id.__str__(), recipe_name=recipe_name)
        return recipe

    @catch_no_result_found_exception
    def get_matched_users(self, recipe: Recipe) -> List[User]:
        db_users: List[DBUser] = self._db.session.query(DBUser).filter().all()
        users: List[User] = []
        for db_user in db_users:
            user = db_user.to_entity()
            UserRepository.load_relationship_for_user(db_user, user)
            users.append(user)
        self._logger.debug("get all matched users for recipe", recipe_id=recipe.id.__str__(), count_matched_users=len(users))
        return users

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> Recipe:
        db_recipe: DBRecipe = self._db.session.query(DBRecipe).filter(DBRecipe.id == entity_id).one()
        recipe = db_recipe.to_user_context_entity()
        self._logger.debug("get recipe by id", recipe_id=recipe.id.__str__())
        return recipe

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[Recipe]:
        db_recipes: List[DBRecipe] = self._db.session.query(DBRecipe).limit(limit).all()
        recipes: List[Recipe] = []
        for db_recipe in db_recipes:
            recipe = db_recipe.to_user_context_entity()
            recipes.append(recipe)
        self._logger.debug("get all recipes", limit=limit, count=len(recipes))
        return recipes

    @catch_no_result_found_exception
    def get_unseen_recipes_for_user(self, user: User, limit: int = 20) -> List[Recipe]:
        recipes_ids: List[UUID] = [recipe.id for recipe in user.seen_recipes]
        db_recipes: List[DBRecipe] = self._db.session.query(DBRecipe).filter(DBRecipe.id.notin_(recipes_ids)).limit(limit).all()
        recipes: List[Recipe] = []
        for db_recipe in db_recipes:
            recipe = db_recipe.to_user_context_entity()
            recipes.append(recipe)
        self._logger.debug("get unseen recipes for user", limit=limit, user_id=user.id.__str__(), count=len(recipes))
        return recipes
