import uuid
from datetime import datetime
from itertools import chain
from types import LambdaType
from typing import List, Callable, Any
from unittest.mock import patch

from pytest import fixture, raises

from application.crawler.chefkoch_crawler import ChefkochCrawler
from domain.model.base import Entity
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.model.vendor_aggregate import Vendor
from domain.repositories.category import AbstractCategoryRepository
from domain.repositories.recipe import AbstractRecipeRepository
from infrastructure.config import CrawlerConfig
from infrastructure.fetch import FetchResult


class TestChefkochCrawler:

    @staticmethod
    @fixture
    def crawler(vendor: Vendor) -> ChefkochCrawler:
        config = CrawlerConfig()
        config.fetch_batch_size = 10
        return ChefkochCrawler(vendor=vendor, config=config)

    @staticmethod
    @fixture
    def overview_item_mocks() -> list:
        return [('overview_url', datetime.now())]

    @staticmethod
    def get_mock_and_test_crawl_and_process_function(test_urls: List[str], test_store_results: bool = False, test_store_callback: Callable = None) -> Callable:
        def mock_and_test_crawl_and_process(urls_to_crawl: List[str], scrape_callback: Callable[[FetchResult], Any], store_results: bool = False, store_callback: Callable = None):
            assert urls_to_crawl == test_urls
            assert isinstance(scrape_callback, LambdaType)
            assert store_results is test_store_results
            assert store_callback == test_store_callback
            return ['verify mock_and_test_crawl_and_process called']

        return mock_and_test_crawl_and_process

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_and_process')
    def test_crawl_categories(self, mock_crawl_and_process, crawler: ChefkochCrawler, vendor: Vendor):
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[vendor.categories_link], test_store_results=False, test_store_callback=crawler._store_categories
        )
        assert crawler.crawl_categories() == 'verify mock_and_test_crawl_and_process called'

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_and_process')
    def test_crawl_and_store_categories(self, mock_crawl_and_process, crawler: ChefkochCrawler, vendor: Vendor):
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[vendor.categories_link], test_store_results=True, test_store_callback=crawler._store_categories
        )
        assert crawler.crawl_categories(store_categories=True) == 'verify mock_and_test_crawl_and_process called'

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_and_process')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._get_recipe_overview_items')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._filter_new_recipes')
    def test_crawl_new_recipes(self, mock_filter_new_recipes, mock_get_recipe_overview_items, mock_crawl_and_process, crawler: ChefkochCrawler, vendor: Vendor,
                               overview_item_mocks):
        mock_filter_new_recipes.return_value = overview_item_mocks
        mock_get_recipe_overview_items.return_value = overview_item_mocks
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[overview_item_mocks[0][0]], test_store_results=False, test_store_callback=crawler._store_recipe
        )
        assert crawler.crawl_new_recipes(store_recipes=False) == ['verify mock_and_test_crawl_and_process called']

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_and_process')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._get_recipe_overview_items')
    @patch('application.crawler.chefkoch_crawler.ChefkochCrawler._filter_new_recipes')
    def test_crawl_and_store_new_recipes(self, mock_filter_new_recipes, mock_get_recipe_overview_items, mock_crawl_and_process, crawler: ChefkochCrawler, vendor: Vendor,
                                         overview_item_mocks):
        mock_filter_new_recipes.return_value = overview_item_mocks
        mock_get_recipe_overview_items.return_value = overview_item_mocks
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(
            test_urls=[overview_item_mocks[0][0]], test_store_results=True, test_store_callback=crawler._store_recipe
        )
        assert crawler.crawl_new_recipes() == ['verify mock_and_test_crawl_and_process called']

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_and_process')
    def test_get_recipe_overview_items(self, mock_crawl_and_process, crawler: ChefkochCrawler, category: Category):
        crawler.vendor.add_category(category)
        mock_crawl_and_process.side_effect = self.get_mock_and_test_crawl_and_process_function(test_urls=[category.url.value])
        assert crawler._get_recipe_overview_items() == list(chain(*['verify mock_and_test_crawl_and_process called']))

    def test_store_categories(self, crawler: ChefkochCrawler, category: Category):
        call_counter = 0

        class CategoryRepositoryMock(AbstractCategoryRepository):

            def get_by_name(self, category_name: str) -> Category:
                pass

            def get_liked_users(self, category: Category) -> List[User]:
                pass

            def get_recipes(self, category: Category) -> List[Recipe]:
                pass

            def get_by_id(self, entity_id: uuid.UUID) -> Entity:
                pass

            def get_all(self, limit: int = None) -> List[Entity]:
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

            def get_matched_users(self, recipe: Recipe) -> List[User]:
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

    def test_store_recipe_fail(self, crawler: ChefkochCrawler):
        with raises(ValueError):
            crawler._store_recipe(recipe=None)

    def test_get_date_sorted_url(self):
        url = 'https://www.chefkoch.de/rs/s0g119/Partyrezepte.html'
        assert ChefkochCrawler._get_date_sorted_url(url) == 'https://www.chefkoch.de/rs/s0o3g119/Partyrezepte.html'

    #
    # @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_and_process')
    # def test_crawl_new_recipes(self, mock_crawl_and_process, crawler: ChefkochCrawler, recipe: Recipe):
    #     call_counter = 0
    #
    #     def mock_and_test_crawl_parse(urls_to_crawl: List[str], scrape_callback: Callable[[FetchResult], Any], store_results: bool = False, store_callback: Callable = None):
    #         nonlocal call_counter
    #         call_counter += 1
    #         if call_counter == 1:  # mock call in _get_recipe_overview_items
    #             assert len(urls_to_crawl) == 182
    #             return [scrape_callback(load_sample_website('recipe_overview.html'))]
    #         elif call_counter == 2:
    #             return [scrape_callback(load_sample_website('recipe.html'))]
    #         else:
    #             raise Exception('called _crawl_and_process too often!')
    #
    #     mock_crawl_and_process.side_effect = mock_and_test_crawl_parse
    #     for category in crawler.scraper.scrape_categories(soup=load_sample_website('categories.html')):
    #         crawler.vendor.add_category(category)
    #
    #     recipes = crawler.crawl_new_recipes(store_recipes=False)
    #     crawled_recipe = one(recipes)
    #
    #     assert crawled_recipe.name == recipe.name
    #     assert crawled_recipe.description == recipe.description
    #     assert crawled_recipe.image == recipe.image
    #     assert crawled_recipe.category.name == recipe.category.name
    #     assert crawled_recipe.vendor.name == recipe.vendor.name
    #     assert crawled_recipe.url == recipe.url
    #     assert crawled_recipe.language.name == recipe.language.name
    #     assert crawled_recipe.cook_time == recipe.cook_time
    #     assert crawled_recipe.prep_time == recipe.prep_time
    #     assert crawled_recipe.total_time == recipe.total_time
    #     assert crawled_recipe.author == recipe.author
    #     assert crawled_recipe.date_published == recipe.date_published
    #     assert crawled_recipe.aggregate_rating == recipe.aggregate_rating
    #
    #     for index, ingredient in enumerate(crawled_recipe.ingredients):
    #         assert ingredient.text == recipe.ingredients[index].text
    #
    # @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_urls')
    # def test_crawl_and_store_new_recipes(self, mock_crawl_urls, crawler: ChefkochCrawler, recipe: Recipe):
    #     call_counter = 0
    #
    #     def mock_and_test_crawl_urls(recipe_urls: List[str]):
    #         nonlocal call_counter
    #         call_counter += 1
    #         if call_counter == 1:  # mock call in _get_recipe_overview_items
    #             assert len(recipe_urls) == 182
    #             return [load_sample_website('recipe_overview.html')]
    #         elif call_counter == 2:
    #             assert len(recipe_urls) == 1
    #             return [load_sample_website('recipe.html')]
    #         else:
    #             raise Exception('called _crawl_and_process too often!')
    #
    #     class MockRecipeRepository(AbstractRecipeRepository):  # TODO: outsource this other tests need it as well
    #
    #         def get_by_name(self, recipe_name: str) -> Recipe:
    #             pass
    #
    #         def get_matched_users(self, recipe: Recipe) -> List[User]:
    #             pass
    #
    #         def get_unseen_recipes_for_user(self, user: User, limit: int = 20) -> List[Recipe]:
    #             pass
    #
    #         def get_by_id(self, entity_id: uuid.UUID) -> Entity:
    #             pass
    #
    #         def get_all(self, limit: int = None) -> List[Entity]:
    #             pass
    #
    #         def add(self, entity: Entity):
    #             pass
    #
    #         def update(self, entity: Entity):
    #             pass
    #
    #         def delete(self, entity: Entity):
    #             pass
    #
    #     mock_crawl_urls.side_effect = mock_and_test_crawl_urls
    #     crawler._recipe_repository = MockRecipeRepository()
    #     for category in crawler.scraper.scrape_categories(soup=load_sample_website('categories.html')):
    #         crawler.vendor.add_category(category)
    #
    #     recipes = crawler.crawl_new_recipes(store_recipes=True)
    #     crawled_recipe = one(recipes)
    #
    #     assert crawled_recipe.name == recipe.name
    #     assert crawled_recipe.description == recipe.description
    #     assert crawled_recipe.image == recipe.image
    #     assert crawled_recipe.category.name == recipe.category.name
    #     assert crawled_recipe.vendor.name == recipe.vendor.name
    #     assert crawled_recipe.url == recipe.url
    #     assert crawled_recipe.language.name == recipe.language.name
    #     assert crawled_recipe.cook_time == recipe.cook_time
    #     assert crawled_recipe.prep_time == recipe.prep_time
    #     assert crawled_recipe.total_time == recipe.total_time
    #     assert crawled_recipe.author == recipe.author
    #     assert crawled_recipe.date_published == recipe.date_published
    #     assert crawled_recipe.aggregate_rating == recipe.aggregate_rating
    #
    #     for index, ingredient in enumerate(crawled_recipe.ingredients):
    #         assert ingredient.text == recipe.ingredients[index].text
