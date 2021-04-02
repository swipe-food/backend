from __future__ import annotations

from typing import List, Callable
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.match_aggregate import Match
from domain.repositories.match import AbstractMatchRepository
from infrastructure.storage.sql.model import DBMatch
from infrastructure.storage.sql.postgres import PostgresDatabase
from infrastructure.storage.sql.repositories.decorators import catch_delete_data_exception, catch_update_data_exception, catch_no_result_found_exception, catch_add_data_exception


def create_match_repository(database: PostgresDatabase, create_logger: Callable) -> MatchRepository:
    if not isinstance(database, PostgresDatabase):
        raise InvalidValueException(MatchRepository, 'database must be a PostgresDatabase')
    return MatchRepository(database=database, create_logger=create_logger)


class MatchRepository(AbstractMatchRepository):

    def __init__(self, database: PostgresDatabase, create_logger: Callable):
        self._db = database
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')

    @catch_add_data_exception
    def add(self, entity: Match):
        self._db.add(DBMatch.from_entity(entity))
        self._logger.debug("added match to database", match_id=entity.id.__str__())

    @catch_no_result_found_exception
    def get_by_id(self, entity_id: UUID) -> Match:
        db_match: DBMatch = self._db.session.query(DBMatch).filter(DBMatch.id == entity_id).one()
        self._logger.debug("get match by id", match_id=db_match.id.__str__())
        return db_match.to_entity()

    @catch_no_result_found_exception
    def get_all(self, limit: int = None) -> List[Match]:
        db_matches: List[DBMatch] = self._db.session.query(DBMatch).limit(limit).all()
        self._logger.debug("get all matches", limit=limit, count=len(db_matches))
        return [db_match.to_entity() for db_match in db_matches]

    @catch_update_data_exception
    def update(self, entity: Match):
        self._db.update(table=DBMatch, filters=(DBMatch.id == entity.id,), data={
            DBMatch.is_active: entity.is_active,
            DBMatch.is_seen_by_user: entity.is_seen_by_user,
        })
        self._logger.debug("updated match", match_id=entity.id.__str__())

    @catch_delete_data_exception
    def delete(self, entity: Match):
        self._db.delete(table=DBMatch, filters=(DBMatch.id == entity.id,))
        self._logger.debug("deleted match", match_id=entity.id.__str__())
