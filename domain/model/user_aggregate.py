from __future__ import annotations

from datetime import datetime
import uuid
from typing import List

from domain.model import category_aggregate, match_aggregate
from domain.model.common_aggregate import Entity, Language


class EMail:

    @classmethod
    def from_text(cls, address: str):
        if not '@' in address:
            raise ValueError("EMail address must contain '@'")
        local_part, _, domain_part = address.partition('@')
        return cls(local_part, domain_part)

    def __init__(self, local_part: str, domain_part: str):
        self._parts = (local_part, domain_part)

    def __str__(self) -> str:
        return '@'.join(self._parts)

    def __repr__(self) -> str:
        return 'EMail(local_part={!r}, domain_part={!r})'.format(*self._parts)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, EMail):
            return NotImplemented  # TODO check if this approach is good
        return self._parts == o._parts

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    @property
    def local(self):
        return self._parts[0]

    @property
    def domain(self):
        return self._parts[1]

    def replace(self, local_part: str = None, domain_part: str = None):
        return EMail(local_part=local_part or self._parts[0],
                     domain_part=domain_part or self._parts[1])


class CategoryLike(Entity):
    """A user can like a category.

    Attributes:
        views: Total amount of viewed recipes for the category
        matches: Total amount of matches between the user and the viewed recipes for the category
    """

    def __init__(self, liked_category_id: uuid.UUID, liked_category_version: int, user: User,
                 category: category_aggregate.Category, views: int, matches: int):
        super().__init__(liked_category_id, liked_category_version)
        self._user = user
        self._category = category
        self._views = views
        self._matches = matches

        self._user.add_liked_category(self)
        self._category.add_like(self)

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

    @property
    def user(self) -> User:
        self._check_not_discarded()
        return self._user

    @user.setter
    def user(self, value: User):
        self._check_not_discarded()
        self._user = value
        self._increment_version()

    @property
    def category(self) -> category_aggregate.Category:
        self._check_not_discarded()
        return self._category

    @category.setter
    def category(self, value: category_aggregate.Category):
        self._check_not_discarded()
        self._category = value
        self._increment_version()

    @property
    def views(self) -> int:
        self._check_not_discarded()
        return self._views

    @views.setter
    def views(self, value: int):
        self._check_not_discarded()
        self._views = value
        self._increment_version()

    @property
    def matches(self) -> int:
        self._check_not_discarded()
        return self._matches

    @matches.setter
    def matches(self, value: int):
        self._check_not_discarded()
        self._matches = value
        self._increment_version()

    def delete(self):
        self._category.remove_like(self)
        self._user.remove_liked_category(self)
        super().delete()


class User(Entity):

    def __init__(self, user_id: uuid.UUID, user_version: int, name: str, first_name: str, is_confirmed: bool,
                 date_last_login: datetime, email: EMail, languages: List[Language]):
        super().__init__(user_id, user_version)
        self._name = name
        self._first_name = first_name
        self._is_confirmed = is_confirmed
        self._date_last_login = date_last_login
        self._email = email
        self._languages = languages
        self._liked_categories: List[CategoryLike] = []
        self._matches: List[match_aggregate.Match] = []

    def __str__(self) -> str:
        return f"User with Name '{self._name}' and EMail '{self._email.__str__()}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, email={email!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            email=self._email.__str__()
        )

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        self._name = value
        self._increment_version()

    @property
    def first_name(self) -> str:
        self._check_not_discarded()
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._check_not_discarded()
        self._first_name = value
        self._increment_version()

    @property
    def is_confirmed(self) -> bool:
        self._check_not_discarded()
        return self._is_confirmed

    @is_confirmed.setter
    def is_confirmed(self, value: bool):
        self._check_not_discarded()
        self._is_confirmed = value
        self._increment_version()

    @property
    def date_last_login(self) -> datetime:
        self._check_not_discarded()
        return self._date_last_login

    @date_last_login.setter
    def date_last_login(self, value: datetime):
        self._check_not_discarded()
        self._date_last_login = value
        self._increment_version()

    @property
    def email(self) -> EMail:
        self._check_not_discarded()
        return self._email

    @email.setter
    def email(self, value: EMail):
        self._check_not_discarded()
        self._email = value
        self._increment_version()

    @property
    def languages(self) -> List[Language]:
        self._check_not_discarded()
        return self._languages

    @languages.setter
    def languages(self, value: List[Language]):
        self._check_not_discarded()
        self._languages = value
        self._increment_version()

    def add_language(self, language: Language):
        self._check_not_discarded()
        self._languages.append(language)
        self._increment_version()

    def remove_language(self, language: Language):
        self._check_not_discarded()
        self._languages.remove(language)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def liked_categories(self) -> List[Language]:
        self._check_not_discarded()
        return self._liked_categories

    @liked_categories.setter
    def liked_categories(self, value: List[CategoryLike]):
        self._check_not_discarded()
        self._liked_categories = value
        self._increment_version()

    def add_liked_category(self, liked_category: CategoryLike):
        self._check_not_discarded()
        self._liked_categories.append(liked_category)
        self._increment_version()

    def remove_liked_category(self, liked_category: CategoryLike):
        self._check_not_discarded()
        self._liked_categories.remove(liked_category)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def matches(self) -> List[match_aggregate.Match]:
        self._check_not_discarded()
        return self._matches

    @matches.setter
    def matches(self, value: List[match_aggregate.Match]):
        self._check_not_discarded()
        self._matches = value
        self._increment_version()

    def add_match(self, match: match_aggregate.Match):
        self._check_not_discarded()
        self._matches.append(match)
        self._increment_version()

    def remove_match(self, match: match_aggregate.Match):
        self._check_not_discarded()
        self._matches.remove(match)  # TODO error handling: raises ValueError
        self._increment_version()

    def delete(self):
        for liked_category in self._liked_categories:
            liked_category.delete()
        for match in self._matches:
            match.delete()
        super().delete()
