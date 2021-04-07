from __future__ import annotations

from typing import List


class URLQueue:

    def __init__(self, urls: List[str] = None):
        self.urls = urls.copy() if urls else list()

    def add(self, value: str or List[str]):
        if isinstance(value, str):
            self.urls.append(value)
        elif isinstance(value, list):
            for item in value:
                self.add(item)
        else:
            raise ValueError(f'unsupported type {type(value)} for {self}')

    def clear(self):
        self.urls.clear()

    def is_empty(self):
        return len(self) == 0

    def __add__(self, other) -> URLQueue:
        self.add(other)
        return self

    def __len__(self) -> int:
        return len(self.urls)

    def __bool__(self):
        return not self.is_empty()

    def __iter__(self):
        return self

    def __next__(self):
        if not self.is_empty():
            return self.urls.pop(0)
        raise StopIteration

    def __repr__(self) -> str:
        return f'URLQueue({len(self)} urls)'
