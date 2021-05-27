import uuid
from datetime import datetime
from itertools import chain
from types import LambdaType
from typing import List, Callable, Any
from unittest.mock import patch

from pytest import fixture, raises

from application.crawler.chefkoch_crawler import ChefkochCrawler
from application.crawler.scrapers import RecipeOverviewItem
from domain.model.base import Entity
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.model.vendor_aggregate import Vendor
from domain.repositories.category import AbstractCategoryRepository
from domain.repositories.recipe import AbstractRecipeRepository
from infrastructure.fetch import FetchResult, AsyncFetcher
from infrastructure.log import Logger


class TestChefkochCrawler:

    @staticmethod
    @fixture
    def crawler(vendor: Vendor) -> ChefkochCrawler:
        fetcher = AsyncFetcher(batch_size=20)
        return ChefkochCrawler(vendor=vendor, fetcher=fetcher, create_logger=Logger.create)

    @staticmethod
    @fixture
    def overview_item_mocks(category: Category) -> list:
        return [RecipeOverviewItem(url='overview_url', category=category, published=datetime.now())]

    @staticmethod
    def get_mock_and_test_crawl_and_process_function(test_urls: List[str], test_store_results: bool = False, test_store_callback: Callable = None) -> Callable:
        def mock_and_test_crawl_and_process(urls_to_crawl: List[str], scrape_callback: Callable[[FetchResult], Any], store_results: bool = False, store_callback: Callable = None):
            assert urls_to_crawl == test_urls
            assert isinstance(scrape_callback, LambdaType)
            assert store_results is test_store_results
            assert store_callback == test_store_callback
            return ['verify mock_and_test_crawl_and_process called']

        return mock_and_test_crawl_and_process

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_and_process')
    def test_crawl_categories(self, mock_crawl_and_process, crawler: ChefkochCrawler, vendor: Vendor):
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[vendor.categories_link], test_store_results=False, test_store_callback=crawler._store_categories
        )
        assert crawler.crawl_categories() == 'verify mock_and_test_crawl_and_process called'

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_and_process')
    def test_crawl_and_store_categories(self, mock_crawl_and_process, crawler: ChefkochCrawler, vendor: Vendor):
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[vendor.categories_link], test_store_results=True, test_store_callback=crawler._store_categories
        )
        assert crawler.crawl_categories(store_categories=True) == 'verify mock_and_test_crawl_and_process called'

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_and_process')
    @patch('application.crawler.base.AbstractBaseCrawler._crawl_categories_if_needed')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._get_recipe_overview_items')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._filter_new_recipes')
    def test_crawl_new_recipes(self, mock_filter_new_recipes, mock_get_recipe_overview_items, mock_crawl_categories_if_needed, mock_crawl_and_process, crawler: ChefkochCrawler,
                               overview_item_mocks):
        mock_filter_new_recipes.return_value = overview_item_mocks
        mock_get_recipe_overview_items.return_value = overview_item_mocks
        mock_crawl_categories_if_needed.return_value = None
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[overview_item_mocks[0].url], test_store_results=False, test_store_callback=crawler._store_recipe
        )
        assert crawler.crawl_new_recipes(store_recipes=False) == ['verify mock_and_test_crawl_and_process called']

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_and_process')
    @patch('application.crawler.base.AbstractBaseCrawler._crawl_categories_if_needed')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._get_recipe_overview_items')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._filter_new_recipes')
    def test_crawl_and_store_new_recipes(self, mock_filter_new_recipes, mock_get_recipe_overview_items, mock_crawl_categories_if_needed, mock_crawl_and_process,
                                         crawler: ChefkochCrawler, overview_item_mocks):
        mock_filter_new_recipes.return_value = overview_item_mocks
        mock_get_recipe_overview_items.return_value = overview_item_mocks
        mock_crawl_categories_if_needed.return_value = None
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[overview_item_mocks[0].url], test_store_results=True, test_store_callback=crawler._store_recipe
        )
        assert crawler.crawl_new_recipes() == ['verify mock_and_test_crawl_and_process called']

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_and_process')
    def test_get_recipe_overview_items(self, mock_crawl_and_process, crawler: ChefkochCrawler, category: Category):
        crawler.vendor.add_category(category)
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(test_urls=[category.url.value])
        assert crawler._get_recipe_overview_items() == list(chain(*['verify mock_and_test_crawl_and_process called']))

    def test_store_categories(self, crawler: ChefkochCrawler, category: Category):
        call_counter = 0

        class CategoryRepositoryMock(AbstractCategoryRepository):

            def get_by_name(self, category_name: str) -> Category:
                pass

            def get_liked_users(self, category_: Category) -> List[User]:
                pass

            def get_recipes(self, category_: Category) -> List[Recipe]:
                pass

            def get_by_id(self, entity_id: uuid.UUID) -> Entity:
                pass

            def get_all(self, limit: int = None) -> List[Entity]:
                pass

            def get_all_categories_for_vendor(self, vendor: Vendor, limit: int = None) -> List[Category]:
                pass

            def add(self, entity: Entity):
                nonlocal call_counter
                assert entity == category
                call_counter += 1

            def update(self, entity: Entity):
                pass

            def delete(self, entity: Entity):
                pass

        crawler._category_repository = CategoryRepositoryMock()
        categories = [category]

        crawler._store_categories(categories=categories)

        assert crawler.vendor.categories == tuple(categories)
        assert call_counter == len(categories)

    def test_store_categories_fail(self, crawler: ChefkochCrawler):
        with raises(ValueError):
            crawler._store_categories(categories=[])

    def test_store_recipe(self, crawler: ChefkochCrawler, recipe: Recipe):
        call_counter = 0

        class RecipeRepositoryMock(AbstractRecipeRepository):

            def get_by_name(self, recipe_name: str) -> Recipe:
                pass

            def get_matched_users(self, recipe_: Recipe) -> List[User]:
                pass

            def get_unseen_recipes_for_user(self, user: User, limit: int = 20) -> List[Recipe]:
                pass

            def get_by_id(self, entity_id: uuid.UUID) -> Entity:
                pass

            def get_all(self, limit: int = None) -> List[Entity]:
                pass

            def add(self, entity: Entity):
                nonlocal call_counter
                assert entity == recipe
                call_counter += 1

            def update(self, entity: Entity):
                pass

            def delete(self, entity: Entity):
                pass

        crawler._recipe_repository = RecipeRepositoryMock()
        crawler._store_recipe(recipe=recipe)

        assert call_counter == 1

    def test_store_recipe_fail(self, crawler: ChefkochCrawler, recipe: Recipe):
        with raises(ValueError):
            crawler._store_recipe(recipe=recipe)

    def test_get_date_sorted_url(self):
        url = 'https://www.chefkoch.de/rs/s0g119/Partyrezepte.html'
        assert ChefkochCrawler._get_date_sorted_url(url) == 'https://www.chefkoch.de/rs/s0o3g119/Partyrezepte.html'
