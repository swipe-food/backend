"""This file contains common domain model classes and functions"""
import uuid
from abc import ABC
from datetime import datetime


def create_entity_id() -> uuid.UUID:
    return uuid.uuid4()


class Entity(ABC):
    """The base class of all entities.

    Attributes:
        id: A unique identifier
        version: An integer version
        discarded: True if this entity should no longer be used. otherwise False

    """

    def __init__(self, entity_id: uuid.UUID, entity_version: int):
        self._id = entity_id
        self._version = entity_version
        self._discarded = False
        self._date_created = datetime.now()

    def __repr__(self) -> str:
        return "discarded={d!r}, id={id!r}, version={v!r}".format(
            d=self._discarded,
            id=self._id.__str__(),
            v=self._version)

    def _increment_version(self):
        self._version += 1

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

    def _check_not_discarded(self):
        if self._discarded:
            raise DiscardEntityError(f"Attempt to use {repr(self)}")

    def delete(self):
        self._discarded = True


class DiscardEntityError(Exception):
    """Raised when an attempt is made to use a discarded entity"""
    pass  # TODO extract Exceptions to own package in domain


class Language(Entity):

    def __init__(self, language_id: uuid.UUID, language_version: int, name: str, code: str):
        super().__init__(language_id, language_version)
        self._name = name
        self._code = code

    def __str__(self) -> str:
        return f"Language '{self._name}' with code '{self._code}'"

    def __repr__(self) -> str:
        return "{c}({s}, name={name!r}, {code!r})".format(
            c=self.__class__.__name__,
            s=super().__repr__(),
            name=self._name,
            code=self._code,
        )

    @property
    def name(self) -> str:
        self._check_not_discarded()
        return self._name

    @property
    def code(self) -> str:
        """The language code according to ISO 639-1"""
        self._check_not_discarded()
        return self._code


class URL:
    VALID_SCHEMES = ['http', 'https']

    @classmethod
    def from_text(cls, url: str):
        # TODO validate
        scheme, domain, resource, parameters = url, url, url, url
        return cls(scheme, domain, resource, parameters)

    def __init__(self, scheme: str, domain: str, resource: str, parameters: str):
        self._parts = (scheme, domain, resource, parameters)

    def __str__(self) -> str:
        return f'{self._parts[0]}//{self._parts[1]}{self._parts[2]}{self._parts[3]}'

    def __repr__(self) -> str:
        return '{c}(url={url!r})'.format(
            c=self.__class__.__name__,
            url=self.__str__(),
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return NotImplemented  # TODO check if this approach is good
        return self._parts == o._parts

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    def replace(self, scheme: str = None, domain: str = None, resource: str = None, parameters: str = None):
        return URL(scheme=scheme or self._parts[0],
                   domain=domain or self._parts[1],
                   resource=resource or self._parts[2],
                   parameters=parameters or self._parts[3])