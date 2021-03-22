from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from plugins.config import DatabaseConfig
from plugins.log import Logger


class PostgresDatabase:

    def __init__(self, config: DatabaseConfig):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        self._config = config
        self._logger = Logger.create(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')
        self._session = None
        self._meta = None

        self.connect()

    def connect(self):
        """connects to the postgres database by setting the session and meta variable"""
        dsn: str = self._config.get_dsn()

        engine: Engine = create_engine(
            url=dsn,
            pool_size=self._config.max_open_connections,
            max_overflow=self._config.max_idle_connections,
            pool_pre_ping=True
        )

        DBSession = sessionmaker(bind=engine)
        self._session: Session = DBSession()

        self._meta = MetaData(bind=engine)
        self._logger.info(f'connected to database', meta=self._meta.__str__())

    @property
    def session(self) -> Session:
        return self._session

    @property
    def meta(self) -> MetaData:
        return self._meta

    def __str__(self):
        return ''


def get_postgres_database(config: DatabaseConfig) -> PostgresDatabase:
    return PostgresDatabase(config)
