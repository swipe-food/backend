from __future__ import annotations

from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.repositories.category import AbstractCategoryRepository
from infrastructure.storage.sql.model import DBCategory, DBUser, DBCategoryLike, DBRecipe
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_delete_data_exception, catch_update_data_exception, \
    catch_no_result_found_exception, catch_add_data_exception
from infrastructure.storage.sql.repositories.user import UserRepository


def create_category_repository(database: PostgresDatabase, create_logger: Callable) -> CategoryRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(CategoryRepository, 'database must be a PostgresDatabase')
    return CategoryRepository(database=database, create_logger=create_logger)


class CategoryRepository(AbstractCategoryRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_add_data_exception
    def add(self, entity: Category):
        self._db.add(DBCategory.from_entity(entity))
        self._logger.debug("added category to database", category_id=entity.id.__str__())

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> Category:
        db_category: DBCategory = self._db.session.query(DBCategory).filter(DBCategory.id == entity_id).one()
        self._logger.debug("get category by id", category_id=db_category.id.__str__())
        return db_category.to_entity()

    @catch_no_result_found_exception
    def get_by_name(self, category_name: str) -> Category:
        db_category: DBCategory = self._db.session.query(DBCategory).filter(DBCategory.name == category_name).one()
        self._logger.debug("get category by name", category_id=db_category.id.__str__(), category_name=category_name)
        return db_category.to_entity()

    @catch_no_result_found_exception
    def get_liked_users(self, category: Category) -> List[User]:
        db_users: List[DBUser] = self._db.session.query(DBUser).join(DBCategoryLike).join(DBCategory).filter(
            DBCategory.id == category.id).all()
        users: List[User] = []
        for db_user in db_users:
            user = db_user.to_entity()
            UserRepository.load_relationship_for_user(db_user, user)
            users.append(user)
        self._logger.debug("get all liked users for category", category_id=category.id.__str__(),
                           count_liked_users=len(users))
        return users

    @catch_no_result_found_exception
    def get_recipes(self, category: Category, limit: int or None) -> List[Recipe]:
        db_recipes: List[DBRecipe] = self._db.session.query(DBRecipe).filter(DBRecipe.fk_category == category.id).limit(
            limit).all()
        self._logger.debug("get all recipes for category", category_id=category.id.__str__(),
                           count_recipes=len(db_recipes))
        return [db_recipe.to_entity() for db_recipe in db_recipes]

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[Category]:
        db_categories: List[DBCategory] = self._db.session.query(DBCategory).limit(limit).all()
        self._logger.debug("get all categories", limit=limit, count=len(db_categories))
        return [db_category.to_entity() for db_category in db_categories]

    @catch_update_data_exception
    def update(self, entity: Category):
        self._db.update(table=DBCategory, filters=(DBCategory.id == entity.id,), data={
            DBCategory.name: entity.name,
            DBCategory.url: entity.url,
            DBCategory.likes: entity.likes,
        })
        self._logger.debug("updated category", category_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: Category):
        self._db.delete(table=DBCategory, filters=(DBCategory.id == entity.id,))
        self._logger.debug("deleted category", category_id=entity.id.__str__())
