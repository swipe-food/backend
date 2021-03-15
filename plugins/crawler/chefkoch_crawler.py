from typing import List

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from plugins.crawler.base_crawler import AbstractBaseCrawler


class ChefkochCrawler(AbstractBaseCrawler):
    @classmethod
    def get_categories_page(cls) -> Category:
        pass

    @classmethod
    def get_new_recipes(cls) -> List[Recipe]:
        pass

    @classmethod
    def crawl_recipe(cls, recipe_url: str) -> Recipe:
        pass
