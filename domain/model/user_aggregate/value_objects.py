import re

from common.exceptions import InvalidValueException
from domain.model.base import Immutable


class EMail(Immutable):
    VALIDATION_REGEX = "[^@]+@[^@]+\\.[^@]+"

    def __init__(self, email_address: str):
        self.validate(email_address)
        self._value = email_address

    @property
    def value(self) -> str:
        return self._value

    @classmethod
    def validate(cls, email_address: str):
        if not isinstance(email_address, str):
            raise InvalidValueException(cls, 'email address must be a string')

        pattern = re.compile(cls.VALIDATION_REGEX)
        if not pattern.match(email_address):
            raise InvalidValueException(cls, f'invalid email {email_address}')

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, EMail):
            return NotImplemented
        return self._value == other._value

    def __str__(self) -> str:
        return self._value
