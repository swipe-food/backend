from __future__ import annotations

import uuid
from typing import List

from domain.exceptions import InvalidValueException
from domain.model.category_like_aggregate import create_category_like, CategoryLike
from domain.model.match_aggregate import Match
from domain.model.user_aggregate import User, create_user
from domain.repositories.category import AbstractCategoryRepository
from domain.repositories.category_like import AbstractCategoryLikeRepository
from domain.repositories.language import AbstractLanguageRepository
from domain.repositories.recipe import AbstractRecipeRepository
from domain.repositories.user import AbstractUserRepository
from domain.services.user import AbstractUserService


def create_user_service(user_repo: AbstractUserRepository, recipe_repo: AbstractRecipeRepository,
                        language_repo: AbstractLanguageRepository,
                        category_like_repo: AbstractCategoryLikeRepository,
                        category_repo: AbstractCategoryRepository) -> UserService:
    if not isinstance(user_repo, AbstractUserRepository):
        raise InvalidValueException(UserService, 'user_repo must be a AbstractUserRepository')
    if not isinstance(recipe_repo, AbstractRecipeRepository):
        raise InvalidValueException(UserService, 'recipe_repo must be a AbstractRecipeRepository')
    if not isinstance(language_repo, AbstractLanguageRepository):
        raise InvalidValueException(UserService, 'language_repo must be a AbstractLanguageRepository')
    if not isinstance(category_like_repo, AbstractCategoryLikeRepository):
        raise InvalidValueException(UserService, 'category_like_repo must be a AbstractCategoryLikeRepository')
    if not isinstance(category_repo, AbstractCategoryRepository):
        raise InvalidValueException(UserService, 'category_repo must be a AbstractCategoryRepository')
    return UserService(user_repo=user_repo, recipe_repo=recipe_repo, language_repo=language_repo,
                       category_like_repo=category_like_repo, category_repo=category_repo)


class UserService(AbstractUserService):

    def __init__(self, user_repo: AbstractUserRepository, recipe_repo: AbstractRecipeRepository,
                 language_repo: AbstractLanguageRepository, category_like_repo: AbstractCategoryLikeRepository,
                 category_repo: AbstractCategoryRepository):
        self._user_repo = user_repo
        self._recipe_repo = recipe_repo
        self._language_repo = language_repo
        self._category_like_repo = category_like_repo
        self._category_repo = category_repo

    def get_by_id(self, user_id: uuid.UUID) -> User:
        return self._user_repo.get_by_id(user_id)

    def get_by_email(self, email: str) -> User:
        return self._user_repo.get_by_email(email)

    def get_all(self, limit: int) -> List[User]:
        return self._user_repo.get_all(limit)

    def get_matches(self, user_id: uuid.UUID, limit: int) -> List[Match]:
        user = self.get_by_id(user_id)
        return list(user.matches)

    def get_liked_categories(self, user_id: uuid.UUID, limit: int) -> List[CategoryLike]:
        user = self.get_by_id(user_id)
        return list(user.liked_categories)

    def confirm(self, user_id: uuid.UUID):
        user = self.get_by_id(user_id)
        user.is_confirmed = True
        self._user_repo.update(user)

    def add_seen_recipe(self, user_id: uuid.UUID, recipe_id: uuid.UUID):
        user = self.get_by_id(user_id)
        recipe = self._recipe_repo.get_by_id(recipe_id)
        user.add_seen_recipe(recipe)
        self._user_repo.add_seen_recipe(user, recipe)

    def add(self, entity_data: dict) -> User:
        user = create_user(user_id=uuid.uuid4(),
                           name=entity_data['name'],
                           first_name=entity_data['first_name'],
                           email=entity_data['email'],
                           is_confirmed=False,
                           date_last_login=entity_data['date_last_login'],
                           liked_categories=[],
                           matches=[],
                           seen_recipes=[],
                           languages=[]
                           )
        self._user_repo.add(user)
        return user

    def update(self, user_id: uuid.UUID, entity_data: dict) -> User:
        user = self.get_by_id(user_id)
        if 'name' in entity_data:
            user.name = entity_data['name']
        if 'first_name' in entity_data:
            user.first_name = entity_data['first_name']
        if 'email' in entity_data:
            user.email = entity_data['email']
            user.is_confirmed = False
        if 'date_last_login' in entity_data:
            user.date_last_login = entity_data['date_last_login']

        self._user_repo.update(user)
        return user

    def delete(self, entity_id: uuid.UUID):
        user = self.get_by_id(entity_id)
        user.delete()
        self._user_repo.delete(user)

    def add_language(self, user_id: uuid.UUID, language_id: uuid.UUID):
        user = self.get_by_id(user_id)
        language = self._language_repo.get_by_id(language_id)
        user.add_language(language)
        self._user_repo.add_language(user, language)

    def remove_language(self, user_id: uuid.UUID, language_id: uuid.UUID):
        user = self.get_by_id(user_id)
        language = self._language_repo.get_by_id(language_id)
        self._user_repo.remove_language(user, language)

    def add_category_like(self, user_id: uuid.UUID, category_id: uuid.UUID):
        user = self.get_by_id(user_id)
        category = self._category_repo.get_by_id(category_id)
        category_like = create_category_like(category_like_id=uuid.uuid4(),
                                             user=user,
                                             category=category,
                                             views=0,
                                             matches=0)
        user.add_category_like(category_like)
        self._category_like_repo.add(category_like)

    def remove_category_like(self, user_id: uuid.UUID, category_like_id: uuid.UUID):
        user = self.get_by_id(user_id)
        category_like = self._category_like_repo.get_by_id(category_like_id)
        if category_like.id not in [user_liked.id for user_liked in user.liked_categories]:
            raise InvalidValueException(raiser=self,
                                        message="Category Like does not belong to the specified User")  # TODO other exception
        self._category_like_repo.delete(category_like)
