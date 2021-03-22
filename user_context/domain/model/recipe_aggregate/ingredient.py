from uuid import UUID

from common.domain.model_base import Entity
from common.exceptions import InvalidValueError


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
            raise InvalidValueError(self, 'text must be a string')
        self._text = text
        self._increment_version()

    def __str__(self):
        return f"Ingredient '{self._text}'"
