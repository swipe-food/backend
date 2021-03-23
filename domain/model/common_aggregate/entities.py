import uuid
from abc import ABC
from datetime import datetime

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
            name=self.name,
            code=self.code,
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
