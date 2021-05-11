from flask import request

from domain.services.vendor import AbstractVendorService
from infrastructure.api.decorators import dump_schema
from infrastructure.api.resources.base import BaseResource
from infrastructure.api.schemas import VendorSchema, RecipeSchema


class VendorNameResource(BaseResource):
    path = '/name/<string:vendor_name>'

    @staticmethod
    @dump_schema(schema=VendorSchema())
    def get(vendor_name):
        svc: AbstractVendorService = request.services['vendor']

        return svc.get_by_name(vendor_name)


class VendorResource(BaseResource):
    path = '/<string:vendor_id>'

    @staticmethod
    @dump_schema(schema=VendorSchema())
    def get(vendor_id):
        svc: AbstractVendorService = request.services['vendor']

        return svc.get_by_id(vendor_id)


class VendorRecipesResource(BaseResource):
    path = '/<string:vendor_id>/recipes'

    @staticmethod
    @dump_schema(schema=RecipeSchema(many=True))
    def get(vendor_id):
        svc: AbstractVendorService = request.services['vendor']

        return svc.get_recipes(vendor_id)


class VendorsResource(BaseResource):
    path = '/'

    @staticmethod
    @dump_schema(schema=VendorSchema(many=True))
    def get():
        svc: AbstractVendorService = request.services['vendor']
        limit = request.args.get("limit")

        return svc.get_all(limit), 200
