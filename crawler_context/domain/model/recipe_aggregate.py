from __future__ import annotations

from datetime import datetime
from typing import List
from typing import Tuple
from uuid import UUID

from common.domain.model_base import Entity
from common.domain.value_objects import AggregateRating, URL, Author
from common.exceptions import InvalidValueError
from crawler_context.domain.model.category_aggregate import Category
from crawler_context.domain.model.ingredient_aggregate import Ingredient


def create_recipe(recipe_id: UUID, name: str, description: str, image_urls: List[str], category: Category,
                  ingredients: List[Ingredient], instructions: str, date_published: datetime,
                  author: str, rating_count: int, rating_value: float) -> Recipe:
    if not isinstance(name, str):
        raise InvalidValueError(Recipe, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueError(Recipe, 'description must be a string')

    if not isinstance(image_urls, list):
        raise InvalidValueError(Recipe, 'image urls must be a list of strings')

    if not isinstance(category, Category):
        raise InvalidValueError(Recipe, 'category must be a Category instance')

    if not isinstance(ingredients, list):
        raise InvalidValueError(Recipe, 'ingredients must be a list of Ingredient instances')

    if not isinstance(instructions, str):
        raise InvalidValueError(Recipe, 'instructions must be a string')

    if not isinstance(date_published, datetime):
        raise InvalidValueError(Recipe, 'date_published must be a datetime')

    if not isinstance(author, str):
        raise InvalidValueError(Recipe, 'author must be a string')

    if not isinstance(rating_count, int):
        raise InvalidValueError(Recipe, 'rating_count must be a int')

    if not isinstance(rating_value, float):
        raise InvalidValueError(Recipe, 'rating_value must be a float')

    image_url_objects = [URL(url=image_url) for image_url in image_urls]
    author_object = Author(name=author)
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
        recipe_id=recipe_id,
        name=name,
        description=description,
        image_urls=image_url_objects,
        category=category,
        ingredients=ingredients,
        instructions=instructions,
        date_published=date_published,
        author=author_object,
        aggregate_rating=aggregate_rating_object,
    )


class Recipe(Entity):

    def __init__(self, recipe_id: UUID, name: str, description: str, image_urls: List[URL], category: Category, ingredients: List[Ingredient],
                 instructions: str, date_published: datetime, author: Author, aggregate_rating: AggregateRating):
        super().__init__(recipe_id)

        self._name = name
        self._description = description
        self._category = category
        self._instructions = instructions
        self._date_published = date_published
        self._author = author
        self._aggregate_rating = aggregate_rating

        self._image_urls: List[URL] = []
        self._ingredients: List[Ingredient] = []

        for image_url in image_urls:
            self.add_image_url(image_url)

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @property
    def description(self) -> str:
        self._check_not_discarded()
        return self._description

    @property
    def image_urls(self) -> Tuple[URL]:
        self._check_not_discarded()
        return tuple(self._image_urls)

    def add_image_url(self, url: URL):
        self._check_not_discarded()
        if not isinstance(url, URL):
            raise InvalidValueError(self, 'image url must be an URL instance')
        self._image_urls.append(url)
        self._increment_version()

    def remove_image_url(self, url: URL):
        self._check_not_discarded()
        if not isinstance(url, URL):
            raise InvalidValueError(self, 'image url must be an URL instance')
        self._image_urls.remove(url)
        self._increment_version()

    @property
    def category(self) -> Category:
        self._check_not_discarded()
        return self._category

    @property
    def ingredients(self) -> Tuple[Ingredient]:
        self._check_not_discarded()
        return tuple(self._ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise InvalidValueError(self, 'ingredient must be an Ingredient instance')
        self._ingredients.append(ingredient)
        self._increment_version()

    def remove_ingredient(self, ingredient: str):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise InvalidValueError(self, 'ingredient must be an Ingredient instance')
        self._ingredients.remove(ingredient)
        self._increment_version()

    @property
    def instructions(self) -> str:
        self._check_not_discarded()
        return self._instructions

    @property
    def date_published(self) -> datetime:
        self._check_not_discarded()
        return self._date_published

    @property
    def author(self) -> Author:
        self._check_not_discarded()
        return self._author

    @property
    def aggregate_rating(self) -> AggregateRating:
        self._check_not_discarded()
        return self._aggregate_rating

    def __str__(self) -> str:
        return f"Recipe '{self._name}' from {self._date_published.strftime('%d.%m.%Y')}"
