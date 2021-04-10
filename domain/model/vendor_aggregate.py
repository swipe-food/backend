from __future__ import annotations

from datetime import datetime
from typing import List, Tuple
from uuid import UUID

from domain.exceptions import InvalidValueException
from domain.model.base import Entity
from domain.model.category_aggregate import Category
from domain.model.common_value_objects import URL
from domain.model.language_aggregate import Language


def create_vendor(vendor_id: UUID, name: str, description: str, url: str, is_active: bool, recipe_pattern: str,
                  categories_link: str, date_last_crawled: datetime,
                  language: Language, categories: List[Category]) -> Vendor:
    if not isinstance(name, str):
        raise InvalidValueException(Vendor, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueException(Vendor, 'description must be a string')

    if not isinstance(url, str):
        raise InvalidValueException(Vendor, 'url must be a string')

    if not isinstance(language, Language):
        raise InvalidValueException(Vendor, 'language must be a Language instance')

    if not isinstance(categories, list):
        raise InvalidValueException(Vendor, 'categories must be a list of Language instances')

    vendor_url_object = URL(url=url)

    return Vendor(
        vendor_id=vendor_id,
        name=name,
        description=description,
        url=vendor_url_object,
        is_active=is_active,
        recipe_pattern=recipe_pattern,
        categories_link=categories_link,
        date_last_crawled=date_last_crawled,
        language=language,
        categories=categories,

    )


class Vendor(Entity):

    def __init__(self, vendor_id: UUID, name: str, description: str, url: URL, is_active: bool, recipe_pattern: str,
                 date_last_crawled: datetime, categories_link: str, language: Language, categories: List[Category]):
        super().__init__(vendor_id)

        self._name = name
        self._description = description
        self._url = url

        self.is_active = is_active
        self.recipe_pattern = recipe_pattern
        self.date_last_crawled = date_last_crawled
        self.categories_link = categories_link
        self._language = language

        self._categories: List[Category] = []

        for category in categories:
            self.add_category(category)

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @property
    def description(self) -> str:
        self._check_not_discarded()
        return self._description

    @property
    def url(self) -> URL:
        self._check_not_discarded()
        return self._url

    @property
    def is_active(self) -> bool:
        self._check_not_discarded()
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._check_not_discarded()
        if not isinstance(value, bool):
            raise InvalidValueException(self, 'is_active must be a bool')
        self._is_active = value
        self._increment_version()

    @property
    def recipe_pattern(self) -> str:
        self._check_not_discarded()
        return self._recipe_pattern

    @recipe_pattern.setter
    def recipe_pattern(self, pattern: str):
        self._check_not_discarded()
        if not isinstance(pattern, str):
            raise InvalidValueException(self, 'recipe pattern must be a string')
        self._recipe_pattern = pattern
        self._increment_version()

    @property
    def date_last_crawled(self) -> datetime:
        self._check_not_discarded()
        return self._date_last_crawled

    @date_last_crawled.setter
    def date_last_crawled(self, value: datetime):
        self._check_not_discarded()
        if not isinstance(value, datetime):
            raise InvalidValueException(self, 'date_last_crawled must be a datetime')
        self._date_last_crawled = value
        self._increment_version()

    @property
    def categories_link(self) -> str:
        self._check_not_discarded()
        return self._categories_link

    @categories_link.setter
    def categories_link(self, link: str):
        self._check_not_discarded()
        if not isinstance(link, str):
            raise InvalidValueException(self, 'categories_link must be a string')
        self._categories_link = link
        self._increment_version()

    @property
    def language(self) -> Language:
        self._check_not_discarded()
        return self._language

    @property
    def categories(self) -> Tuple[Category]:
        self._check_not_discarded()
        return tuple(self._categories)

    def add_category(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise InvalidValueException(self, 'category must be a Category instance')
        self._categories.append(category)
        self._increment_version()

    def remove_category(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise InvalidValueException(self, 'category must be a Category instance')
        self._categories.remove(category)
        self._increment_version()

    def delete(self):
        for category in self._categories:
            category.delete()
        super().delete()

    def __str__(self) -> str:
        return f"Vendor '{self._name}' with URL '{self._url}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, is_active={is_active!r}, count_categories={count_categories!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            is_active=self._is_active,
            count_categories=len(self._categories)
        )
