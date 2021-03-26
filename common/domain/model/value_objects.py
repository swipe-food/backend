import re
from urllib.parse import urlparse

from common.domain.model.base import Immutable
from common.exceptions import InvalidValueError


class URL(Immutable):
    VALID_PROTOCOLS = ['http', 'https']

    def __init__(self, url: str):
        self.validate(url)
        self._value = url

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def validate(cls, url: str):
        if not isinstance(url, str):
            raise InvalidValueError(cls, 'url must be a string')

        parsed_url = urlparse(url)
        if parsed_url.scheme not in cls.VALID_PROTOCOLS or parsed_url.netloc == '':
            raise InvalidValueError(
                cls, f'Invalid {cls.__class__.__name__} {url}')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __str__(self) -> str:
        return self._value


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


class AggregateRating(Immutable):

    def __init__(self, rating_count: int, rating_value: float):
        if not isinstance(rating_count, int):
            raise InvalidValueError(
                self, 'rating count must be an int')

        if not isinstance(rating_value, float):
            raise InvalidValueError(self, 'rating value must be a float')

        if rating_value < 0:
            raise InvalidValueError(self, 'rating count cannot be less than 0')

        if not 0 <= rating_value <= 5:
            raise InvalidValueError(self, 'rating value has to be between 0 and 5')

        self._rating_count = rating_count
        self._rating_value = rating_value

    @property
    def rating_count(self) -> int:
        return self._rating_count

    @property
    def rating_value(self) -> float:
        return self._rating_value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._rating_count == other.rating_count and self._rating_value == other.rating_count

    def __str__(self) -> str:
        return f'Rating Count: {self._rating_count}, Rating Value: {self._rating_value}'


class Author(Immutable):
    def __init__(self, name: str):
        if not isinstance(name, str):
            raise InvalidValueError(self, 'name must be a string')

        self._name = name

    @property
    def name(self) -> str:
        return self._name

    def __eq__(self, other: object):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._name == other._name

    def __str__(self):
        return f"Recipe Author '{self._name}'"
