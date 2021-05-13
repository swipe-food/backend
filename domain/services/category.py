import uuid
from abc import abstractmethod, ABC
from typing import List

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.services.base import AbstractQueryService


class AbstractCategoryService(AbstractQueryService, ABC):

    @abstractmethod
    def get_by_name(self, category_name: str) -> Category:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, limit: int) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def get_liked_users(self, category_id: uuid.UUID) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, category_id: uuid.UUID, limit: int or None) -> List[Recipe]:
        raise NotImplementedError
