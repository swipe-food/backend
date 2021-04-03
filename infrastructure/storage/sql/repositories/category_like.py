from __future__ import annotations

from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.category_like_aggregate import CategoryLike
from domain.repositories.category_like import AbstractCategoryLikeRepository
from infrastructure.storage.sql.model import DBCategoryLike
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_delete_data_exception, catch_update_data_exception, catch_no_result_found_exception, catch_add_data_exception


def create_category_like_repository(database: PostgresDatabase, create_logger: Callable) -> CategoryLikeRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(CategoryLikeRepository, 'database must be a PostgresDatabase')
    return CategoryLikeRepository(database=database, create_logger=create_logger)


class CategoryLikeRepository(AbstractCategoryLikeRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_add_data_exception
    def add(self, entity: CategoryLike):
        self._db.add(DBCategoryLike.from_entity(entity))
        self._logger.debug("added category like to database", category_like_id=entity.id.__str__())

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> CategoryLike:
        db_category_like: DBCategoryLike = self._db.session.query(DBCategoryLike).filter(DBCategoryLike.id == entity_id).one()
        self._logger.debug("get category like by id", category_like_id=db_category_like.id.__str__())
        return db_category_like.to_entity()

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[CategoryLike]:
        db_category_likes: List[DBCategoryLike] = self._db.session.query(DBCategoryLike).limit(limit).all()
        self._logger.debug("get all category likes", limit=limit, count=len(db_category_likes))
        return [db_category_like.to_entity() for db_category_like in db_category_likes]

    @catch_update_data_exception
    def update(self, entity: CategoryLike):
        self._db.update(table=DBCategoryLike, filters=(DBCategoryLike.id == entity.id,), data={
            DBCategoryLike.matches: entity.matches,
            DBCategoryLike.views: entity.views,
        })
        self._logger.debug("updated category like", category_like_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: CategoryLike):
        self._db.delete(table=DBCategoryLike, filters=(DBCategoryLike.id == entity.id,))
        self._logger.debug("deleted category like", category_like_id=entity.id.__str__())
