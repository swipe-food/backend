from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

from domain.model.category_aggregate import Category
from domain.model.common_aggregate import Language
from domain.model.entity import Entity
from domain.model.match_aggregate import Match
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate.value_objects import EMail


class User(Entity):

    def __init__(self, name: str, first_name: str, is_confirmed: bool,
                 date_last_login: datetime, email: EMail, languages: List[Language]):
        super().__init__()

        self.name = name
        self.first_name = first_name
        self.is_confirmed = is_confirmed
        self.date_last_login = date_last_login
        self.email = email
        self._languages: List[Language] = []
        self._liked_categories: List[CategoryLike] = []
        self._matches: List[Match] = []
        self._seen_recipes: List[Recipe] = []

        if not isinstance(languages, list):
            raise ValueError('languages must be a list of Language instances')

        for language in languages:
            self.add_language(language)

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @name.setter
    def name(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise ValueError('name must be a string')
        self._name = value
        self._increment_version()

    @property
    def first_name(self) -> str:
        self._check_not_discarded()
        return self._first_name

    @first_name.setter
    def first_name(self, value: str):
        self._check_not_discarded()
        if not isinstance(value, str):
            raise ValueError('first name must be a string')
        self._first_name = value
        self._increment_version()

    @property
    def is_confirmed(self) -> bool:
        self._check_not_discarded()
        return self._is_confirmed

    @is_confirmed.setter
    def is_confirmed(self, value: bool):
        self._check_not_discarded()
        if not isinstance(value, bool):
            raise ValueError('is_confirmed must be a bool')
        self._is_confirmed = value
        self._increment_version()

    @property
    def date_last_login(self) -> datetime:
        self._check_not_discarded()
        return self._date_last_login

    @date_last_login.setter
    def date_last_login(self, value: datetime):
        self._check_not_discarded()
        if not isinstance(value, datetime):
            raise ValueError('last login date must be a datetime')
        self._date_last_login = value
        self._increment_version()

    @property
    def email(self) -> EMail:
        self._check_not_discarded()
        return self._email

    @email.setter
    def email(self, value: EMail):
        self._check_not_discarded()
        if not isinstance(value, EMail):
            raise ValueError('email must be a EMail instance')
        self._email = value
        self._increment_version()

    @property
    def languages(self) -> Tuple[Language]:
        self._check_not_discarded()
        return tuple(self._languages)

    def add_language(self, language: Language):
        self._check_not_discarded()
        if not isinstance(language, Language):
            raise ValueError('language must be a Language instance')
        self._languages.append(language)
        self._increment_version()

    def remove_language(self, language: Language):
        self._check_not_discarded()
        if not isinstance(language, Language):
            raise ValueError('language must be a Language instance')
        self._languages.remove(language)
        self._increment_version()

    @property
    def liked_categories(self) -> Tuple[CategoryLike]:
        self._check_not_discarded()
        return tuple(self._liked_categories)

    def add_liked_category(self, liked_category: CategoryLike):
        self._check_not_discarded()
        if not isinstance(liked_category, CategoryLike):
            raise ValueError('liked_category must be a CategoryLike instance')
        self._liked_categories.append(liked_category)
        self._increment_version()

    def remove_liked_category(self, liked_category: CategoryLike):
        self._check_not_discarded()
        if not isinstance(liked_category, CategoryLike):
            raise ValueError('liked_category must be a CategoryLike instance')
        self._liked_categories.remove(liked_category)
        self._increment_version()

    @property
    def matches(self) -> Tuple[Match]:
        self._check_not_discarded()
        return tuple(self._matches)

    def add_match(self, match: Match):
        self._check_not_discarded()
        if not isinstance(match, Match):
            raise ValueError('match must be a Match instance')
        self._matches.append(match)
        self._increment_version()

    def remove_match(self, match: Match):
        self._check_not_discarded()
        if not isinstance(match, Match):
            raise ValueError('match must be a Match instance')
        self._matches.remove(match)
        self._increment_version()

    @property
    def seen_recipes(self) -> Tuple[Recipe]:
        self._check_not_discarded()
        return tuple(self._seen_recipes)

    def add_seen_recipe(self, recipe: Recipe):
        self._check_not_discarded()
        if not isinstance(recipe, Recipe):
            raise ValueError('recipe must be a Recipe instance')
        self._seen_recipes.append(recipe)
        self._increment_version()

    def remove_seen_recipe(self, recipe: Recipe):
        self._check_not_discarded()
        if not isinstance(recipe, Recipe):
            raise ValueError('recipe must be a Recipe instance')
        self._seen_recipes.remove(recipe)
        self._increment_version()

    def delete(self):
        for liked_category in self._liked_categories:
            liked_category.delete()
        for match in self._matches:
            match.delete()
        super().delete()

    def __str__(self) -> str:
        return f"User with Name '{self._name}' and EMail '{self._email.__str__()}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, email={email!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            email=self._email.__str__()
        )


class CategoryLike(Entity):
    """A user can like a category.

    Attributes:
        views: Total amount of viewed recipes for the category
        matches: Total amount of matches between the user and the viewed recipes for the category
    """

    def __init__(self, user: User, category: Category, views: int, matches: int):
        super().__init__()

        if not isinstance(user, User):
            raise ValueError('user must be a User instance')

        if not isinstance(category, Category):
            raise ValueError('category must be a Category instance')

        if not isinstance(views, int):
            raise ValueError('views must be an int')

        if not isinstance(matches, int):
            raise ValueError('matches must be an int')

        self._user = user
        self._category = category
        self._views = views
        self._matches = matches

        self._user.add_liked_category(self)
        self._category.add_like(self)

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
        self._category.remove_like(self)
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
