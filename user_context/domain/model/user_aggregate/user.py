from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

from more_itertools import one

from common.domain.model_base import Entity
from common.domain.value_objects import Language
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate import EMail, CategoryLike
from user_context.domain.model.user_aggregate.recipe_match import Match


class User(Entity):

    def __init__(self, name: str, first_name: str, is_confirmed: bool, date_last_login: datetime,
                 email: EMail, liked_categories: List[Category], matches: List[Recipe],
                 seen_recipes: List[Recipe], languages: List[Language]):
        super().__init__()

        self.name = name
        self.first_name = first_name
        self.is_confirmed = is_confirmed
        self.date_last_login = date_last_login
        self.email = email

        self._liked_categories: List[CategoryLike] = []
        self._matches: List[Match] = []
        self._seen_recipes: List[Recipe] = []
        self._languages: List[Language] = []

        for liked_category in liked_categories:
            self.add_category_like(liked_category)

        for match in matches:
            self.add_match(match)

        for seen_recipe in seen_recipes:
            self.add_seen_recipe(seen_recipe)

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

    def add_category_like(self, category: Category, views: int = 0, matches: int = 0):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise ValueError('liked_category must be a CategoryLike instance')
        category_like = CategoryLike(user=self, category=category, views=views, matches=matches)
        self._liked_categories.append(category_like)
        self._increment_version()

    def remove_category_like(self, category: Category):
        self._check_not_discarded()
        if not isinstance(category, Category):
            raise ValueError('category must be a Category instance')
        category_like_to_remove = one(
            filter(lambda liked_category: liked_category.category.id == category.id, self._liked_categories)
        )
        self._liked_categories.remove(category_like_to_remove)
        self._increment_version()

    @property
    def matches(self) -> Tuple[Match]:
        self._check_not_discarded()
        return tuple(self._matches)

    def add_match(self, matched_recipe: Recipe):
        self._check_not_discarded()
        if not isinstance(matched_recipe, Recipe):
            raise ValueError('matched_recipe must be a Recipe instance')
        match = Match(user=self, recipe=matched_recipe, timestamp=datetime.now(), is_seen_by_user=False, is_active=True)
        self._matches.append(match)
        self._increment_version()

    def remove_match(self, matched_recipe: Recipe):
        self._check_not_discarded()
        if not isinstance(matched_recipe, Recipe):
            raise ValueError('matched_recipe must be a Recipe instance')
        match = one(
            filter(lambda match_item: match_item.recipe.id == matched_recipe.id, self._matches)
        )
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
