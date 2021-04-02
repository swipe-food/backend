from __future__ import annotations

from common.exceptions import InvalidValueException
from crawler_context.domain.model.recipe_aggregate import Recipe
from crawler_context.domain.repositories.recipe import AbstractRecipeRepository
from infrastructure.log import Logger
from infrastructure.storage.sql.model import DBRecipe
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_update_data_exception, catch_add_data_exception, catch_delete_data_exception


def create_recipe_repository(database: PostgresDatabase) -> RecipeRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(RecipeRepository, 'database must be a PostgresDatabase')
    return RecipeRepository(database=database)


class RecipeRepository(AbstractRecipeRepository):

    def __init__(self, database: PostgresDatabase):
        self._db = database
        self._logger = Logger.create(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

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
            DBRecipe.vendor_id: entity.vendor_id,
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
