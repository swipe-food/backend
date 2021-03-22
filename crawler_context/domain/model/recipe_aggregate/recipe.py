from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

from common.domain import Entity, URL, AggregateRating, Ingredient
from crawler_context.domain.model.recipe_aggregate.value_objects import RecipeCategory, Author


class Recipe(Entity):

    def __init__(self, name: str, description: str, image_url: URL, category: RecipeCategory, ingredients: List[Ingredient],
                 instructions: str, date_published: datetime, author: Author, aggregate_rating: AggregateRating):
        super().__init__()

        self._name = name
        self._description = description
        self._image_url = image_url
        self._category = category
        self._instructions = instructions
        self._date_published = date_published
        self._author = author
        self._aggregate_rating = aggregate_rating

        self._ingredients: List[Ingredient] = []

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
    def image_url(self) -> URL:
        self._check_not_discarded()
        return self._image_url

    @property
    def category(self) -> RecipeCategory:
        self._check_not_discarded()
        return self._category

    @property
    def ingredients(self) -> Tuple[Ingredient]:
        self._check_not_discarded()
        return tuple(self._ingredients)

    def add_ingredient(self, ingredient: str or Ingredient):
        self._check_not_discarded()
        if isinstance(ingredient, str):
            ingredient = Ingredient(text=ingredient)
        elif not isinstance(ingredient, Ingredient):
            raise ValueError('ingredient must be a string or an Ingredient instance')
        self._ingredients.append(ingredient)
        self._increment_version()

    def remove_ingredient(self, ingredient: str):
        self._check_not_discarded()
        if isinstance(ingredient, str):
            ingredient = Ingredient(text=ingredient)
        elif not isinstance(ingredient, Ingredient):
            raise ValueError('ingredient must be a string or an Ingredient instance')
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

    @classmethod
    def from_structured_data(cls, structured_data: dict) -> Recipe:
        category = RecipeCategory(name=cls._get_attribute_from_structured_data('recipeCategory', structured_data))
        ingredients = [Ingredient(ingredient) for ingredient in cls._get_attribute_from_structured_data('recipeIngredient', structured_data)]
        author = Author(name=structured_data.get('author', dict()).get('name'))
        aggregate_rating = AggregateRating(
            rating_count=structured_data.get('aggregateRating', dict()).get('ratingCount'),
            rating_value=structured_data.get('aggregateRating', dict()).get('ratingValue'),
        )
        return cls(
            name=cls._get_attribute_from_structured_data('name', structured_data),
            description=cls._get_attribute_from_structured_data('description', structured_data),
            image_url=cls._get_attribute_from_structured_data('image', structured_data),
            category=category,
            ingredients=ingredients,
            instructions=cls._get_attribute_from_structured_data('recipeInstructions', structured_data),
            date_published=datetime.strptime(cls._get_attribute_from_structured_data('datePublished', structured_data), '%Y-%m-%d'),
            author=author,
            aggregate_rating=aggregate_rating,
        )

    @staticmethod
    def _get_attribute_from_structured_data(attribute: str, structured_data: dict):
        return structured_data.get(attribute, None)

    def __str__(self) -> str:
        return f"Recipe '{self._name}' from {self._date_published.strftime('%d.%m.%Y')}"
