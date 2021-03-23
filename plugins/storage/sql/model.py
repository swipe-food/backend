from __future__ import annotations

import uuid
from typing import List, Type

from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey, TIMESTAMP, func, Text, Interval, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from domain.model.category_aggregate.entities import Category
from domain.model.common_aggregate import Language, Entity
from domain.model.match_aggregate.entities import Match
from domain.model.recipe_aggregate.entities import ImageURL, Ingredient, Recipe
from domain.model.user_aggregate import User, CategoryLike
from domain.model.vendor_aggregate.entities import Vendor

Base = declarative_base()


def get_association_table(name: str, left: str, right: str) -> Table:
    return Table(
        name,
        Base.metadata,
        Column(f'fk_{left}', UUID(as_uuid=True), ForeignKey(f'{left}.id')),
        Column(f'fk_{right}', UUID(as_uuid=True), ForeignKey(f'{right}.id'))
    )


def parse_list(model: Type[Base], entities: List[Entity]):
    return [model.from_entity(entity) for entity in entities]


class DBLanguage(Base):
    __tablename__ = 'language'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    code = Column(String(2))

    @classmethod
    def from_entity(cls, language: Language) -> DBLanguage:
        return cls(
            id=language.id,
            name=language.name,
            code=language.code
        )


user_languages_association_table = get_association_table('user_languages', 'user', 'language')
seen_recipes_association_table = get_association_table('user_seen_recipes', 'user', 'recipe')


class DBUser(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    first_name = Column(String(50))
    is_confirmed = Column(Boolean, nullable=False, server_default='0')
    date_last_login = Column(Date)
    email = Column(String(50))
    languages = relationship('DBLanguage', secondary=user_languages_association_table)
    liked_categories = relationship('DBCategoryLike', back_populates='user')
    matches = relationship('DBMatch', back_populates='user')
    seen_recipes = relationship('DBRecipe', secondary=seen_recipes_association_table)

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id,
            name=user.name,
            first_name=user.first_name,
            is_confirmed=user.is_confirmed,
            date_last_login=user.date_last_login,
            email=user.email.__str__(),
            languages=parse_list(DBLanguage, user.languages),
            liked_categories=parse_list(DBCategoryLike, user.liked_categories),
            matches=parse_list(DBMatch, user.matches),
            seen_recipes=parse_list(DBRecipe, user.seen_recipes),
        )


class DBCategoryLike(Base):
    __tablename__ = 'category_like'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    views = Column(Integer)
    matches = Column(Integer)
    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    fk_category = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    user = relationship('DBUser', back_populates='liked_categories')
    category = relationship('DBCategory', back_populates='likes')

    @classmethod
    def from_entity(cls, category_like: CategoryLike):
        return cls(
            id=category_like.id,
            views=category_like.views,
            matches=category_like.matches,
            fk_user=category_like.user.id,
            fk_category=category_like.category.id,
    #        user=DBUser.from_entity(category_like.user),
    #        category=DBCategory.from_entity(category_like.category),
        )


class DBCategory(Base):
    __tablename__ = 'category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))
    likes = relationship('DBCategoryLike', back_populates='category')
    recipes = relationship('DBRecipe', back_populates='category')

    @classmethod
    def from_entity(cls, category: Category):
        return cls(
            id=category.id,
            name=category.name,
            fk_vendor=category.vendor.id,
   #         vendor=DBVendor.from_entity(category.vendor),
            likes=parse_list(DBCategoryLike, category.likes),
            recipes=parse_list(DBRecipe, category.recipes),
        )


class DBMatch(Base):
    __tablename__ = 'match'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_seen_by_user = Column(Boolean, nullable=False, server_default='0')
    is_active = Column(Boolean, nullable=False, server_default='0')
    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))
    user = relationship('DBUser', back_populates='matches')
    recipe = relationship('DBRecipe', back_populates='matches')

    @classmethod
    def from_entity(cls, match: Match):
        return cls(
            id=match.id,
            timestamp=match.timestamp,
            is_seen_by_user=match.is_seen_by_user,
            fk_user=match.user.id,
            user=parse_list(DBUser, match.user),
            fk_recipe=match.recipe.id,
            recipe=parse_list(DBRecipe, match.recipe)
        )


class DBImageURL(Base):
    __tablename__ = 'image_url'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    url = Column(String(200), server_default='')
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))

    @classmethod
    def from_entity(cls, image_url: ImageURL, recipe_id: UUID):
        return cls(
            id=image_url.id,
            url=image_url.__str__(),
            fk_recipe=recipe_id
        )


class DBIngredient(Base):
    __tablename__ = 'ingredient'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    text = Column(String(200), server_default='')
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))

    @classmethod
    def from_entity(cls, ingredient: Ingredient, recipe_id: UUID):
        return cls(
            id=ingredient.id,
            text=ingredient.text,
            fk_recipe=recipe_id
        )


class DBRecipe(Base):
    __tablename__ = 'recipe'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, server_default='')
    vendor_id = Column(String(100))
    prep_time = Column(Interval())
    cook_time = Column(Interval())
    total_time = Column(Interval())
    url = Column(String(200))
    fk_category = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    category = relationship('DBCategory')
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'))
    language = relationship('DBLanguage')
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))
    images = relationship('DBImageURL', cascade="all, delete-orphan")
    ingredients = relationship('DBIngredient', cascade="all, delete-orphan")
    matches = relationship('DBMatch', back_populates='recipe')

    @classmethod
    def from_entity(cls, recipe: Recipe):
        return cls(
            id=recipe.id,
            name=recipe.name,
            description=recipe.description,
            vendor_id=recipe.vendor_id,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            total_time=recipe.total_time,
            url=recipe.url.__str__(),
            fk_category=recipe.category.id,
            category=DBCategory.from_entity(recipe.category),
            fk_language=recipe.language.id,
            language=DBLanguage.from_entity(recipe.language),
            fk_vendor=recipe.vendor.id,
            images=parse_list(DBImageURL, recipe.images),
            ingredients=parse_list(DBIngredient, recipe.ingredients),
            matches=parse_list(DBMatch, recipe.matches),
        )


vendor_languages_association_table = get_association_table('vendor_languages', 'vendor', 'language')


class DBVendor(Base):
    __tablename__ = 'vendor'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, server_default='')
    url = Column(String(200))
    is_active = Column(Boolean, nullable=False, server_default='0')
    date_last_crawled = Column(Date)
    recipe_pattern = Column(String(100))
    languages = relationship('DBLanguage', secondary=vendor_languages_association_table)
    categories = relationship('DBCategory')

    @classmethod
    def from_entity(cls, vendor: Vendor):
        return cls(
            id=vendor.id,
            name=vendor.name,
            description=vendor.description,
            url=vendor.url.__str__(),
            is_active=vendor.is_active,
            date_last_crawled=vendor.date_last_crawled,
            recipe_pattern=vendor.recipe_pattern,
            languages=parse_list(DBLanguage, vendor.languages),
            categories=parse_list(DBCategory, vendor.categories),
        )
