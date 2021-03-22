from __future__ import annotations

from uuid import UUID

from common.domain.model_base import Entity
from common.domain.value_objects import URL
from common.exceptions import InvalidValueError


def create_category(category_id: UUID, name: str, url: str) -> Category:
    if not isinstance(name, str):
        raise InvalidValueError(Category, 'name must be a string')

    if not isinstance(url, str):
        raise InvalidValueError(Category, 'url must be a string')

    url_object = URL(url=url)

    return Category(category_id=category_id, name=name, url=url_object)


class Category(Entity):

    def __init__(self, category_id: UUID, name: str, url: URL):
        super().__init__(category_id)

        self.name = name
        self.url = url

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, category_name: str):
        self._check_not_discarded()
        if not isinstance(category_name, str):
            raise InvalidValueError(self, 'name must be a string')
        self._name = category_name
        self._increment_version()

    @property
    def url(self) -> URL:
        self._check_not_discarded()
        return self._url

    @url.setter
    def url(self, category_url: URL):
        self._check_not_discarded()
        if not isinstance(category_url, URL):
            raise InvalidValueError(self, 'url must be a URL instance')
        self._url = category_url
        self._increment_version()
