from common.domain import Immutable


class RecipeCategory(Immutable):

    def __init__(self, name: str):
        if not isinstance(name, str):
            raise ValueError('recipe category name must be a string')

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


class Author(Immutable):
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise ValueError('author name must be a string')

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
