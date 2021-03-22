from abc import abstractmethod
from typing import List

from common.domain import AbstractBaseRepository
from user_context.domain.model.category_aggregate import Category
from user_context.domain import Recipe
from user_context.domain import User
from user_context.domain import Vendor


class AbstractCategoryRepository(AbstractBaseRepository):

    @abstractmethod
    def get_by_name(self, category_name: str) -> Category:
        raise NotImplementedError

    def get_liked_users(self, category: Category) -> List[User]:
        raise NotImplementedError

    def get_recipes(self, category: Category) -> List[Recipe]:
        raise NotImplementedError

    def get_vendors(self, category: Category) -> List[Vendor]:
        raise NotImplementedError
