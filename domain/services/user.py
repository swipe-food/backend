import uuid
from abc import abstractmethod, ABC
from typing import List

from domain.model.category_like_aggregate import CategoryLike
from domain.model.match_aggregate import Match
from domain.model.user_aggregate import User
from domain.services.base import AbstractQueryService, AbstractCommandService


class AbstractUserService(AbstractQueryService, AbstractCommandService, ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_matches(self, user_id: uuid.UUID, limit: int) -> List[Match]:
        raise NotImplementedError

    @abstractmethod
    def get_liked_categories(self, user_id: uuid.UUID, limit: int) -> List[CategoryLike]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, limit: int) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def confirm(self, user_id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def add_seen_recipe(self, user_id: uuid.UUID, recipe_id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def add_language(self, user_id: uuid.UUID, language_id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def remove_language(self, user_id: uuid.UUID, language_id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def add_category_like(self, user_id: uuid.UUID, category_id: uuid.UUID):
        raise NotImplementedError

    @abstractmethod
    def remove_category_like(self, user_id: uuid.UUID, category_like_id: uuid.UUID):
        raise NotImplementedError
