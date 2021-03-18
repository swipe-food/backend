from datetime import datetime

from plugins.crawler.scrapers import ChefkochScraper, ParsedRecipeOverviewItem
from plugins.crawler.test_utils import parsed_recipe_sample, load_sample_website


class TestChefkochScraper:

    def test_parse_recipe(self):
        soup = load_sample_website('recipe.html')
        parsed_recipe = ChefkochScraper.parse_recipe(soup=soup)
        assert parsed_recipe == parsed_recipe_sample

    def test_parse_recipe_overview(self):
        soup = load_sample_website('recipe_overview.html')
        parsed_recipe_overview = ChefkochScraper.parse_recipe_overview(soup=soup)
        assert len(parsed_recipe_overview) == 30
        for recipe in parsed_recipe_overview:
            assert isinstance(recipe, ParsedRecipeOverviewItem)
            assert isinstance(recipe.name, str)
            assert isinstance(recipe.url, str)
            assert isinstance(recipe.date_published, datetime)

    def test_parse_categories(self):
        soup = load_sample_website('categories.html')
        parsed_categories = ChefkochScraper.parse_categories(soup=soup)
        assert len(parsed_categories) == 182
        for category in parsed_categories:
            assert isinstance(category.name, str)
            assert isinstance(category.url, str)
