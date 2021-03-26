from __future__ import annotations

import uuid

from sqlalchemy import Column, String, Boolean, Date, Integer, ForeignKey, TIMESTAMP, func, Text, Interval
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from common.domain.value_objects import URL
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.category_like_aggregate import CategoryLike
from user_context.domain.model.ingredient_aggregate import Ingredient
from user_context.domain.model.language_aggregate import Language
from user_context.domain.model.match_aggregate import Match
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate import User
from user_context.domain.model.vendor_aggregate import Vendor

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
    def from_entity(cls, user: User, recipe: Recipe) -> DBUserSeenRecipes:
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
    likes = Column(Integer)
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))

    @classmethod
    def from_entity(cls, category: Category):
        return cls(
            id=category.id,
            name=category.name,
            fk_vendor=category.vendor.id,  # TODO add vendor as attribute in category Entity
            likes=category.likes,
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


class DBImageURL(Base):
    __tablename__ = 'image_url'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    url = Column(String(200), server_default='')
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))

    @classmethod
    def from_entity(cls, image_url: URL, recipe_id: UUID):
        return cls(
            id=uuid.uuid4(),  # TODO model ImageURL as simple URL
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
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'))
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))
    images = relationship('DBImageURL', cascade="all, delete-orphan")
    ingredients = relationship('DBIngredient')

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
            fk_language=recipe.language.id,
            fk_vendor=recipe.vendor.id,
            images=[DBImageURL.from_entity(image, recipe.id) for image in recipe.images],
            ingredients=[DBIngredient.from_entity(ingredient, recipe.id) for ingredient in recipe.ingredients],
        )


class DBVendorLanguages(Base):
    __tablename__ = 'vendor_languages'

    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'), primary_key=True, nullable=False)
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, vendor: Vendor, language: Language) -> DBVendorLanguages:
        return cls(
            fk_vendor=vendor.id,
            fk_language=language.id
        )


class DBVendor(Base):
    __tablename__ = 'vendor'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, server_default='')
    url = Column(String(200))
    is_active = Column(Boolean, nullable=False, server_default='0')
    recipe_pattern = Column(String(100))

    @classmethod
    def from_entity(cls, vendor: Vendor):
        return cls(
            id=vendor.id,
            name=vendor.name,
            description=vendor.description,
            url=vendor.url.__str__(),
            is_active=vendor.is_active,
            recipe_pattern=vendor.recipe_pattern,
        )
