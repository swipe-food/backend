from __future__ import annotations

import uuid

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, TIMESTAMP, func, Text, Interval, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

from domain.model.category_aggregate import Category, create_category
from domain.model.category_like_aggregate import CategoryLike, create_category_like
from domain.model.ingredient_aggregate import Ingredient, create_ingredient
from domain.model.language_aggregate import Language
from domain.model.match_aggregate import Match, create_match
from domain.model.recipe_aggregate import Recipe, create_recipe
from domain.model.user_aggregate import User, create_user
from domain.model.vendor_aggregate import Vendor, create_vendor

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
            code=language.code,
        )

    def to_entity(self) -> Language:
        return Language(
            language_id=self.id,
            name=self.name,
            code=self.code,
        )


class DBUserLanguages(Base):
    __tablename__ = 'user_languages'

    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True, nullable=False)
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, user: User, language: Language) -> DBUserLanguages:
        return cls(
            fk_user=user.id,
            fk_language=language.id,
        )


class DBUserSeenRecipes(Base):
    __tablename__ = 'user_seen_recipes'

    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'), primary_key=True, nullable=False)
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, user: User, recipe: Recipe) -> DBUserSeenRecipes:
        return cls(
            fk_user=user.id,
            fk_recipe=recipe.id,
        )


class DBUser(Base):
    __tablename__ = 'user'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    first_name = Column(String(50))
    is_confirmed = Column(Boolean, nullable=False, server_default='0')
    date_last_login = Column(DateTime())
    email = Column(String(50))
    languages = relationship("DBLanguage", secondary="user_languages")
    seen_recipes = relationship("DBRecipe", secondary="user_seen_recipes")
    matches = relationship("DBMatch", back_populates="user")
    liked_categories = relationship("DBCategoryLike", back_populates="user")

    @classmethod
    def from_entity(cls, user: User):
        """creates a DBUser instance from the entity class User.
            Important: The relationships of the DBUser class are not parsed. They have to be added manually.
        """
        return cls(
            id=user.id,
            name=user.name,
            first_name=user.first_name,
            is_confirmed=user.is_confirmed,
            date_last_login=user.date_last_login,
            email=user.email.__str__(),
        )

    def to_entity(self) -> User:
        return create_user(
            user_id=self.id,
            name=self.name,
            first_name=self.first_name,
            email=self.email,
            is_confirmed=self.is_confirmed,
            date_last_login=self.date_last_login,
            languages=[language.to_entity() for language in self.languages],
            liked_categories=[],
            matches=[],
            seen_recipes=[seen_recipe.to_entity() for seen_recipe in self.seen_recipes],
        )


class DBCategoryLike(Base):
    __tablename__ = 'category_like'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    fk_category = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    views = Column(Integer)
    matches = Column(Integer)
    user = relationship("DBUser", back_populates="liked_categories")
    category = relationship("DBCategory")

    @classmethod
    def from_entity(cls, category_like: CategoryLike):
        """creates a DBCategoryLike instance from the entity class CategoryLike.
            Important: The relationships of the DBCategoryLike class are not parsed. They have to be added manually.
        """
        return cls(
            id=category_like.id,
            fk_user=category_like.user.id,
            fk_category=category_like.category.id,
            views=category_like.views,
            matches=category_like.matches,
        )

    def to_entity(self) -> CategoryLike:
        return create_category_like(
            category_like_id=self.id,
            user=self.user.to_entity(),
            category=self.category.to_entity(),
            views=self.views,
            matches=self.matches,
        )


class DBCategory(Base):
    __tablename__ = 'category'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(50), nullable=False)
    url = Column(String(200), unique=True)
    likes = Column(Integer, nullable=False, default=0)
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))
    vendor = relationship("DBVendor", back_populates="categories")

    @classmethod
    def from_entity(cls, category: Category):
        """creates a DBCategoryLike instance from the entity class Category.
            Important: The relationship of the DBCategory class are not parsed. They have to be added manually.
        """
        return cls(
            id=category.id,
            name=category.name,
            url=category.url.__str__(),
            fk_vendor=category.vendor.id,
        )

    def to_entity(self) -> Category:
        return create_category(
            category_id=self.id,
            name=self.name,
            url=self.url,
            vendor=self.vendor.to_entity(),
        )


