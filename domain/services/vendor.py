import uuid
from abc import abstractmethod, ABC
from typing import List

from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.services.base import AbstractQueryService


class AbstractVendorService(AbstractQueryService, ABC):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, limit: int) -> List[Vendor]:
        raise NotImplementedError

    @abstractmethod
    def get_recipes(self, vendor_id: uuid.UUID) -> List[Recipe]:
        raise NotImplementedError
