from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Tuple

from bs4 import BeautifulSoup

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe


class AbstractBaseScraper(ABC):

    @abstractmethod
    def scrape_recipe(self, soup: BeautifulSoup, url: str) -> Recipe:
        raise NotImplementedError

    def scrape_recipe_overview(self, soup: BeautifulSoup) -> List[Tuple[str, datetime]]:
        raise NotImplementedError

    @abstractmethod
    def scrape_categories(self, soup: BeautifulSoup) -> List[Category]:
        raise NotImplementedError
