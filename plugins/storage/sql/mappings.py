import uuid

from sqlalchemy import Table, Column, String, MetaData, Boolean, Date, Integer, TIMESTAMP, Text, Interval, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class SQLAlchemyMappings:

    def __init__(self, metadata: MetaData):
        self._metadata = metadata
        self.key_type = UUID(as_uuid=True)
        self._pk_column = Column('_id', self.key_type, primary_key=True, default=uuid.uuid4, unique=True,
                                 nullable=False)

    def get_language_mapping(self) -> Table:
        return Table(
            'language',
            self._metadata,
            self._pk_column.copy(),
            Column('_name', String(50), nullable=False),
            Column('_code', String(2)),
        )

    def get_user_mapping(self) -> Table:
        return Table(
            'user',
            self._metadata,
            self._pk_column.copy(),
            Column('_name', String(50)),
            Column('_first_name', String(50)),
            Column('_is_confirmed', Boolean, nullable=False, server_default='0'),
            Column('_date_last_login', Date),
            Column('_email', String(50)),
        )

    def get_category_like_mapping(self) -> Table:
        return Table(
            'category_like',
            self._metadata,
            self._pk_column.copy(),
            Column('_views', Integer),
            Column('_matches', Integer),
            Column('user_id', self.key_type, ForeignKey('user._id')),
            Column('category_id', self.key_type, ForeignKey('category._id')),
        )

    def get_category_mapping(self) -> Table:
        return Table(
            'category',
            self._metadata,
            self._pk_column.copy(),
            Column('_name', String(50)),
            Column('_vendor_id', self.key_type, ForeignKey('vendor._id')),
        )

    def get_match_mapping(self) -> Table:
        return Table(
            'match',
            self._metadata,
            self._pk_column.copy(),
            Column('_timestamp', TIMESTAMP(timezone=True), nullable=False, server_default=func.now()),
            Column('_is_seen_by_user', Boolean, nullable=False, server_default='0'),
            Column('_is_active', Boolean, nullable=False, server_default='0'),
            Column('user_id', self.key_type, ForeignKey('user._id')),
            Column('recipe_id', self.key_type, ForeignKey('recipe._id'))
        )

    def get_image_url_mapping(self) -> Table:
        return Table(
            'image_url',
            self._metadata,
            self._pk_column.copy(),
            Column('_url', String(200), server_default=''),
            Column('recipe_id', self.key_type, ForeignKey('recipe._id'), nullable=False)
        )

    def get_ingredient_mapping(self) -> Table:
        return Table(
            'ingredient',
            self._metadata,
            self._pk_column.copy(),
            Column('_text', String(200), server_default=''),
            Column('recipe_id', self.key_type, ForeignKey('recipe._id'), nullable=False)
        )

    def get_recipe_mapping(self) -> Table:
        return Table(
            'recipe',
            self._metadata,
            self._pk_column.copy(),
            Column('_name', String(100), nullable=False),
            Column('_description', Text, server_default=''),
            Column('_vendor_id', String(100)),
            Column('_prep_time', Interval()),
            Column('_cook_time', Interval()),
            Column('_total_time', Interval()),
            Column('_url', String(200)),
            Column('category_id', self.key_type, ForeignKey('category._id')),
            Column('language_id', self.key_type, ForeignKey('language._id')),
            Column('vendor_id', self.key_type, ForeignKey('vendor._id')),
        )

    def get_vendor_mapping(self) -> Table:
        return Table(
            'vendor',
            self._metadata,
            self._pk_column.copy(),
            Column('_name', String(100), nullable=False),
            Column('_description', Text, server_default=''),
            Column('_url', String(200)),
            Column('_is_active', Boolean, nullable=False, server_default='0'),
            Column('_date_last_crawled', Date),
            Column('_recipe_pattern', String(100)),
        )

    def get_association_table(self, name: str, left: str, right: str) -> Table:
        return Table(
            name,
            self._metadata,
            Column(f'{left}_id', self.key_type, ForeignKey(f'{left}._id')),
            Column(f'{right}_id', self.key_type, ForeignKey(f'{right}._id'))
        )


def create_sql_mappings(metadata: MetaData) -> SQLAlchemyMappings:
    if not isinstance(metadata, MetaData):
        raise ValueError('metadata must be a MetaData instance')

    return SQLAlchemyMappings(metadata=metadata)
