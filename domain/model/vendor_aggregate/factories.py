from datetime import datetime
from typing import List

from domain.model.common_aggregate import URL, Language
from domain.model.vendor_aggregate.entities import Vendor


def create_vendor(name: str, description: str, url: str, is_active: bool, date_last_crawled: datetime,
                  languages: List[Language], recipe_pattern: str) -> Vendor:
    return Vendor(
        name=name,
        description=description,
        url=URL(url),
        is_active=is_active,
        date_last_crawled=date_last_crawled,
        languages=languages,
        recipe_pattern=recipe_pattern
    )
