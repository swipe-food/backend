from __future__ import annotations

from datetime import timedelta
from typing import List, Tuple

from common.domain.model_base import Entity
from common.domain.value_objects import URL, Language, Ingredient, AggregateRating, RecipeURL
from common.exceptions import InvalidValueError
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.vendor_aggregate import Vendor


def create_recipe(name: str, description: str, vendor_id: str, recipe_url: str,
                  image_urls: List[str], ingredients: List[str], rating_count: int, rating_value: float,
                  category: Category, vendor: Vendor, language: Language, prep_time: timedelta = None,
                  cook_time: timedelta = None, total_time: timedelta = None) -> Recipe:
    if not isinstance(name, str):
        raise InvalidValueError(Recipe, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueError(Recipe, 'description must be a string')

    if not isinstance(prep_time, timedelta):
        raise InvalidValueError(Recipe, 'prep_time must be a timedelta')

    if not isinstance(cook_time, timedelta):
        raise InvalidValueError(Recipe, 'cook_time must be a timedelta')

    if not isinstance(total_time, timedelta):
        raise InvalidValueError(Recipe, 'total_time must be a timedelta')

    if not isinstance(category, Category):
        raise InvalidValueError(Recipe, 'category must be a Category instance')

    if not isinstance(vendor, Vendor):
        raise InvalidValueError(Recipe, 'vendor must be a Vendor instance')

    if not isinstance(language, Language):
        raise InvalidValueError(Recipe, 'language must be a Language instance')

    if not isinstance(image_urls, list):
        raise InvalidValueError(Recipe, 'image_urls must be a list of strings')

    if not isinstance(ingredients, list):
        raise InvalidValueError(Recipe, 'ingredients must be a list of strings')

    recipe_url_object = RecipeURL(url=recipe_url, vendor_pattern=vendor.recipe_pattern)
    image_url_objects = [URL(url=image_url) for image_url in image_urls]
    ingredient_objects = [Ingredient(text=ingredient) for ingredient in ingredients]
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
        name=name,
        description=description,
        vendor_id=vendor_id,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        url=recipe_url_object,
        images=image_url_objects,
        ingredients=ingredient_objects,
        category=category,
        aggregate_rating=aggregate_rating_object,
        language=language,
        vendor=vendor
    )


class Recipe(Entity):

    def __init__(self, name: str, description: str, vendor_id: str, prep_time: timedelta, cook_time: timedelta,
                 total_time: timedelta, url: RecipeURL, images: List[URL], ingredients: List[Ingredient],
                 aggregate_rating: AggregateRating, category: Category, vendor: Vendor, language: Language):
        super().__init__()

        self._name = name
        self._description = description
        self._prep_time = prep_time
        self._cook_time = cook_time
        self._total_time = total_time
        self._category = category
        self._vendor = vendor
        self._language = language
        self._matches = 0

        self.vendor_id = vendor_id
        self.url = url
        self.aggregate_rating = aggregate_rating

        self._ingredients: List[Ingredient] = []
        self._images: List[URL] = []

        for ingredient in ingredients:
            self.add_ingredient(ingredient)

        for image in images:
            self.add_image(image)

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @property
    def description(self) -> str:
        self._check_not_discarded()
        return self._description

    @property
    def vendor_id(self) -> str:
        self._check_not_discarded()
        return self._vendor_id

    @vendor_id.setter
    def vendor_id(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise InvalidValueError(self, 'vendor_id must be a string')
        self._vendor_id = value
        self._increment_version()

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
    def url(self) -> RecipeURL:
        self._check_not_discarded()
        return self._url

    @url.setter
    def url(self, value: RecipeURL):
        self._check_not_discarded()
        if not isinstance(value, RecipeURL):
            raise InvalidValueError(self, 'url must be a RecipeURL instance')
        self._url = value
        self._increment_version()

    @property
    def images(self) -> Tuple[URL]:
        self._check_not_discarded()
        return tuple(self._images)

    def add_image(self, image_url: URL):
        self._check_not_discarded()
        if not isinstance(image_url, RecipeURL):
            raise InvalidValueError(self, 'image_url must be a URL instance')
        self._images.append(image_url)
        self._increment_version()

    def remove_image(self, image_url: URL):
        self._check_not_discarded()
        if not isinstance(image_url, RecipeURL):
            raise InvalidValueError(self, 'image_url must be a URL instance')
        self._images.remove(image_url)
        self._increment_version()

    @property
    def ingredients(self) -> Tuple[Ingredient]:
        self._check_not_discarded()
        return tuple(self._ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise InvalidValueError(self, 'ingredient must be a Ingredient instance')
        self._ingredients.append(ingredient)
        self._increment_version()

    def remove_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise InvalidValueError(self, 'ingredient must be a Ingredient instance')
        self._ingredients.remove(ingredient)
        self._increment_version()

    @property
    def aggregate_rating(self) -> AggregateRating:
        self._check_not_discarded()
        return self._aggregate_rating

    @aggregate_rating.setter
    def aggregate_rating(self, rating: Tuple[int, float]):
        self._check_not_discarded()
        self._aggregate_rating = AggregateRating(*rating)
        self._increment_version()

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

    @property
    def matches(self) -> int:
        self._check_not_discarded()
        return self._matches

    def add_match(self):
        self._check_not_discarded()
        self._matches += 1
        self._increment_version()

    def remove_match(self):
        self._check_not_discarded()
        self._matches -= 1
        self._increment_version()

    def delete(self):
        super().delete()

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
