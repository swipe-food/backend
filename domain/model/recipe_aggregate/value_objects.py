import re

from domain.model.common_aggregate import URL


class RecipeURL(URL):

    @classmethod
    def from_text_with_pattern(cls, url: str, vendor_pattern: str):
        scheme, netloc, path, query = cls._parse(url)

        if scheme not in cls.VALID_SCHEMES or netloc == '':
            raise ValueError(f'Invalid {cls.__class__.__name__} {url}')

        regex = re.compile(vendor_pattern)
        if not regex.search(url):
            raise ValueError(f"Invalid {cls.__class__.__name__} '{url}' for Vendor pattern {vendor_pattern}")
        return cls(scheme, netloc, path, query)

    def __init__(self, scheme: str, netloc: str, path: str, query: str):
        super().__init__(scheme, netloc, path, query)

    def replace(self, scheme: str = None, netloc: str = None, path: str = None, query: str = None):
        return RecipeURL(scheme=scheme or self._parts[0],
                         netloc=netloc or self._parts[1],
                         path=path or self._parts[2],
                         query=query or self._parts[3])


class AggregateRating:

    @classmethod
    def from_values(cls, rating_count: int, rating_value: float):
        if rating_value < 0:
            raise ValueError(f'{cls.__class__.__name__} rating count cannot be less than 0')
        if not 0 <= rating_value <= 5:
            raise ValueError(f'{cls.__class__.__name__} rating value has to be between 0 and 5')
        return cls(rating_count, rating_value)

    def __init__(self, rating_count: int, rating_value: float):
        self._rating_count = rating_count
        self._rating_value = rating_value

    def __str__(self) -> str:
        return f'Rating Count: {self._rating_count}, Rating Value: {self._rating_value}'

    def __repr__(self) -> str:
        return '{c}(rating_count={rating_count!r}, rating_value={rating_value!r})'.format(
            c=self.__class__.__name__,
            rating_count=self._rating_count,
            rating_value=self._rating_value,
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return NotImplemented
        return self._rating_count == o.rating_count and self._rating_value == o.rating_count

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    @property
    def rating_value(self):
        return self._rating_value

    @property
    def rating_count(self):
        return self._rating_count

    def replace(self, rating_count: int = None, rating_value: float = None):
        return AggregateRating(rating_count=rating_count or self._rating_count,
                               rating_value=rating_value or self._rating_value)
