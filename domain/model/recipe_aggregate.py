import uuid
from datetime import timedelta
from typing import List

from domain.model import match_aggregate, category_aggregate, vendor_aggregate
from domain.model.common_aggregate import Entity, URL, Language


class RecipeURL(URL):

    @classmethod
    def from_text_with_pattern(cls, url: str, vendor_pattern: str):
        # TODO validate with pattern of vendor
        scheme, domain, resource, parameters = url, url, url, url
        return cls(scheme, domain, resource, parameters)

    def __init__(self, scheme: str, domain: str, resource: str, parameters: str):
        super().__init__(scheme, domain, resource, parameters)

    def replace(self, scheme: str = None, domain: str = None, resource: str = None, parameters: str = None):
        return RecipeURL(scheme=scheme or self._parts[0],
                         domain=domain or self._parts[1],
                         resource=resource or self._parts[2],
                         parameters=parameters or self._parts[3])


class ImageURL(Entity):

    def __init__(self, image_url_id: uuid.UUID, image_url_version: int, scheme: str, domain: str, resource: str,
                 parameters: str):
        super().__init__(entity_id=image_url_id, entity_version=image_url_version)
        self._parts = (scheme, domain, resource, parameters)

    def __str__(self) -> str:
        return f'{self._parts[0]}//{self._parts[1]}{self._parts[2]}{self._parts[3]}'

    def __repr__(self) -> str:
        return "{c}({s}, url={url!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            url=self.__str__(),
        )


class Ingredient(Entity):
    # TODO check if it is possible to implement this as a value object

    def __init__(self, ingredient_id: uuid.UUID, ingredient_version: int, text: str):
        super().__init__(ingredient_id, ingredient_version)
        self._text = text

    def __str__(self) -> str:
        return f'{self._text}'

    def __repr__(self) -> str:
        return '{c}(text={text!r})'.format(
            c=self.__class__.__name__,
            text=self._text
        )

    @property
    def text(self) -> str:
        self._check_not_discarded()
        return self._text

    @text.setter
    def text(self, value: str):
        self._check_not_discarded()
        self._text = value
        self._increment_version()


class AggregateRating:
    # TODO check how to best implement this
    def __init__(self, rating_count: int, rating_value: float):
        pass


class Recipe(Entity):

    def __init__(self, recipe_id: uuid.UUID, recipe_version: int, name: str, description: str, vendor_id: str,
                 prep_time: timedelta, cook_time: timedelta, total_time: timedelta, url: RecipeURL,
                 images: List[ImageURL], ingredients: List[Ingredient], aggregate_rating: AggregateRating,
                 category: category_aggregate.Category, vendor: vendor_aggregate.Vendor, language: Language):
        super().__init__(recipe_id, recipe_version)
        self._name = name
        self._description = description
        self._vendor_id = vendor_id
        self._prep_time = prep_time
        self._cook_time = cook_time
        self._total_time = total_time
        self._url = url
        self._images = images
        self._ingredients = ingredients
        self._aggregate_rating = aggregate_rating
        self._category = category
        self._vendor = vendor
        self._language = language
        self._matches: List[match_aggregate.Match] = []

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

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        self._name = value
        self._increment_version()

    @property
    def description(self) -> str:
        self._check_not_discarded()
        return self._description

    @description.setter
    def description(self, value: str):
        self._check_not_discarded()
        self._description = value
        self._increment_version()

    @property
    def vendor_id(self) -> str:
        self._check_not_discarded()
        return self._vendor_id

    @vendor_id.setter
    def vendor_id(self, value: str):
        self._check_not_discarded()
        self._vendor_id = value
        self._increment_version()

    @property
    def prep_time(self) -> timedelta:
        self._check_not_discarded()
        return self._prep_time

    @prep_time.setter
    def prep_time(self, value: timedelta):
        self._check_not_discarded()
        self._prep_time = value
        self._increment_version()

    @property
    def cook_time(self) -> timedelta:
        self._check_not_discarded()
        return self._cook_time

    @cook_time.setter
    def cook_time(self, value: timedelta):
        self._check_not_discarded()
        self._cook_time = value
        self._increment_version()

    @property
    def total_time(self) -> timedelta:
        self._check_not_discarded()
        return self._total_time

    @total_time.setter
    def total_time(self, value: timedelta):
        self._check_not_discarded()
        self._total_time = value
        self._increment_version()

    @property
    def url(self) -> RecipeURL:
        self._check_not_discarded()
        return self._url

    @url.setter
    def url(self, value: RecipeURL):
        self._check_not_discarded()
        self._url = value
        self._increment_version()

    @property
    def images(self) -> List[ImageURL]:
        self._check_not_discarded()
        return self._images

    @images.setter
    def images(self, value: List[ImageURL]):
        self._check_not_discarded()
        self._images = value
        self._increment_version()

    @property
    def ingredients(self) -> List[Ingredient]:
        self._check_not_discarded()
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value: List[Ingredient]):
        self._check_not_discarded()
        self._ingredients = value
        self._increment_version()

    @property
    def aggregate_rating(self) -> AggregateRating:
        self._check_not_discarded()
        return self._aggregate_rating

    @aggregate_rating.setter
    def aggregate_rating(self, value: AggregateRating):
        self._check_not_discarded()
        self._aggregate_rating = value
        self._increment_version()

    @property
    def category(self) -> category_aggregate.Category:
        self._check_not_discarded()
        return self._category

    @category.setter
    def category(self, value: category_aggregate.Category):
        self._check_not_discarded()
        self._category = value
        self._increment_version()

    @property
    def vendor(self) -> vendor_aggregate.Vendor:
        self._check_not_discarded()
        return self._vendor

    @vendor.setter
    def vendor(self, value: vendor_aggregate.Vendor):
        self._check_not_discarded()
        self._vendor = value
        self._increment_version()

    @property
    def language(self) -> Language:
        self._check_not_discarded()
        return self._language

    @language.setter
    def language(self, value: Language):
        self._check_not_discarded()
        self._language = value
        self._increment_version()

    @property
    def matches(self) -> List[match_aggregate.Match]:
        self._check_not_discarded()
        return self._matches

    @matches.setter
    def matches(self, value: List[match_aggregate.Match]):
        self._check_not_discarded()
        self._matches = value
        self._increment_version()

    def add_match(self, match: match_aggregate.Match):
        self._check_not_discarded()
        self._matches.append(match)
        self._increment_version()

    def remove_match(self, match: match_aggregate.Match):
        self._check_not_discarded()
        self._matches.remove(match)  # TODO error handling: raises ValueError
        self._increment_version()

    def delete(self):
        for match in self._matches:
            match.delete()
        for image in self._images:
            image.delete()
        for ingredient in self._ingredients:
            ingredient.delete()
        super().delete()
