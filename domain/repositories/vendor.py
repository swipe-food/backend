from abc import abstractmethod, ABC
from typing import List

from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.base import AbstractBaseRepository


class AbstractVendorRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def add_languages(self, vendor: Vendor):
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, vendor: Vendor) -> List[Recipe]:
        raise NotImplementedError
