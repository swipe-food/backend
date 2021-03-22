import inspect
import uuid
from abc import ABC
from datetime import datetime
from typing import Any, Callable

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
