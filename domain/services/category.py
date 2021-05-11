import uuid
from abc import abstractmethod
from typing import List

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.services.base import AbstractBaseService


class AbstractCategoryService(AbstractBaseService):

    @abstractmethod
    def get_by_id(self, category_id: uuid.UUID) -> Category:
        raise NotImplementedError

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
    def get_recipes(self, category_id: uuid.UUID) -> List[Recipe]:
        raise NotImplementedError
