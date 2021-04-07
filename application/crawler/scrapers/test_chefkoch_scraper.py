from datetime import datetime
from uuid import uuid4

from pytest import fixture

from application.crawler.scrapers import ChefkochScraper
from application.crawler.test_utils import parsed_recipe_sample, load_sample_website
from domain.model.vendor_aggregate import create_vendor


class TestChefkochScraper:

    @classmethod
    @fixture
    def scraper(cls) -> ChefkochScraper:
        return ChefkochScraper(vendor=create_vendor(
            vendor_id=uuid4(),
            name='test vendor',
            description='test',
            url='https://www.chefkoch.de',
            is_active=True,
            recipe_pattern='/rezepte/id/name.html',
            categories_link='/kategorien/',
            date_last_crawled=datetime.now(),
            languages=[],
            categories=[],
        ))

    def test_parse_recipe(self, scraper: ChefkochScraper):
        soup = load_sample_website('recipe.html')
        parsed_recipe = scraper.scrape_recipe(soup=soup)
        assert parsed_recipe == parsed_recipe_sample

    def test_parse_recipe_overview(self, scraper: ChefkochScraper):
        soup = load_sample_website('recipe_overview.html')
        parsed_recipe_overview = scraper.scrape_recipe_overview(soup=soup)
        assert len(parsed_recipe_overview) == 30
        for recipe in parsed_recipe_overview:
            assert len(recipe) == 2
            assert isinstance(recipe, tuple)
            assert isinstance(recipe[0], str)
            assert isinstance(recipe[1], datetime)

    def test_parse_categories(self, scraper: ChefkochScraper):
        soup = load_sample_website('categories.html')
        parsed_categories = scraper.scrape_categories(soup=soup)
        assert len(parsed_categories) == 182
        for category in parsed_categories:
            assert isinstance(category.name, str)
            assert isinstance(category.url, str)
