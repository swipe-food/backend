from __future__ import annotations

from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from domain.exceptions import MissingArgumentException, InvalidValueException
from infrastructure.config import DatabaseConfig
from infrastructure.storage.sql.model import Base


def create_postgres_database(config: DatabaseConfig, create_logger: Callable) -> PostgresDatabase:
    if not isinstance(config, DatabaseConfig):
        raise InvalidValueException(DatabaseConfig, 'config must be a DatabaseConfig')
    return PostgresDatabase(config=config, create_logger=create_logger)


class PostgresDatabase:
    """
        Represents a wrapper for a Postgres Database
    """

    def __init__(self, config: DatabaseConfig, create_logger: Callable):
        self._config = config
        self._logger = create_logger(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')
        self._engine = None
        self._session = None

        self.connect()
        self.create_tables()

    def connect(self):
        """connect to the postgres database via the dsn"""
        dsn: str = self._config.get_dsn()

        self._engine: Engine = create_engine(
            url=dsn,
            pool_size=self._config.max_open_connections,
            max_overflow=self._config.max_idle_connections,
            pool_pre_ping=True,
            echo=self._config.logging_enabled,
        )

        DBSession = sessionmaker(bind=self._engine)
        self._session: Session = DBSession()

        self._logger.info(f'connected to database', engine=self._engine.__str__())

    def create_tables(self):
        Base.metadata.create_all(bind=self._engine)
        self._logger.info('created tables')

    def add(self, *items: Base):
        """Adds one or multiple items to the database"""
        for item in items:
            self._session.add(item)
        self._session.commit()

    def update(self, table: Base, filters: tuple, data: dict):
        """Updates a row in the database
        :param table: class of the table that should get altered
        :param filters: list of comparisons, which are the filters for the query ([User.id == user_id] for instance)
        :param data: dict with the column names as keys and the values as the new data, doesn't have to contain all columns
        """
        if not filters or not data:
            raise MissingArgumentException(f'either param filters ({filters}) or param data ({data}) is empty!')
        self._session.query(table).filter(*filters).update(data, synchronize_session='evaluate')
        self._session.commit()

    def delete(self, table: Base, filters: tuple):
        """Deletes rows from the database
        :param table: class of the table that should get altered
        :param filters: list of comparisons, which are the filters for the query ([User.id == user_id] for instance)
        """
        if not filters:
            raise MissingArgumentException(f'param filters ({filters}) is empty!')
        self._session.query(table).filter(*filters).delete(synchronize_session='fetch')
        self._session.commit()

    @property
    def session(self) -> Session:
        return self._session

    @property
    def engine(self) -> Engine:
        return self._engine

    def __repr__(self):
        return '{c}(engine={engine}, session={session})'.format(
            c=self.__class__.__name__,
            engine=self._engine.__repr__(),
            session=self._session.__repr__()
        )
