from sqlalchemy import Table, Column, String, MetaData, Boolean, Date, Integer, TIMESTAMP, Text, Interval, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class SQLAlchemyMappings:

    def __init__(self, metadata: MetaData):
        self._metadata = metadata
        self._pk_column = Column('id', UUID(as_uuid=True), primary_key=True)

    def get_language_mapping(self) -> Table:
        return Table(
            'language',
            self._metadata,
            self._pk_column.copy(),
            Column('name', String(50), nullable=False),
            Column('code', String(2)),
        )

    def get_user_mapping(self) -> Table:
        return Table(
            'user',
            self._metadata,
            self._pk_column.copy(),
            Column('name', String(50)),
            Column('first_name', String(50)),
            Column('is_confirmed', Boolean, nullable=False, server_default='0'),
            Column('date_last_login', Date),
            Column('email', String(50)),
        )

    def get_category_like_mapping(self) -> Table:
        return Table(
            'category_like',
            self._metadata,
            self._pk_column.copy(),
            Column('views', Integer),
            Column('matches', Integer),
        )

    def get_category_mapping(self) -> Table:
        return Table(
            'category',
            self._metadata,
            self._pk_column.copy(),
            Column('name', String(50)),
        )

    def get_match_mapping(self) -> Table:
        return Table(
            'match',
            self._metadata,
            self._pk_column.copy(),
            Column('timestamp', TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
            Column('is_seen_by_user', Boolean, nullable=False, server_default='0'),
            Column('is_active', Boolean, nullable=False, server_default='0'),
        )

    def get_image_url_mapping(self) -> Table:
        return Table(
            'image_url',
            self._metadata,
            self._pk_column.copy(),
            Column('url', String(200)),
            Column('recipe_id', UUID(as_uuid=True), ForeignKey('recipe.id'))
        )

    def get_ingredient_mapping(self) -> Table:
        return Table(
            'ingredient',
            self._metadata,
            self._pk_column.copy(),
            Column('text', String(200)),
            Column('recipe_id', UUID(as_uuid=True), ForeignKey('recipe.id'))
        )

    def get_recipe_mapping(self) -> Table:
        return Table(
            'recipe',
            self._metadata,
            self._pk_column.copy(),
            Column('name', String(100), nullable=False),
            Column('description', Text, server_default=''),
            Column('vendor_id', String(100)),
            Column('prep_time', Interval()),
            Column('cook_time', Interval()),
            Column('total_time', Interval()),
            Column('total_time', Interval()),
            Column('url', String(200)),
        )

    def get_vendor_mapping(self) -> Table:
        return Table(
            'vendor',
            self._metadata,
            self._pk_column.copy(),
            Column('name', String(100), nullable=False),
            Column('description', Text, server_default=''),
            Column('url', String(200)),
            Column('is_active', Boolean, nullable=False, server_default='0'),
            Column('date_last_crawled', Date),
            Column('recipe_pattern', String(100)),
        )

    def get_association_table(self, name: str, left: str, right: str) -> Table:
        return Table(
            name,
            self._metadata,
            Column(f'{left}_id', UUID(as_uuid=True), ForeignKey(f'{left}.id')),
            Column(f'{right}_id', UUID(as_uuid=True), ForeignKey(f'{right}.id'))
        )
