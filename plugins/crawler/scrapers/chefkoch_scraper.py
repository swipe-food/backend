from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from plugins.crawler.scrapers.base_scraper import AbstractBaseScraper


class ChefkochScraper(AbstractBaseScraper):
    def get_recipe(self) -> Recipe:
        pass

    def get_categories(self) -> Category:
        pass
