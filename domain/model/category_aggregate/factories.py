from domain.model.category_aggregate.entities import Category
from domain.model.common_aggregate import create_entity_id
from domain.model.vendor_aggregate.entities import Vendor


def create_category(version: int, name: str, vendor: Vendor) -> Category:
    return Category(category_id=create_entity_id(),
                    category_version=version,
                    name=name,
                    vendor=vendor)
