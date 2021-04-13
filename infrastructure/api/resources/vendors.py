from infrastructure.api.resources.base import BaseResource


class VendorResource(BaseResource):
    path = '/<string:vendor_id>'

    @staticmethod
    def get(vendor_id):
        return {'id': vendor_id}


class VendorsResource(BaseResource):
    path = '/'

    @staticmethod
    def get():
        pass
