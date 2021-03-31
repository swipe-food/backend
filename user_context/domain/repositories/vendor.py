from abc import abstractmethod, ABC
from typing import List

from common.domain.repositories import AbstractQueryBaseRepository
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.vendor_aggregate import Vendor


class AbstractVendorRepository(AbstractQueryBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self, vendor: Vendor) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, vendor: Vendor) -> List[Recipe]:
        raise NotImplementedError
