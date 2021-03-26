import re

from common.domain.value_objects import URL
from common.exceptions import InvalidValueError


class RecipeURL(URL):

    def __init__(self, url: str, vendor_pattern: str):
        super().__init__(url)
        self.validate_vendor_pattern(url, vendor_pattern)

    @classmethod
    def validate_vendor_pattern(cls, url: str, vendor_pattern: str):
        cls.validate(url)
        regex = re.compile(vendor_pattern)
        if not regex.search(url):
            raise InvalidValueError(cls, f"invalid url '{url}' for Vendor pattern {vendor_pattern}")