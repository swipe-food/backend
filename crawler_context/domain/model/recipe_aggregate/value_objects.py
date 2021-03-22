from common.domain.model_base import Immutable
from common.exceptions import InvalidValueError


class RecipeCategory(Immutable):

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise InvalidValueError(self, 'category name must be a string')

        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._name == other._name

    def __str__(self):
        return f"Recipe Category '{self._name}'"


class Ingredient(Immutable):

    def __init__(self, text: str):
        if not isinstance(text, str):
            raise ValueError('ingredient text must be a sting')
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    def __str__(self) -> str:
        return f'{self._text}'


class Author(Immutable):
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise InvalidValueError(self, 'name must be a string')

        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._name == other._name

    def __str__(self):
        return f"Recipe Author '{self._name}'"
