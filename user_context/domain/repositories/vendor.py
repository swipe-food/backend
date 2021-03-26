from abc import abstractmethod
from typing import List

from common.domain.repositories import AbstractBaseRepository
from user_context.domain.model.category_aggregate import Category
from common.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.vendor_aggregate import Vendor


class AbstractVendorRepository(AbstractBaseRepository):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self, vendor: Vendor) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, vendor: Vendor) -> List[Recipe]:
        raise NotImplementedError
