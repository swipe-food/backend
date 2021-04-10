from datetime import datetime
from unittest.mock import patch

from pytest import fixture

from application.crawler.scrapers import ChefkochScraper, RecipeOverviewItem
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from tests.conftest import load_sample_website


class TestChefkochScraper:

    @staticmethod
    @fixture
    def scraper(vendor: Vendor) -> ChefkochScraper:
        return ChefkochScraper(vendor=vendor)

    @patch('application.crawler.scrapers.chefkoch_scraper.create_recipe_from_structured_data')
    def test_scrape_recipe(self, mock_create_recipe_from_structured_data, scraper: ChefkochScraper, recipe: Recipe, vendor: Vendor, category: Category):
        called = False
        vendor_fixture, category_fixture = vendor, category

        def mock_and_test_create_recipe_from_structured_data(structured_data: dict, url: str, vendor: Vendor, category: Category):
            nonlocal called

            called = True
            assert isinstance(structured_data, dict)
            assert url == recipe.url.value
            assert vendor == vendor_fixture
            assert category == category_fixture
            return recipe

        mock_create_recipe_from_structured_data.side_effect = mock_and_test_create_recipe_from_structured_data

        assert scraper.scrape_recipe(soup=load_sample_website('recipe.html'), url=recipe.url.value, category=category) == recipe
        assert called is True

    def test_parse_recipe_overview(self, scraper: ChefkochScraper, category: Category):
        parsed_recipe_overview = scraper.scrape_recipe_overview(soup=load_sample_website('recipe_overview.html'), category=category)

        assert len(parsed_recipe_overview) == 30
        for recipe in parsed_recipe_overview:
            assert isinstance(recipe, RecipeOverviewItem)
            assert isinstance(recipe.url, str)
            assert isinstance(recipe.category, Category)
            assert isinstance(recipe.published, datetime)

    def test_parse_categories(self, scraper: ChefkochScraper):
        parsed_categories = scraper.scrape_categories(soup=load_sample_website('categories.html'))

        assert len(parsed_categories) == 182
        for category in parsed_categories:
            assert isinstance(category, Category)
