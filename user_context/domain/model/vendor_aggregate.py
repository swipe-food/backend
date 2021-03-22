from __future__ import annotations

from typing import List, Tuple

from common.domain.model_base import Entity
from common.domain.value_objects import Language, URL
from common.exceptions import InvalidValueError
from user_context.domain.model.category_aggregate import Category


def create_vendor(name: str, description: str, url: str, is_active: bool, recipe_pattern: str,
                  languages: List[Language], categories: List[Category]) -> Vendor:
    if not isinstance(name, str):
        raise InvalidValueError(Vendor, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueError(Vendor, 'description must be a string')

    if not isinstance(languages, list):
        raise InvalidValueError(Vendor, 'languages must be a list of Language instances')

    if not isinstance(categories, list):
        raise InvalidValueError(Vendor, 'categories must be a list of Language instances')

    vendor_url_object = URL(url=url)

    return Vendor(
        name=name,
        description=description,
        url=vendor_url_object,
        is_active=is_active,
        recipe_pattern=recipe_pattern,
        languages=languages,
        categories=categories,
    )


class Vendor(Entity):

    def __init__(self, name: str, description: str, url: URL, is_active: bool, recipe_pattern: str,
                 languages: List[Language], categories: List[Category]):
        super().__init__()

        self._name = name
        self._description = description
        self._url = url

        self.is_active = is_active
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
            raise InvalidValueError(self, 'is_active must be a bool')
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
            raise InvalidValueError(self, 'recipe pattern must be a string')
        self._recipe_pattern = pattern
        self._increment_version()

    @property
    def languages(self) -> Tuple[Language]:
        self._check_not_discarded()
        return tuple(self._languages)

    def add_language(self, language: Language):
        self._check_not_discarded()
        if not isinstance(language, Language):
            raise InvalidValueError(self, 'language must be a Language instance')
        self._languages.append(language)
        self._increment_version()

    def remove_language(self, language: Language):
        self._check_not_discarded()
        if not isinstance(language, Language):
            raise InvalidValueError(self, 'language must be a Language instance')
        self._languages.remove(language)
        self._increment_version()

    @property
    def categories(self) -> Tuple[Category]:
        self._check_not_discarded()
        return tuple(self._categories)

    def add_category(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise InvalidValueError(self, 'category must be a Category instance')
        self._categories.append(category)
        self._increment_version()

    def remove_category(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise InvalidValueError(self, 'category must be a Category instance')
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
