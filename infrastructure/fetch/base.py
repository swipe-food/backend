from __future__ import annotations

from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import List, Generator

from bs4 import BeautifulSoup


class AbstractFetcher(ABC):

    @abstractmethod
    def fetch(self, urls: List[str]) -> Generator[List[FetchResult], None, None]:
        raise NotImplementedError


@dataclass
class FetchResult:
    url: str
    status: int
    html: BeautifulSoup
