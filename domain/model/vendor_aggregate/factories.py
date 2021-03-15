from datetime import datetime
from typing import List

from domain.model.common_aggregate.entities import Language
from domain.model.common_aggregate.factories import create_entity_id
from domain.model.common_aggregate.value_objects import URL
from domain.model.vendor_aggregate.entities import Vendor


def create_vendor(version: int, name: str, description: str, url: str, is_active: bool, date_last_crawled: datetime,
                  languages: List[Language], recipe_pattern: str) -> Vendor:
    return Vendor(vendor_id=create_entity_id(),
                  vendor_version=version,
                  name=name,
                  description=description,
                  url=URL.from_text(url),
                  is_active=is_active,
                  date_last_crawled=date_last_crawled,
                  languages=languages,
                  recipe_pattern=recipe_pattern)
