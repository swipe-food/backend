from __future__ import annotations

import uuid

from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey, TIMESTAMP, func, Text, Interval, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from common.domain.model.ingredient_aggregate import Ingredient
from user_context.domain.model.category_aggregate import Category as UserContextCategory
from crawler_context.domain.model.category_aggregate import Category as CrawlerContextCategory
from user_context.domain.model.category_like_aggregate import CategoryLike
from common.domain.model.language_aggregate import Language
from user_context.domain.model.match_aggregate import Match
from user_context.domain.model.recipe_aggregate import Recipe as UserContextRecipe
from crawler_context.domain.model.recipe_aggregate import Recipe as CrawlerContextRecipe
from user_context.domain.model.user_aggregate import User
from user_context.domain.model.vendor_aggregate import Vendor as UserContextVendor
from crawler_context.domain.model.vendor_aggregate import Vendor as CrawlerContextVendor

Base = declarative_base()


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


class DBUserLanguages(Base):
    __tablename__ = 'user_languages'

    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True, nullable=False)
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, user: User, language: Language) -> DBUserLanguages:
        return cls(
            fk_user=user.id,
            fk_language=language.id
        )


class DBUserSeenRecipes(Base):
    __tablename__ = 'user_seen_recipes'

    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True, nullable=False)
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, user: User, recipe: UserContextRecipe) -> DBUserSeenRecipes:
        return cls(
            fk_user=user.id,
            fk_recipe=recipe.id
        )


class DBUser(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    first_name = Column(String(50))
    is_confirmed = Column(Boolean, nullable=False, server_default='0')
    date_last_login = Column(Date)
    email = Column(String(50))

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id,
            name=user.name,
            first_name=user.first_name,
            is_confirmed=user.is_confirmed,
            date_last_login=user.date_last_login,
            email=user.email.__str__()
        )


class DBCategoryLike(Base):
    __tablename__ = 'category_like'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    fk_category = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    views = Column(Integer)
    matches = Column(Integer)

    @classmethod
    def from_entity(cls, category_like: CategoryLike):
        return cls(
            id=category_like.id,
            fk_user=category_like.user.id,
            fk_category=category_like.category.id,
            views=category_like.views,
            matches=category_like.matches,
        )


class DBCategory(Base):
    __tablename__ = 'category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    url = Column(String(200))
    likes = Column(Integer)
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))

    @classmethod
    def from_user_context_entity(cls, category: UserContextCategory):
        return cls(
            id=category.id,
            name=category.name,
            likes=category.likes,
            fk_vendor=category.vendor.id,
        )

    @classmethod
    def from_crawler_context_entity(cls, category: CrawlerContextCategory):
        return cls(
            id=category.id,
            name=category.name,
            url=category.url.__str__(),
            fk_vendor=category.vendor.id,
        )


class DBMatch(Base):
    __tablename__ = 'match'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_seen_by_user = Column(Boolean, nullable=False, server_default='0')
    is_active = Column(Boolean, nullable=False, server_default='0')
    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))

    @classmethod
    def from_entity(cls, match: Match):
        return cls(
            id=match.id,
            timestamp=match.timestamp,
            is_seen_by_user=match.is_seen_by_user,
            fk_user=match.user.id,
            fk_recipe=match.recipe.id,
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
    date_published = Column(Date())
    url = Column(String(200))
    rating_count = Column(Integer())
    rating_value = Column(Float())
    fk_category = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'))
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))
    image = Column(String(200))
    ingredients = relationship('DBIngredient')

    @classmethod
    def from_entity(cls, recipe: UserContextRecipe or CrawlerContextRecipe):
        return cls(
            id=recipe.id,
            name=recipe.name,
            description=recipe.description,
            vendor_id=recipe.vendor_id,
            prep_time=recipe.prep_time,
            cook_time=recipe.cook_time,
            total_time=recipe.total_time,
            date_published=recipe.date_published,
            url=recipe.url.__str__(),
            image=recipe.image.__str__(),
            rating_count=recipe.aggregate_rating.rating_count if recipe.aggregate_rating is not None else None,
            rating_value=recipe.aggregate_rating.rating_value if recipe.aggregate_rating is not None else None,
            fk_category=recipe.category.id,
            fk_language=recipe.language.id,
            fk_vendor=recipe.vendor.id,
            ingredients=[DBIngredient.from_entity(ingredient, recipe.id) for ingredient in recipe.ingredients],
        )


class DBVendorLanguages(Base):
    __tablename__ = 'vendor_languages'

    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'), primary_key=True, nullable=False)
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, vendor: UserContextVendor, language: Language) -> DBVendorLanguages:
        return cls(
            fk_vendor=vendor.id,
            fk_language=language.id
        )


class DBVendor(Base):
    __tablename__ = 'vendor'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, server_default='')
    url = Column(String(200), nullable=False)
    is_active = Column(Boolean, server_default='0')
    recipe_pattern = Column(String(100))
    date_last_crawled = Column(Date())
    categories_link = Column(String(200))

    @classmethod
    def from_user_context_entity(cls, vendor: UserContextVendor):
        return cls(
            id=vendor.id,
            name=vendor.name,
            description=vendor.description,
            url=vendor.url.__str__(),
            is_active=vendor.is_active,
            recipe_pattern=vendor.recipe_pattern,
        )

    @classmethod
    def from_crawler_context_entity(cls, vendor: CrawlerContextVendor):
        return cls(
            id=vendor.id,
            name=vendor.name,
            url=vendor.base_url.__str__(),
            date_last_crawled=vendor.date_last_crawled,
            categories_link=vendor.categories_link
        )