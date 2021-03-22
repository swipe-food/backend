from datetime import datetime

from common.domain import Entity
from domain.model.recipe_aggregate import Recipe


class Match(Entity):

    def __init__(self, user, recipe: Recipe, timestamp: datetime, is_seen_by_user: bool, is_active: bool):
        super().__init__()

        if not user.__class__.__name__ == 'User':  # can't import User because of circular imports
            raise ValueError('user must be an User instance')

        if not isinstance(recipe, Recipe):
            raise ValueError('recipe must be a Recipe instance')

        if not isinstance(timestamp, datetime):
            raise ValueError('timestamp must be a datetime')

        self._user = user
        self._recipe = recipe
        self._timestamp = timestamp

        self.is_seen_by_user = is_seen_by_user
        self.is_active = is_active

    @property
    def user(self):
        # type: () -> User
        self._check_not_discarded()
        return self._user

    @property
    def recipe(self) -> Recipe:
        self._check_not_discarded()
        return self._recipe

    @property
    def timestamp(self) -> datetime:
        self._check_not_discarded()
        return self._timestamp

    @property
    def is_seen_by_user(self) -> bool:
        self._check_not_discarded()
        return self._is_seen_by_user

    @is_seen_by_user.setter
    def is_seen_by_user(self, value: bool):
        self._check_not_discarded()
        if not isinstance(value, bool):
            raise ValueError('is_seen_by_user must be a bool')
        self._is_seen_by_user = value
        self._increment_version()

    @property
    def is_active(self) -> bool:
        self._check_not_discarded()
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool):
        self._check_not_discarded()
        if not isinstance(value, bool):
            raise ValueError('is_active must be a bool')
        self._is_active = value
        self._increment_version()

    def delete(self):
        self._user.remove_match(self)
        super().delete()

    def __str__(self) -> str:
        return f"Match between '{self._user.email.__str__()}' and '{self._recipe.name}'"

    def __repr__(self) -> str:
        return "{c}({s}, timestamp={timestamp!r}, {user}, {recipe})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            timestamp=self._timestamp,
            user=self._user.__repr__(),
            recipe=self._recipe.__repr__()
        )
