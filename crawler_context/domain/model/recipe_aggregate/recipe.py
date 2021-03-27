from datetime import timedelta, datetime
from typing import List, Tuple
from uuid import UUID

from common.domain.model.base import Entity
from common.domain.model.ingredient_aggregate import Ingredient
from common.domain.model.language_aggregate import Language
from common.domain.model.value_objects import URL, AggregateRating, Author, RecipeURL
from common.exceptions import InvalidValueException
from crawler_context.domain.model.category_aggregate import Category
from crawler_context.domain.model.vendor_aggregate import Vendor


class Recipe(Entity):

    def __init__(self, recipe_id: UUID, name: str, description: str, author: Author, vendor_id: str, prep_time: timedelta,
                 cook_time: timedelta, total_time: timedelta, date_published: datetime, url: RecipeURL, image: URL, ingredients: List[Ingredient],
                 aggregate_rating: AggregateRating, category: Category, vendor: Vendor, language: Language):
        super().__init__(recipe_id)

        self._name = name
        self._description = description
        self._author = author
        self._vendor_id = vendor_id
        self._prep_time = prep_time
        self._cook_time = cook_time
        self._total_time = total_time
        self._date_published = date_published
        self._url = url
        self._category = category
        self._vendor = vendor
        self._language = language
        self._aggregate_rating = aggregate_rating
        self._image = image
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
    def author(self):
        self._check_not_discarded()
        return self._author

    @property
    def vendor_id(self) -> str:
        self._check_not_discarded()
        return self._vendor_id

    @property
    def prep_time(self) -> timedelta:
        self._check_not_discarded()
        return self._prep_time

    @property
    def cook_time(self) -> timedelta:
        self._check_not_discarded()
        return self._cook_time

    @property
    def total_time(self) -> timedelta:
        self._check_not_discarded()
        return self._total_time

    @property
    def date_published(self) -> datetime:
        self._check_not_discarded()
        return self._date_published

    @property
    def url(self) -> RecipeURL:
        self._check_not_discarded()
        return self._url

    @property
    def image(self) -> URL:
        self._check_not_discarded()
        return self._image

    @property
    def ingredients(self) -> Tuple[Ingredient]:
        self._check_not_discarded()
        return tuple(self._ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise InvalidValueException(self, 'ingredient must be a Ingredient instance')
        self._ingredients.append(ingredient)
        self._increment_version()

    def remove_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise InvalidValueException(self, 'ingredient must be a Ingredient instance')
        self._ingredients.remove(ingredient)
        self._increment_version()

    @property
    def aggregate_rating(self) -> AggregateRating:
        self._check_not_discarded()
        return self._aggregate_rating

    @property
    def category(self) -> Category:
        self._check_not_discarded()
        return self._category

    @property
    def vendor(self) -> Vendor:
        self._check_not_discarded()
        return self._vendor

    @property
    def language(self) -> Language:
        self._check_not_discarded()
        return self._language

    def __str__(self) -> str:
        return f"Recipe '{self._name}' from '{self._url.__str__()}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, {url!r}, category_name={category_name!r}, {vendor})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            url=self._url,
            category_name=self._category.name,
            vendor=self._vendor.__repr__(),
        )
