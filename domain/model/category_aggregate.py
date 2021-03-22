from __future__ import annotations

from common.domain import Entity


def create_category(name: str) -> Category:
    return Category(name=name)


class Category(Entity):

    def __init__(self, name: str):
        super().__init__()

        self.name = name
        self._likes = 0

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise ValueError('category name must be a string')
        self._name = value
        self._increment_version()

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

    def delete(self):
        super().delete()

    def __str__(self) -> str:
        return f"Category '{self._name}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
        )
