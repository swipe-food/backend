from __future__ import annotations

from uuid import UUID

from common.domain.model.base import Entity
from common.exceptions import InvalidValueException


def create_ingredient(ingredient_id: UUID, text: str) -> Ingredient:
    return Ingredient(ingredient_id=ingredient_id, text=text)


class Ingredient(Entity):

    def __init__(self, ingredient_id: UUID, text: str):
        super().__init__(ingredient_id)

        self.text = text

    @property
    def text(self):
        self._check_not_discarded()
        return self._text

    @text.setter
    def text(self, text: str):
        self._check_not_discarded()
        if not isinstance(text, str):
            raise InvalidValueException(self, 'text must be a string')
        self._text = text
        self._increment_version()

    def __str__(self):
        return f"Ingredient '{self._text}'"
