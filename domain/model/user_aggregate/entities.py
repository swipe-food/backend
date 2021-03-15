from __future__ import annotations
from datetime import datetime

import uuid
from typing import List

from domain.model.match_aggregate.entities import Match
from domain.model.category_aggregate.entities import Category
from domain.model.common_aggregate import Entity, Language
from domain.model.recipe_aggregate.entities import Recipe
from domain.model.user_aggregate.value_objects import EMail


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
        self._matches: List[Match] = []
        self._seen_recipes: List[Recipe] = []

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

    def add_language(self, language: Language):
        self._check_not_discarded()
        self._languages.append(language)
        self._increment_version()

    def remove_language(self, language: Language):
        self._check_not_discarded()
        self._languages.remove(language)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def liked_categories(self) -> List[CategoryLike]:
        self._check_not_discarded()
        return self._liked_categories

    def add_liked_category(self, liked_category: CategoryLike):
        self._check_not_discarded()
        self._liked_categories.append(liked_category)
        self._increment_version()

    def remove_liked_category(self, liked_category: CategoryLike):
        self._check_not_discarded()
        self._liked_categories.remove(liked_category)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def matches(self) -> List[Match]:
        self._check_not_discarded()
        return self._matches

    def add_match(self, match: Match):
        self._check_not_discarded()
        self._matches.append(match)
        self._increment_version()

    def remove_match(self, match: Match):
        self._check_not_discarded()
        self._matches.remove(match)  # TODO error handling: raises ValueError
        self._increment_version()

    @property
    def seen_recipes(self) -> List[Recipe]:
        self._check_not_discarded()
        return self._seen_recipes

    def add_seen_recipe(self, recipe: Recipe):
        self._check_not_discarded()
        self._seen_recipes.append(recipe)
        self._increment_version()

    def remove_seen_recipe(self, recipe: Recipe):
        self._check_not_discarded()
        self._seen_recipes.remove(recipe)  # TODO error handling: raises ValueError
        self._increment_version()

    def delete(self):
        for liked_category in self._liked_categories:
            liked_category.delete()
        for match in self._matches:
            match.delete()
        super().delete()


class CategoryLike(Entity):
    """A user can like a category.

    Attributes:
        views: Total amount of viewed recipes for the category
        matches: Total amount of matches between the user and the viewed recipes for the category
    """

    def __init__(self, liked_category_id: uuid.UUID, liked_category_version: int, user: User,
                 category: Category, views: int, matches: int):
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

    @property
    def category(self) -> Category:
        self._check_not_discarded()
        return self._category

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