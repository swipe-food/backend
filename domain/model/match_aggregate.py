import uuid
from datetime import datetime

from domain.model.common_aggregate import Entity


class Match(Entity):

    def __init__(self, match_id: uuid.UUID, match_version: int, user, recipe, timestamp: datetime,
                 is_seen_by_user: bool,
                 is_active: bool):
        super().__init__(match_id, match_version)
        self._user = user
        self._recipe = recipe
        self._timestamp = timestamp
        self._is_seen_by_user = is_seen_by_user
        self._is_active = is_active

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

    @property
    def user(self):
        self._check_not_discarded()
        return self._user

    @user.setter
    def user(self, value):
        self._check_not_discarded()
        self._user = value
        self._increment_version()

    @property
    def recipe(self):
        self._check_not_discarded()
        return self._recipe

    @recipe.setter
    def recipe(self, value):
        self._check_not_discarded()
        self._recipe = value
        self._increment_version()

    @property
    def timestamp(self) -> datetime:
        self._check_not_discarded()
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: datetime):
        self._check_not_discarded()
        self._timestamp = value
        self._increment_version()

    @property
    def is_seen_by_user(self):
        self._check_not_discarded()
        return self._is_seen_by_user

    @is_seen_by_user.setter
    def is_seen_by_user(self, value):
        self._check_not_discarded()
        self._is_seen_by_user = value
        self._increment_version()

    @property
    def is_active(self):
        self._check_not_discarded()
        return self._is_active

    @is_active.setter
    def is_active(self, value):
        self._check_not_discarded()
        self._is_active = value
        self._increment_version()

    def delete(self):
        self._user.remove_match(self)
        self._recipe.remove_match(self)
        super().delete()
