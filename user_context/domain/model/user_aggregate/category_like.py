from uuid import UUID

from common.domain.model_base import Entity
from common.exceptions import InvalidValueError
from user_context.domain.model.category_aggregate import Category


class CategoryLike(Entity):
    """A user can like a category.

    Attributes:
        views: Total amount of viewed recipes for the category
        matches: Total amount of matches between the user and the viewed recipes for the category
    """

    def __init__(self, category_like_id: UUID, user, category: Category, views: int, matches: int):
        super().__init__(category_like_id)

        if not user.__class__.__name__ == 'User':  # can't import User because of circular imports
            raise InvalidValueError(self, 'user must be a User instance')

        if not isinstance(category, Category):
            raise InvalidValueError(self, 'category must be a Category instance')

        if not isinstance(views, int):
            raise InvalidValueError(self, 'views must be an int')

        if not isinstance(matches, int):
            raise InvalidValueError(self, 'matches must be an int')

        self._user = user
        self._category = category
        self._views = views
        self._matches = matches

        self._user.add_category_like(self)
        self._category.add_like()

    @property
    def user(self):
        # type: () -> User
        self._check_not_discarded()
        return self._user

    @property
    def category(self) -> Category:
        self._check_not_discarded()
        return self._category

    @property
    def views(self) -> int:
        self._check_not_discarded()
        return self._views

    def add_view(self):
        self._check_not_discarded()
        self._views += 1
        self._increment_version()

    @property
    def matches(self) -> int:
        self._check_not_discarded()
        return self._matches

    def add_match(self):
        self._check_not_discarded()
        self._matches += 1
        self._increment_version()

    def delete(self):
        self._category.remove_like()
        self._user.remove_liked_category(self)
        super().delete()

    def __str__(self) -> str:
        return f"LikedCategory for User '{self._user.email}' and Category {self._category.name}"

    def __repr__(self) -> str:
        return "{c}({s}, views={views!r}, matches={matches!r}, {user}, {category})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            views=self._views,
            matches=self._matches,
            user=self._user.__repr__(),
            category=self._category.__repr__(),
        )