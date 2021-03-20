from datetime import timedelta
from typing import List, Tuple

from domain.model.category_aggregate import Category
from domain.model.common_aggregate import Language, URL
from domain.model.entity import Entity
from domain.model.match_aggregate import Match
from domain.model.recipe_aggregate.value_objects import RecipeURL, AggregateRating, Ingredient
from domain.model.vendor_aggregate import Vendor


class Recipe(Entity):

    def __init__(self, name: str, description: str, vendor_id: str, prep_time: timedelta, cook_time: timedelta,
                 total_time: timedelta, url: RecipeURL, images: List[URL], ingredients: List[Ingredient],
                 aggregate_rating: AggregateRating, category: Category, vendor: Vendor, language: Language):
        super().__init__()

        if not isinstance(name, str):
            raise ValueError('name must be a string')

        if not isinstance(description, str):
            raise ValueError('description must be a string')

        if not isinstance(prep_time, timedelta):
            raise ValueError('prep_time must be a timedelta')

        if not isinstance(cook_time, timedelta):
            raise ValueError('cook_time must be a timedelta')

        if not isinstance(total_time, timedelta):
            raise ValueError('total_time must be a timedelta')

        if not isinstance(aggregate_rating, AggregateRating):
            raise ValueError('aggregate_rating must be a AggregateRating instance')

        if not isinstance(category, Category):
            raise ValueError('category must be a Category instance')

        if not isinstance(vendor, Vendor):
            raise ValueError('vendor must be a Vendor instance')

        if not isinstance(language, Language):
            raise ValueError('language must be a Language instance')

        if not isinstance(images, list):
            raise ValueError('images must be a list of URL instances')

        if not isinstance(ingredients, list):
            raise ValueError('ingredients must be a list of Ingredient instances')

        self._name = name
        self._description = description
        self._prep_time = prep_time
        self._cook_time = cook_time
        self._total_time = total_time
        self._aggregate_rating = aggregate_rating
        self._category = category
        self._vendor = vendor
        self._language = language

        self.vendor_id = vendor_id
        self.url = url

        self._ingredients: List[Ingredient] = []
        self._images: List[URL] = []
        self._matches: List[Match] = []

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
            raise ValueError('vendor_id must be a string')
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
            raise ValueError('url must be a RecipeURL instance')
        self._url = value
        self._increment_version()

    @property
    def images(self) -> Tuple[URL]:
        self._check_not_discarded()
        return tuple(self._images)

    def add_image(self, image_url: URL):
        self._check_not_discarded()
        if not isinstance(image_url, RecipeURL):
            raise ValueError('image_url must be a URL instance')
        self._images.append(image_url)
        self._increment_version()

    def remove_image(self, image_url: URL):
        self._check_not_discarded()
        if not isinstance(image_url, RecipeURL):
            raise ValueError('image_url must be a URL instance')
        self._images.remove(image_url)
        self._increment_version()

    @property
    def ingredients(self) -> Tuple[Ingredient]:
        self._check_not_discarded()
        return tuple(self._ingredients)

    def add_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise ValueError('ingredient must be a Ingredient instance')
        self._ingredients.append(ingredient)
        self._increment_version()

    def remove_ingredient(self, ingredient: Ingredient):
        self._check_not_discarded()
        if not isinstance(ingredient, Ingredient):
            raise ValueError('ingredient must be a Ingredient instance')
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

    @property
    def matches(self) -> Tuple[Match]:
        self._check_not_discarded()
        return tuple(self._matches)

    def add_match(self, match: Match):
        self._check_not_discarded()
        if not isinstance(match, Match):
            raise ValueError('match must be a Match instance')
        self._matches.append(match)
        self._increment_version()

    def remove_match(self, match: Match):
        self._check_not_discarded()
        if not isinstance(match, Match):
            raise ValueError('match must be a Match instance')
        self._matches.remove(match)
        self._increment_version()

    def delete(self):
        for match in self._matches:
            match.delete()
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
