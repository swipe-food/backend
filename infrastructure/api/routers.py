from abc import ABC
from typing import List

from flask_restplus import Namespace

from infrastructure.api.resources.base import BaseResource
from infrastructure.api.resources.vendors import VendorResource


class AbstractRouter(Namespace, ABC):
    name: str
    description: str
    api_resources: List[BaseResource]

    def __init__(self, *args, **kwargs):
        super().__init__(name=self.name, description=self.description, *args, **kwargs)
        self._add_resources()

    def _add_resources(self):
        for resource in self.api_resources:
            self.add_resource(
                resource,
                resource.path
            )


class VendorRouter(AbstractRouter):
    name = 'vendors'
    description = 'test description'
    api_resources = [VendorResource]
