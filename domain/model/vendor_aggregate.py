from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

from common.domain import Entity
from domain.model.category_aggregate import Category
from domain.model.common_value_objects import URL, Language


def create_vendor(name: str, description: str, url: str, is_active: bool, date_last_crawled: datetime,
                  languages: List[Language], categories: List[Category], recipe_pattern: str) -> Vendor:
    if not isinstance(name, str):
        raise ValueError('vendor name must be a string')

    if not isinstance(description, str):
        raise ValueError('description must be a string')

    if not isinstance(languages, list):
        raise ValueError('languages must be a list of Language instances')

    if not isinstance(categories, list):
        raise ValueError('categories must be a list of Language instances')

    vendor_url_object = URL(url=url)

    return Vendor(
        name=name,
        description=description,
        url=vendor_url_object,
        is_active=is_active,
        date_last_crawled=date_last_crawled,
        languages=languages,
        categories=categories,
        recipe_pattern=recipe_pattern,
    )


class Vendor(Entity):

    def __init__(self, name: str, description: str, url: URL, is_active: bool, date_last_crawled: datetime,
                 languages: List[Language], categories: List[Category], recipe_pattern: str):
        super().__init__()

        self._name = name
        self._description = description
        self._url = url

        self.is_active = is_active
        self.date_last_crawled = date_last_crawled
        self.recipe_pattern = recipe_pattern

        self._languages: List[Language] = []
        self._categories: List[Category] = []

        for language in languages:
            self.add_language(language)

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
            raise ValueError('is_active must be a bool')
        self._is_active = value
        self._increment_version()

    @property
    def date_last_crawled(self) -> datetime:
        self._check_not_discarded()
        return self._date_last_crawled

    @date_last_crawled.setter
    def date_last_crawled(self, value: datetime):
        self._check_not_discarded()
        if not isinstance(value, datetime):
            raise ValueError('date_last_crawled must be a datetime')
        self._date_last_crawled = value
        self._increment_version()

    @property
    def languages(self) -> Tuple[Language]:
        self._check_not_discarded()
        return tuple(self._languages)

    def add_language(self, language: Language):
        self._check_not_discarded()
        if not isinstance(language, Language):
            raise ValueError('language must be a Language instance')
        self._languages.append(language)
        self._increment_version()

    def remove_language(self, language: Language):
        self._check_not_discarded()
        if not isinstance(language, Language):
            raise ValueError('language must be a Language instance')
        self._languages.remove(language)
        self._increment_version()

    @property
    def recipe_pattern(self) -> str:
        self._check_not_discarded()
        return self._recipe_pattern

    @recipe_pattern.setter
    def recipe_pattern(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise ValueError('recipe_pattern must be a string')
        self._recipe_pattern = value
        self._increment_version()

    @property
    def categories(self) -> Tuple[Category]:
        self._check_not_discarded()
        return tuple(self._categories)

    def add_category(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise ValueError('category must be a Category instance')
        self._categories.append(category)
        self._increment_version()

    def remove_category(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise ValueError('category must be a Category instance')
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
