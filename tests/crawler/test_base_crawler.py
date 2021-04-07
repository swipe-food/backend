from datetime import datetime, timedelta
from typing import List
from unittest.mock import patch

from pytest import fixture

from application.crawler.base_crawler import AbstractBaseCrawler
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from infrastructure.config import CrawlerConfig
from infrastructure.fetch import FetchResult
from tests.conftest import load_sample_website


class TestBaseCrawler:
    FETCH_BATCH_SIZE = 20

    @classmethod
    @fixture
    def crawler_implementation(cls, vendor: Vendor):
        config = CrawlerConfig()
        config.fetch_batch_size = cls.FETCH_BATCH_SIZE

        class CrawlerImplementation(AbstractBaseCrawler):

            @classmethod
            def crawl_categories(cls) -> List[Category]:
                pass

            @classmethod
            def crawl_new_recipes(cls) -> List[Recipe]:
                pass

        return CrawlerImplementation(vendor=vendor, config=config)

    @patch('application.crawler.base_crawler.AsyncFetcher.fetch_parallel')
    def test_crawl_urls(self, mock_fetch, crawler_implementation):
        test_urls = [f'test_url_{i}' for i in range(100)]

        def test_and_mock_fetch(urls: List[str], batch_size: int):
            assert urls == test_urls
            assert batch_size == self.FETCH_BATCH_SIZE

            for url in urls:
                yield [f'{url}_batch_fetched']

        mock_fetch.side_effect = test_and_mock_fetch

        page_generator = crawler_implementation._crawl_urls(urls=test_urls)
        pages = list(page_generator)

        assert pages == [f'test_url_{i}_batch_fetched' for i in range(100)]

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_urls')
    def test_crawl_and_process(self, mock_crawl_urls, crawler_implementation):
        test_urls = [f'test_url_{i}' for i in range(100)]
        test_fetch_result = FetchResult(url=test_urls[0], status=200, html=load_sample_website('recipe.html'))
        scrape_callback_called = False

        def scrape_callback(page):
            nonlocal scrape_callback_called
            scrape_callback_called = True
            assert page == test_fetch_result
            return 'scrape result'

        def mock_crawl_urls_implementation(urls: List[str]):
            assert urls == test_urls
            yield test_fetch_result

        mock_crawl_urls.side_effect = mock_crawl_urls_implementation

        assert crawler_implementation._crawl_and_process(urls_to_crawl=test_urls, scrape_callback=scrape_callback) == ['scrape result']
        assert scrape_callback_called is True

    @patch('application.crawler.base_crawler.AbstractBaseCrawler._crawl_urls')
    def test_crawl_and_process_and_store(self, mock_crawl_urls, crawler_implementation):
        test_urls = [f'test_url_{i}' for i in range(100)]
        test_fetch_result = FetchResult(url=test_urls[0], status=200, html=load_sample_website('recipe.html'))
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
            assert urls == test_urls
            yield test_fetch_result

        mock_crawl_urls.side_effect = mock_crawl_urls_implementation

        assert crawler_implementation._crawl_and_process(
            urls_to_crawl=test_urls, scrape_callback=scrape_callback, store_results=True, store_callback=store_callback,
        ) == ['scrape result']
        assert scrape_callback_called is True
        assert store_callback_called is True

    def test_filter_new_recipes(self, crawler_implementation):
        recipe_overviews = [
            ('url 1', datetime.now()),
            ('url 2', datetime.now() - timedelta(days=2)),
            ('url 3', datetime.now() - timedelta(days=1)),
            ('url 4', datetime.now() - timedelta(days=1)),
            ('url 5', datetime.now() - timedelta(days=3)),
        ]

        assert crawler_implementation._filter_new_recipes(recipe_overviews) == [recipe_overviews[2], recipe_overviews[3]]
