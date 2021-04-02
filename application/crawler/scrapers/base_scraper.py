from abc import ABC, abstractmethod
from typing import List

from bs4 import BeautifulSoup

from application.crawler.scrapers.data_classes import ParsedRecipe, ParsedCategory, ParsedRecipeOverviewItem


class AbstractBaseScraper(ABC):

    @classmethod
    @abstractmethod
    def parse_recipe(cls, soup: BeautifulSoup) -> ParsedRecipe:
        raise NotImplementedError

    @classmethod
    def parse_recipe_overview(cls, soup: BeautifulSoup) -> List[ParsedRecipeOverviewItem]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def parse_categories(cls, soup: BeautifulSoup) -> List[ParsedCategory]:
        raise NotImplementedError
