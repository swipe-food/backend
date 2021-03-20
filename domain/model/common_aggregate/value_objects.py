from urllib.parse import urlparse

from domain.model.immutable import Immutable


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
            raise ValueError('url must be a string')

        parsed_url = urlparse(url)
        if parsed_url.scheme not in cls.VALID_PROTOCOLS or parsed_url.netloc == '':
            raise ValueError(f'Invalid {cls.__class__.__name__} {url}')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._value == other._value

    def __str__(self) -> str:
        return self._value


class Language(Immutable):

    def __init__(self, name: str, code: str):
        if not isinstance(name, str):
            raise ValueError('language name must be a string')

        if not isinstance(code, str):
            raise ValueError('language code must be a string')

        if len(code) != 2:
            raise ValueError('Language Acronym must have a length of 2')

        self._name = name
        self._code = code

    @property
    def name(self) -> str:
        return self._name

    @property
    def code(self) -> str:
        """The language code according to ISO 639-1"""
        return self._code

    def __str__(self) -> str:
        return f"Language '{self._name}' with code '{self._code}'"
