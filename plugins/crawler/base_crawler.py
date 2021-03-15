from abc import ABC, abstractmethod
from typing import List

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe


class AbstractBaseCrawler(ABC):

    @classmethod
    @abstractmethod
    def get_categories_page(cls) -> Category:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def get_new_recipes(cls) -> List[Recipe]:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def crawl_recipe(cls, recipe_url: str) -> Recipe:
        raise NotImplemented
