from typing import List

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from plugins.config import DatabaseConfig
from plugins.log import Logger
from plugins.storage.sql.model import Base


class PostgresDatabase:
    """
        Represents a wrapper for a Postgres Database
    """
    def __init__(self, config: DatabaseConfig):
        self._config = config
        self._logger = Logger.create(f'{__name__}.{self.__class__.__name__}')
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
            echo=True,
        )

        DBSession = sessionmaker(bind=self._engine)
        self._session: Session = DBSession()

        self._logger.info(f'connected to database', engine=self._engine.__str__())

    def create_tables(self):
        Base.metadata.drop_all(bind=self._engine)
        Base.metadata.create_all(bind=self._engine)
        self._logger.info('created tables')

    def create(self, *items):
        for item in items:
            self._session.add(item)
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


def get_postgres_database(config: DatabaseConfig) -> PostgresDatabase:
    return PostgresDatabase(config)
