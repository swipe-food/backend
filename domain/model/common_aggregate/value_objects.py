from urllib.parse import urlparse

from domain.model.immutable import Immutable


class URL(Immutable):
    VALID_PROTOCOLS = ['http', 'https']

    def __init__(self, value: str):
        self.validate(value)
        self._value = value

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def validate(cls, url: str) -> bool:
        if not isinstance(url, str):
            raise ValueError('url must be a string')

        parsed_url = urlparse(url)
        if parsed_url.scheme not in cls.VALID_PROTOCOLS or parsed_url.netloc == '':
            raise ValueError(f'Invalid {cls.__class__.__name__} {url}')
        return True

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value
