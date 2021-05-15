from __future__ import annotations

from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.repositories.recipe import AbstractRecipeRepository
from infrastructure.storage.sql.model import DBRecipe, DBUser
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_no_result_found_exception, \
    catch_add_data_exception, catch_update_data_exception, catch_delete_data_exception
from infrastructure.storage.sql.repositories.user import UserRepository


def create_recipe_repository(database: PostgresDatabase, create_logger: Callable) -> RecipeRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(RecipeRepository, 'database must be a PostgresDatabase')
    return RecipeRepository(database=database, create_logger=create_logger)


class RecipeRepository(AbstractRecipeRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_no_result_found_exception
    def get_by_name(self, recipe_name: str) -> Recipe:
        db_recipe: DBRecipe = self._db.session.query(DBRecipe).filter(DBRecipe.name == recipe_name).one()
        recipe = db_recipe.to_entity()
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
        self._logger.debug("get all matched users for recipe", recipe_id=recipe.id.__str__(),
                           count_matched_users=len(users))
        return users

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> Recipe:
        db_recipe: DBRecipe = self._db.session.query(DBRecipe).filter(DBRecipe.id == entity_id).one()
        recipe = db_recipe.to_entity()
        self._logger.debug("get recipe by id", recipe_id=recipe.id.__str__())
        return recipe

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[Recipe]:
        db_recipes: List[DBRecipe] = self._db.session.query(DBRecipe).limit(limit).all()
        self._logger.debug("get all recipes", limit=limit, count=len(db_recipes))
        return [db_recipe.to_entity() for db_recipe in db_recipes]

    @catch_no_result_found_exception
    def get_unseen_recipes_for_user(self, user: User, limit: int = 20) -> List[Recipe]:
        recipes_ids: List[UUID] = [recipe.id for recipe in user.seen_recipes]
        db_recipes: List[DBRecipe] = self._db.session.query(DBRecipe).filter(DBRecipe.id.notin_(recipes_ids)).limit(
            limit).all()
        recipes: List[Recipe] = []
        for db_recipe in db_recipes:
            recipe = db_recipe.to_entity()
            recipes.append(recipe)
        self._logger.debug("get unseen recipes for user", limit=limit, user_id=user.id.__str__(),
                           count_recipes=len(recipes))
        return recipes

    @catch_add_data_exception
    def add(self, entity: Recipe):
        self._db.add(DBRecipe.from_entity(entity))
        self._logger.debug("added recipe to database", recipe_id=entity.id.__str__())

    @catch_update_data_exception
    def update(self, entity: Recipe):
        self._db.update(table=DBRecipe, filters=(DBRecipe.id == entity.id,), data={
            DBRecipe.name: entity.name,
            DBRecipe.description: entity.description,
            DBRecipe.author: entity.author.name,
            DBRecipe.vendor_id: entity.vendor.id,
            DBRecipe.prep_time: entity.prep_time,
            DBRecipe.cook_time: entity.cook_time,
            DBRecipe.total_time: entity.total_time,
            DBRecipe.url: entity.url.__str__(),
            DBRecipe.image: entity.image.__str__(),
        })
        self._logger.debug("updated recipe", recipe_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: Recipe):
        self._db.delete(table=DBRecipe, filters=(DBRecipe.id == entity.id,))
        self._logger.debug("deleted recipe", recipe_id=entity.id.__str__())
