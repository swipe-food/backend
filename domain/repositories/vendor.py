from abc import abstractmethod, ABC
from typing import List

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.base import AbstractQueryBaseRepository, AbstractCommandBaseRepository


class AbstractVendorRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self, vendor: Vendor) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, vendor: Vendor) -> List[Recipe]:
        raise NotImplementedError
