from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, registry, relationship
from sqlalchemy.orm.session import Session

from domain.model.category_aggregate.entities import Category
from domain.model.common_aggregate import Language, Entity
from domain.model.match_aggregate.entities import Match
from domain.model.recipe_aggregate.entities import ImageURL, Ingredient, Recipe
from domain.model.user_aggregate import User, CategoryLike
from domain.model.vendor_aggregate.entities import Vendor
from plugins.config import DatabaseConfig
from plugins.log import Logger
from plugins.storage.sql.mappings import SQLAlchemyMappings, create_sql_mappings


class PostgresDatabase:

    def __init__(self, config: DatabaseConfig):
        """ creates a singleton object, if it is not created,
        or else returns the previous singleton object"""
        self._config = config
        self._logger = Logger.create(f'{__name__}.{self.__class__.__name__}')
        self._logger.info(f'created new {self.__class__.__name__}')
        self._session = None
        self._metadata = None
        self._mapper_registry = None

        self.connect()
        self.init_mappings()

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

        self._metadata = MetaData(bind=engine)
        self._mapper_registry = registry(metadata=self._metadata)
        self._logger.info(f'connected to database', meta=self._metadata.__str__())

    def init_mappings(self):
        mappings: SQLAlchemyMappings = create_sql_mappings(self._metadata)

        self._mapper_registry.map_imperatively(Language, mappings.get_language_mapping())
        self._mapper_registry.map_imperatively(ImageURL, mappings.get_image_url_mapping())
        self._mapper_registry.map_imperatively(Ingredient, mappings.get_ingredient_mapping())
        self._mapper_registry.map_imperatively(Recipe, mappings.get_recipe_mapping(), properties={
            'images': relationship(ImageURL, cascade="all, delete-orphan"),
            'ingredients': relationship(Ingredient, cascade="all, delete-orphan"),
            'category': relationship(Category),
            'vendor': relationship(Vendor),
            'language': relationship(Language),
            'matches': relationship(Match, back_populates='recipe'),
        })

        vendor_languages_association_table = mappings.get_association_table('vendor_languages', 'vendor', 'language')
        self._mapper_registry.map_imperatively(Vendor, mappings.get_vendor_mapping(), properties={
            'language': relationship(Language, secondary=vendor_languages_association_table),
            'categories': relationship(Category, back_populates='vendor'),
        })

        self._mapper_registry.map_imperatively(Category, mappings.get_category_mapping(), properties={
            'vendor': relationship(Vendor, back_populates="categories"),
            'likes': relationship(CategoryLike, back_populates='category'),
            'recipes': relationship(Recipe, back_populates='category'),
        })

        user_languages_association_table = mappings.get_association_table('user_languages', 'user', 'language')
        seen_recipes_association_table = mappings.get_association_table('user_seen_recipes', 'user', 'recipe')
        self._mapper_registry.map_imperatively(User, mappings.get_user_mapping(), properties={
            'language': relationship(Language, secondary=user_languages_association_table),
            'likes': relationship(CategoryLike, back_populates='user', cascade="all, delete-orphan"),
            'matches': relationship(Match, back_populates='user', cascade="all, delete-orphan"),
            'seen_recipes': relationship(Recipe, secondary=seen_recipes_association_table)
        })

        self._mapper_registry.map_imperatively(CategoryLike, mappings.get_category_like_mapping(), properties={
            'user': relationship(User, back_populates='likes'),
            'category': relationship(Category, back_populates='likes'),
        })

        self._mapper_registry.map_imperatively(Match, mappings.get_match_mapping(), properties={
            'user': relationship(User, back_populates='matches'),
            'recipe': relationship(Recipe, back_populates='matches'),
        })

        self._metadata.create_all()

    def create(self, item: Entity):
        self._session.add(item)
        self._session.commit()

    @property
    def session(self) -> Session:
        return self._session

    @property
    def metadata(self) -> MetaData:
        return self._metadata

    def __repr__(self):
        return '{c}(metadata={metadata}, session={session})'.format(
            c=self.__class__.__name__,
            metadata=self.metadata.__repr__(),
            session=self.session.__repr__()
        )


def get_postgres_database(config: DatabaseConfig) -> PostgresDatabase:
    return PostgresDatabase(config)
