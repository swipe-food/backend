from datetime import datetime, timedelta
from typing import List, Generator
from unittest.mock import patch

from pytest import fixture

from application.crawler.base import AbstractBaseCrawler
from application.crawler.scrapers import RecipeOverviewItem
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from infrastructure.fetch import FetchResult, AbstractFetcher
from infrastructure.log import Logger
from tests.conftest import load_sample_website


class TestBaseCrawler:
    test_urls = [f'test_url_{i}' for i in range(100)]

    class FetcherMock(AbstractFetcher):

        def fetch(self, urls: List[str]) -> Generator[List[FetchResult], None, None]:
            assert urls == TestBaseCrawler.test_urls
            for url in urls:
                yield [f'{url}_batch_fetched']

    @classmethod
    @fixture
    def crawler_implementation(cls, vendor: Vendor):
        class CrawlerImplementation(AbstractBaseCrawler):

            @classmethod
            def crawl_categories(cls) -> List[Category]:
                pass

            @classmethod
            def crawl_new_recipes(cls) -> List[Recipe]:
                pass

        return CrawlerImplementation(vendor=vendor, fetcher=cls.FetcherMock(), create_logger=Logger.create)

    def test_crawl_urls(self, crawler_implementation):
        page_generator = crawler_implementation._crawl_urls(urls=self.test_urls)
        pages = list(page_generator)

        assert pages == [f'test_url_{i}_batch_fetched' for i in range(100)]

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_urls')
    def test_crawl_and_process(self, mock_crawl_urls, crawler_implementation):
        test_fetch_result = FetchResult(url=self.test_urls[0], status=200, html=load_sample_website('recipe.html'))
        scrape_callback_called = False

        def scrape_callback(page):
            nonlocal scrape_callback_called
            scrape_callback_called = True
            assert page == test_fetch_result
            return 'scrape result'

        def mock_crawl_urls_implementation(urls: List[str]):
            assert urls == self.test_urls
            yield test_fetch_result

        mock_crawl_urls.side_effect = mock_crawl_urls_implementation

        assert crawler_implementation._crawl_and_process(urls_to_crawl=self.test_urls, scrape_callback=scrape_callback) == ['scrape result']
        assert scrape_callback_called is True

    @patch('application.crawler.base.AbstractBaseCrawler._crawl_urls')
    def test_crawl_and_process_and_store(self, mock_crawl_urls, crawler_implementation):
        test_fetch_result = FetchResult(url=self.test_urls[0], status=200, html=load_sample_website('recipe.html'))
        scrape_callback_called, store_callback_called = False, False

        def scrape_callback(page):
            nonlocal scrape_callback_called
            scrape_callback_called = True
            assert page == test_fetch_result
            return 'scrape result'

        def store_callback(value):
            nonlocal store_callback_called
            assert value == 'scrape result'
            store_callback_called = True

        def mock_crawl_urls_implementation(urls: List[str]):
            assert urls == self.test_urls
            yield test_fetch_result

        mock_crawl_urls.side_effect = mock_crawl_urls_implementation

        assert crawler_implementation._crawl_and_process(
            urls_to_crawl=self.test_urls, scrape_callback=scrape_callback, store_results=True, store_callback=store_callback,
        ) == ['scrape result']
        assert scrape_callback_called is True
        assert store_callback_called is True

    def test_filter_new_recipes(self, crawler_implementation, category: Category):
        recipe_overviews = [
            RecipeOverviewItem(url='url 1', category=category, published=datetime.now()),
            RecipeOverviewItem(url='url 2', category=category, published=datetime.now() - timedelta(days=2)),
            RecipeOverviewItem(url='url 3', category=category, published=datetime.now() - timedelta(days=1)),
            RecipeOverviewItem(url='url 4', category=category, published=datetime.now() - timedelta(days=1)),
            RecipeOverviewItem(url='url 5', category=category, published=datetime.now() - timedelta(days=3)),
        ]

        assert crawler_implementation._filter_new_recipes(recipe_overviews) == [recipe_overviews[2], recipe_overviews[3]]
