from datetime import datetime
from unittest.mock import patch

from pytest import fixture

from application.crawler.scrapers import ChefkochScraper
from domain.model.category_aggregate import Category
from domain.model.language_aggregate import Language
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from tests.conftest import load_sample_website


class TestChefkochScraper:

    @staticmethod
    @fixture
    def scraper(vendor: Vendor) -> ChefkochScraper:
        return ChefkochScraper(vendor=vendor)

    @patch('application.crawler.scrapers.chefkoch_scraper.create_recipe_from_structured_data')
    def test_scrape_recipe(self, mock_create_recipe_from_structured_data, scraper: ChefkochScraper, recipe: Recipe, vendor: Vendor, language: Language):
        called = False
        vendor_fixture, language_fixture = vendor, language

        def mock_and_test_create_recipe_from_structured_data(structured_data: dict, url: str, vendor: Vendor, language: Language):
            nonlocal called

            called = True
            assert isinstance(structured_data, dict)
            assert url == recipe.url.value
            assert vendor == vendor_fixture
            assert language == language_fixture
            return recipe

        mock_create_recipe_from_structured_data.side_effect = mock_and_test_create_recipe_from_structured_data

        assert scraper.scrape_recipe(soup=load_sample_website('recipe.html'), url=recipe.url.value) == recipe
        assert called is True

    def test_parse_recipe_overview(self, scraper: ChefkochScraper):
        parsed_recipe_overview = scraper.scrape_recipe_overview(soup=load_sample_website('recipe_overview.html'))

        assert len(parsed_recipe_overview) == 30
        for recipe in parsed_recipe_overview:
            assert len(recipe) == 2
            assert isinstance(recipe, tuple)
            assert isinstance(recipe[0], str)
            assert isinstance(recipe[1], datetime)

    def test_parse_categories(self, scraper: ChefkochScraper):
        parsed_categories = scraper.scrape_categories(soup=load_sample_website('categories.html'))

        assert len(parsed_categories) == 182
        for category in parsed_categories:
            assert isinstance(category, Category)