class DBMatch(Base):
    __tablename__ = 'match'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    is_seen_by_user = Column(Boolean, nullable=False, server_default='0')
    is_active = Column(Boolean, nullable=False, server_default='0')
    fk_user = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    fk_recipe = Column(UUID(as_uuid=True), ForeignKey('recipe.id'))
    user = relationship("DBUser", back_populates="matches")
    recipe = relationship("DBRecipe")

    @classmethod
    def from_entity(cls, match: Match):
        """creates a DBMatch instance from the entity class Match.
            Important: The relationship of the DBMatch class are not parsed. They have to be added manually.
        """
        return cls(
            id=match.id,
            timestamp=match.timestamp,
            is_seen_by_user=match.is_seen_by_user,
            is_active=match.is_active,
            fk_user=match.user.id,
            fk_recipe=match.recipe.id,
        )

    def to_entity(self) -> Match:
        return create_match(
            match_id=self.id,
            timestamp=self.timestamp,
            is_seen_by_user=self.is_seen_by_user,
            is_active=self.is_active,
            user=self.user.to_entity(),
            recipe=self.recipe.to_entity(),
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
            fk_recipe=recipe_id,
        )

    def to_entity(self):
        return create_ingredient(
            ingredient_id=self.id,
            text=self.text,
        )


class DBRecipe(Base):
    __tablename__ = 'recipe'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, server_default='')
    author = Column(String(50))
    prep_time = Column(Interval())
    cook_time = Column(Interval())
    total_time = Column(Interval())
    date_published = Column(DateTime())
    url = Column(String(200))
    rating_count = Column(Integer())
    rating_value = Column(Float())
    fk_category = Column(UUID(as_uuid=True), ForeignKey('category.id'))
    category = relationship("DBCategory")
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'))
    language = relationship("DBLanguage")
    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'))
    vendor = relationship("DBVendor")
    image = Column(String(200))
    ingredients = relationship("DBIngredient")

    @classmethod
    def from_entity(cls, recipe: Recipe):
        """creates a DBRecipe instance from the entity class Recipe.
            Important: The relationship of the DBRecipe class are not parsed. They have to be added manually.
        """
        return cls(
            id=recipe.id,
            name=recipe.name,
            description=recipe.description,
            author=recipe.author.__str__(),
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

    def to_entity(self) -> Recipe:
        return create_recipe(
            recipe_id=self.id,
            name=self.name,
            description=self.description,
            author=self.author,
            prep_time=self.prep_time,
            cook_time=self.cook_time,
            total_time=self.total_time,
            date_published=self.date_published,
            url=self.url,
            rating_value=self.rating_value,
            rating_count=self.rating_count,
            image_url=self.image,
            ingredients=[db_ingredient.to_entity() for db_ingredient in self.ingredients],
            category=self.category.to_entity(),
            vendor=self.vendor.to_entity(),
            language=self.language.to_entity(),
        )


class DBVendorLanguages(Base):
    __tablename__ = 'vendor_languages'

    fk_vendor = Column(UUID(as_uuid=True), ForeignKey('vendor.id'), primary_key=True, nullable=False)
    fk_language = Column(UUID(as_uuid=True), ForeignKey('language.id'), primary_key=True, nullable=False)

    @classmethod
    def from_entity(cls, vendor: Vendor, language: Language) -> DBVendorLanguages:
        return cls(
            fk_vendor=vendor.id,
            fk_language=language.id,
        )


class DBVendor(Base):
    __tablename__ = 'vendor'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, server_default='')
    url = Column(String(200), nullable=False)
    is_active = Column(Boolean, server_default='0')
    recipe_pattern = Column(String(100))
    date_last_crawled = Column(DateTime())
    categories_link = Column(String(200))
    languages = relationship("DBLanguage", secondary="vendor_languages")
    categories = relationship("DBCategory", back_populates="vendor")

    @classmethod
    def from_entity(cls, vendor: Vendor):
        """creates a DBVendor instance from the user context entity class Vendor.
            Important: The relationship of the DBVendor class are not parsed. They have to be added manually.
        """
        return cls(
            id=vendor.id,
            name=vendor.name,
            description=vendor.description,
            url=vendor.url.__str__(),
            is_active=vendor.is_active,
            date_last_crawled=vendor.date_last_crawled,
            categories_link=vendor.categories_link,
            recipe_pattern=vendor.recipe_pattern,
        )

    def to_entity(self) -> Vendor:
        return create_vendor(
            vendor_id=self.id,
            name=self.name,
            description=self.description,
            url=self.url,
            is_active=self.is_active,
            recipe_pattern=self.recipe_pattern,
            categories_link=self.categories_link,
            date_last_crawled=self.date_last_crawled,
            languages=[language.to_entity() for language in self.languages],
            categories=[],
        )
