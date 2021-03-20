from __future__ import annotations

import inspect
from abc import ABC


class Immutable(ABC):
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
