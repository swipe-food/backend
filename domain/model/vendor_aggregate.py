from __future__ import annotations

from datetime import datetime
import uuid
from typing import List

from domain.model import category_aggregate
from domain.model.common_aggregate import Entity, Language, URL


class Vendor(Entity):

    def __init__(self, vendor_id: uuid.UUID, vendor_version: int, name: str, description: str, url: URL,
                 is_active: bool, date_last_crawled: datetime, languages: List[Language], recipe_pattern: str):
        super().__init__(vendor_id, vendor_version)
        self._name = name
        self._description = description
        self._url = url
        self._is_active = is_active
        self._date_last_crawled = date_last_crawled
        self._languages = languages
        self._recipe_pattern = recipe_pattern
        self._categories: List[category_aggregate.Category] = []

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
    def url(self) -> URL:
        self._check_not_discarded()
        return self._url

    @url.setter
    def url(self, value: URL):
        self._check_not_discarded()
        self._url = value
        self._increment_version()

    @property
    def is_active(self) -> bool:
        self._check_not_discarded()
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._check_not_discarded()
        self._is_active = value
        self._increment_version()

    @property
    def date_last_crawled(self) -> datetime:
        self._check_not_discarded()
        return self._date_last_crawled

    @date_last_crawled.setter
    def date_last_crawled(self, value: datetime):
        self._check_not_discarded()
        self._date_last_crawled = value
        self._increment_version()

    @property
    def languages(self) -> List[Language]:
        self._check_not_discarded()
        return self._languages

    @languages.setter
    def languages(self, value: List[Language]):
        self._check_not_discarded()
        self._languages = value
        self._increment_version()

    def add_language(self, language: Language):
        self._check_not_discarded()
        self._languages.append(language)
        self._increment_version()

    def remove_language(self, language: Language):
        self._check_not_discarded()
        self._languages.remove(language)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def recipe_pattern(self) -> str:
        self._check_not_discarded()
        return self._recipe_pattern

    @recipe_pattern.setter
    def recipe_pattern(self, value: str):
        self._check_not_discarded()
        self._recipe_pattern = value
        self._increment_version()

    @property
    def categories(self) -> List[category_aggregate.Category]:
        self._check_not_discarded()
        return self._categories

    @categories.setter
    def categories(self, value: List[category_aggregate.Category]):
        self._check_not_discarded()
        self._categories = value
        self._increment_version()

    def add_category(self, category: category_aggregate.Category):
        self._check_not_discarded()
        self._categories.append(category)
        self._increment_version()

    def remove_category(self, category: category_aggregate.Category):
        self._check_not_discarded()
        self._categories.remove(category)  # TODO error handling: raises ValueError
        self._increment_version()

    def delete(self):
        for category in self._categories:
            category.delete()
        super().delete()