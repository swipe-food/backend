from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe


class AbstractBaseScraper(ABC):

    def __init__(self, soup: BeautifulSoup):
        self._soup = soup

    @abstractmethod
    def get_recipe(self) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def get_categories(self) -> Category:
        raise NotImplementedError

    @property
    def soup(self):
        return self._soup
