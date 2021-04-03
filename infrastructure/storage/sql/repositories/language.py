from __future__ import annotations

from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.language_aggregate import Language
from domain.repositories.language import AbstractLanguageRepository
from infrastructure.storage.sql.model import DBLanguage
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_delete_data_exception, catch_update_data_exception, catch_no_result_found_exception, catch_add_data_exception


def create_language_repository(database: PostgresDatabase, create_logger: Callable) -> LanguageRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(LanguageRepository, 'database must be a PostgresDatabase')
    return LanguageRepository(database=database, create_logger=create_logger)


class LanguageRepository(AbstractLanguageRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_add_data_exception
    def add(self, entity: Language):
        self._db.add(DBLanguage.from_entity(entity))
        self._logger.debug("added language to database", language_id=entity.id.__str__())
        
    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> Language:
        db_language: DBLanguage = self._db.session.query(DBLanguage).filter(DBLanguage.id == entity_id).one()
        self._logger.debug("get language by id", language_id=db_language.id.__str__())
        return db_language.to_entity()

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[Language]:
        db_languages: List[DBLanguage] = self._db.session.query(DBLanguage).limit(limit).all()
        self._logger.debug("get all languages", limit=limit, count=len(db_languages))
        return [db_language.to_entity() for db_language in db_languages]

    @catch_update_data_exception
    def update(self, entity: Language):
        self._db.update(table=DBLanguage, filters=(DBLanguage.id == entity.id,), data={
            DBLanguage.name: entity.name,
            DBLanguage.code: entity.code,
        })
        self._logger.debug("updated language", language_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: Language):
        self._db.delete(table=DBLanguage, filters=(DBLanguage.id == entity.id,))
        self._logger.debug("deleted language", language_id=entity.id.__str__())