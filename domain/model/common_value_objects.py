from urllib.parse import urlparse

from common.exceptions import InvalidValueException
from domain.model.base import Immutable


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
            raise InvalidValueException(cls, 'url must be a string')

        parsed_url = urlparse(url)
        if parsed_url.scheme not in cls.VALID_PROTOCOLS or parsed_url.netloc == '':
            raise InvalidValueException(cls, f'Invalid {cls.__class__.__name__} {url}')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __str__(self) -> str:
        return self._value
