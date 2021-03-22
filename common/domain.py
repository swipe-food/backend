from __future__ import annotations

import inspect
import re
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, List
from urllib.parse import urlparse

from common.exceptions import DiscardEntityError


class Entity(ABC):
    """The base class of all entities.

    Attributes:
        id: A unique identifier
        version: An integer version
        discarded: True if this entity should no longer be used. otherwise False

    """

    def __init__(self):
        self._id = uuid.uuid4()
        self._version = 1
        self._discarded = False
        self._date_created = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def version(self):
        return self._version

    @property
    def discarded(self):
        return self._discarded

    @property
    def date_created(self):
        return self._date_created

    def delete(self):
        self._discarded = True

    def _check_not_discarded(self):
        if self._discarded:
            raise DiscardEntityError(f"Attempt to use {repr(self)}")

    def _increment_version(self):
        self._version += 1

    def _get(self, value: Any) -> Any:
        self._check_not_discarded()
        return value

    def _set(self, set_callback: Callable):
        self._check_not_discarded()
        set_callback()
        self._increment_version()

    def __repr__(self) -> str:
        return "discarded={d!r}, id={id!r}, version={v!r}".format(
            d=self._discarded,
            id=self._id.__str__(),
            v=self._version)


class Immutable(ABC):
    """All inheriting subclasses are immutable, only the constructor can set attributes"""

    def replace(self, *args, **kwargs) -> Immutable:
        return self.__class__.__init__(
            *args,
            **{attribute: value if value is None else getattr(self, attribute) for attribute, value in kwargs.items()}
        )

    def __setattr__(self, name, value):
        caller = inspect.stack()[1][3]
        if caller == '__init__':
            return super().__setattr__(name, value)
        raise AttributeError("can't set attribute for an immutable object")

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'


class AbstractBaseRepository(ABC):

    def __init__(self, db_connection):
        self._db_connection = db_connection

    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Entity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: Entity):
        raise NotImplementedError


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