from __future__ import annotations

import uuid
from typing import List

from domain.exceptions import InvalidValueException
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.vendor import AbstractVendorRepository
from domain.services.vendor import AbstractVendorService


def create_vendor_service(vendor_repo: AbstractVendorRepository) -> VendorService:
    if not isinstance(vendor_repo, AbstractVendorRepository):
        raise InvalidValueException(VendorService, 'config must be a AppConfig')
    return VendorService(repo=vendor_repo)


class VendorService(AbstractVendorService):

    def __init__(self, repo: AbstractVendorRepository):
        self._repo = repo

    def get_by_id(self, vendor_id: uuid.UUID) -> Vendor:
        return self._repo.get_by_id(vendor_id)

    def get_by_name(self, vendor_name: str) -> Vendor:
        return self._repo.get_by_name(vendor_name)

    def get_all(self, limit: int) -> List[Vendor]:
        return self._repo.get_all(limit)

    def get_recipes(self, vendor_id: uuid.UUID) -> List[Recipe]:
        vendor = self._repo.get_by_id(vendor_id)

        return self._repo.get_recipes(vendor)
