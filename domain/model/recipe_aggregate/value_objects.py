import re

from domain.model.common_aggregate import URL
from domain.model.immutable import Immutable


class RecipeURL(URL):

    def __init__(self, url: str, vendor_pattern: str):
        super().__init__(url)
        self.validate_vendor_pattern(url, vendor_pattern)

    @classmethod
    def validate_vendor_pattern(cls, url: str, vendor_pattern: str):
        cls.validate(url)
        regex = re.compile(vendor_pattern)
        if not regex.search(url):
            raise ValueError(f"Invalid {cls.__class__.__name__} '{url}' for Vendor pattern {vendor_pattern}")


class Ingredient(Immutable):

    def __init__(self, text: str):
        if not isinstance(text, str):
            raise ValueError('ingredient text must be a sting')
        self._text = text

    @property
    def text(self) -> str:
        return self._text

    def __str__(self) -> str:
        return f'{self._text}'


class AggregateRating(Immutable):

    def __init__(self, rating_count: int, rating_value: float):
        if not isinstance(rating_count, int):
            raise ValueError('rating count must be an int')

        if not isinstance(rating_value, float):
            raise ValueError('rating value must be a float')

        if rating_value < 0:
            raise ValueError('rating count cannot be less than 0')

        if not 0 <= rating_value <= 5:
            raise ValueError('rating value has to be between 0 and 5')

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
