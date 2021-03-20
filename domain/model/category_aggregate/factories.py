from domain.model.category_aggregate.entities import Category
from domain.model.vendor_aggregate import Vendor


def create_category(name: str, vendor: Vendor) -> Category:
    return Category(name=name, vendor=vendor)
