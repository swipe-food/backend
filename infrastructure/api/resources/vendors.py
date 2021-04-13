from infrastructure.api.resources.base import BaseResource


# TODO: request & response models (with marshmallow for example)


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
