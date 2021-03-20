import inspect
from abc import ABC


class Immutable(ABC):
    def __setattr__(self, name, value):
        caller = inspect.stack()[1][3]
        if caller == '__init__':
            return super().__setattr__(name, value)
        raise AttributeError("can't set attribute for an immutable object")

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'
