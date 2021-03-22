from abc import abstractmethod
from typing import List

from common.domain import AbstractBaseRepository
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.model.vendor_aggregate import Vendor


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
