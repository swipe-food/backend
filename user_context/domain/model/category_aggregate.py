from __future__ import annotations

from uuid import UUID

from common.domain.model_base import Entity
from common.exceptions import InvalidValueError

def create_category(category_id: UUID, name: str, vendor) -> Category:
    return Category(category_id=category_id, name=name, vendor=vendor)


class Category(Entity):

    def __init__(self, category_id: UUID, name: str, vendor):
        super().__init__(category_id)

        self._name = name
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
            raise InvalidValueError(self, 'name must be a string')
        self._name = value
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
