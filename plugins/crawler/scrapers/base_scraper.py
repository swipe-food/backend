from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup

from plugins.crawler.scrapers.data import ParsedRecipe, ParsedCategory


class AbstractBaseScraper(ABC):

    def __init__(self, soup: BeautifulSoup):
        self._soup = soup

    @abstractmethod
    def parse_recipe(self) -> ParsedRecipe:
        raise NotImplementedError

    @abstractmethod
    def parse_categories(self) -> List[ParsedCategory]:
        raise NotImplementedError

    @property
    def soup(self):
        return self._soup
