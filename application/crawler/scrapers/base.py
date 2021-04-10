from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List

from bs4 import BeautifulSoup

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe


class AbstractBaseScraper(ABC):

    @abstractmethod
    def scrape_recipe(self, soup: BeautifulSoup, url: str, category: Category) -> Recipe:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def scrape_recipe_overview(soup: BeautifulSoup, category: Category) -> List[RecipeOverviewItem]:
        raise NotImplementedError

    @abstractmethod
    def scrape_categories(self, soup: BeautifulSoup) -> List[Category]:
        raise NotImplementedError


@dataclass(eq=True, frozen=True)
class RecipeOverviewItem:
    url: str
    category: Category
    published: datetime
