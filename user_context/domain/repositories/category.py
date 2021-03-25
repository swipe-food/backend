from abc import abstractmethod, ABC
from typing import List

from common.domain.repositories import AbstractBaseRepository
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate import User
from user_context.domain.model.vendor_aggregate import Vendor


class AbstractCategoryRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, category_name: str) -> Category:
        raise NotImplementedError

    @abstractmethod
    def get_liked_users(self, category: Category) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, category: Category) -> List[Recipe]:
        raise NotImplementedError

    @abstractmethod
    def get_vendors(self, category: Category) -> List[Vendor]:
        raise NotImplementedError
