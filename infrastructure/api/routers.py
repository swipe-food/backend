from abc import ABC
from typing import List

from flask_restplus import Namespace

from infrastructure.api.resources import BaseResource
from infrastructure.api.resources.category import CategoryRecipesResource, CategoriesResource, CategoryNameResource, CategoryResource, CategoryUsersResource
from infrastructure.api.resources.status import StatusResource
from infrastructure.api.resources.vendor import VendorResource, VendorsResource, VendorRecipesResource, VendorNameResource


class AbstractRouter(Namespace, ABC):
    name: str
    description: str
    router_resources: List[BaseResource]

    def __init__(self, *args, **kwargs):
        super().__init__(name=self.name, description=self.description, *args, **kwargs)
        self._add_resources()

    def _add_resources(self):
        for resource in self.router_resources:
            self.add_resource(resource, resource.path)


class StatusRouter(AbstractRouter):
    name = 'status'
    description = 'Status Information about the API'
    router_resources = [StatusResource]


class VendorRouter(AbstractRouter):
    name = 'vendors'
    description = "Information about the Vendors. Only GET Resources, since the API shouldn't modify the Vendor Entities."
    router_resources = [VendorResource, VendorNameResource, VendorsResource, VendorRecipesResource]


class CategoryRouter(AbstractRouter):
    name = 'categories'
    description = "Information about the Categories. Only GET Resources, since the API shouldn't modify the Category Entities."
    router_resources = [CategoryResource, CategoryNameResource, CategoriesResource, CategoryRecipesResource, CategoryUsersResource]
