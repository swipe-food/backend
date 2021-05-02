from flask import request

from domain.services.vendor import AbstractVendorService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import vendor_schema, vendor_list_schema, recipe_list_schema


class VendorNameResource(BaseResource):
    path = '/name/<string:vendor_name>'

    @staticmethod
    @dump_schema(schema=vendor_schema)
    def get(vendor_name):
        svc: AbstractVendorService = request.services['vendor']
        vendor = svc.get_by_name(vendor_name)

        return vendor


class VendorResource(BaseResource):
    path = '/<string:vendor_id>'

    @staticmethod
    @dump_schema(schema=vendor_schema)
    def get(vendor_id):
        svc: AbstractVendorService = request.services['vendor']
        vendor = svc.get_by_id(vendor_id)

        return vendor


class VendorRecipesResource(BaseResource):
    path = '/<string:vendor_id>/recipes'

    @staticmethod
    @dump_schema(schema=recipe_list_schema)
    def get(vendor_id):
        svc: AbstractVendorService = request.services['vendor']
        recipes = svc.get_recipes(vendor_id)

        return recipes


class VendorsResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=vendor_list_schema)
    def get():
        svc: AbstractVendorService = request.services['vendor']
        limit = request.args.get("limit")
        vendors = svc.get_all(limit)

        return vendors
