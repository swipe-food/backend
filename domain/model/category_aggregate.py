from __future__ import annotations

from uuid import UUID

from common.exceptions import InvalidValueException
from domain.model.base import Entity
from domain.model.common_value_objects import URL


def create_category(category_id: UUID, name: str, url: str, vendor) -> Category:
    if not vendor.__class__.__name__ == 'Vendor':
        raise InvalidValueException(Category, 'vendor must be a Vendor instance')

    url_object = URL(url=url)
    return Category(category_id=category_id, name=name, url=url_object, vendor=vendor)


class Category(Entity):

    def __init__(self, category_id: UUID, name: str, url: URL, vendor):
        super().__init__(category_id)

        self.name = name
        self.url = url

        self._vendor = vendor
        self._likes = 0  # set by CategoryLike instances

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise InvalidValueException(self, 'name must be a string')
        self._name = value
        self._increment_version()

    @property
    def url(self) -> URL:
        self._check_not_discarded()
        return self._url

    @url.setter
    def url(self, category_url: URL):
        self._check_not_discarded()
        if not isinstance(category_url, URL):
            raise InvalidValueException(self, 'url must be a URL instance')
        self._url = category_url
        self._increment_version()

    @property
    def vendor(self):
        # type: () -> Vendor
        self._check_not_discarded()
        return self._vendor

    @property
    def likes(self) -> int:
        self._check_not_discarded()
        return self._likes

    def add_like(self):
        self._check_not_discarded()
        self._likes += 1
        self._increment_version()

    def remove_like(self):
        self._check_not_discarded()
        self._likes -= 1
        self._increment_version()

    def __str__(self) -> str:
        return f"Category '{self._name}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
        )
