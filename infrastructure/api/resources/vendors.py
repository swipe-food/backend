from infrastructure.api.resources.base import BaseResource


class VendorResource(BaseResource):
    path = '/<string:vendor_id>'

    def get(self, vendor_id):
        return {'id': vendor_id}
