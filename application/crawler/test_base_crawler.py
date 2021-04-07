from typing import List
from unittest.mock import patch

from pytest import fixture

from application.crawler.base_crawler import AbstractBaseCrawler
from application.crawler.scrapers import ParsedRecipe, ParsedCategory


class TestBaseCrawler:
    FETCH_BATCH_SIZE = 20

    @staticmethod
    @fixture
    def crawler_implementation():
        class CrawlerImplementation(AbstractBaseCrawler):
            fetch_batch_size = 20

            @classmethod
            def crawl_categories(cls) -> List[ParsedCategory]:
                pass

            @classmethod
            def crawl_new_recipes(cls) -> List[ParsedRecipe]:
                pass

        return CrawlerImplementation()

    @patch('application.crawler.fetch.async_fetcher.AsyncFetcher.fetch_parallel')
    def test_crawl_and_parse(self, mock_fetch, crawler_implementation):
        urls = [f'test_url_{i}' for i in range(100)]

        def test_and_mock_fetch(url_batch):
            assert len(url_batch) == 20
            for url in url_batch:
                assert url == urls.pop(0)
            return [f'{url}_fetched' for url in url_batch]

        mock_fetch.side_effect = test_and_mock_fetch

        fetched_urls = crawler_implementation._crawl_urls(
            recipe_urls=urls.copy(),
            scrape_callback=lambda result: f'{result}_scraped'
        )

        assert sorted(fetched_urls) == sorted([f'test_url_{i}_fetched_scraped' for i in range(100)])

    @patch('application.crawler.fetch.async_fetcher.AsyncFetcher.fetch_parallel')
    def test_crawl_and_parse_list(self, mock_fetch, crawler_implementation):
        urls = [f'test_url_{i}' for i in range(100)]

        def test_and_mock_fetch(url_batch):
            assert len(url_batch) == 20
            for url in url_batch:
                assert url == urls.pop(0)
            return [[f'{url}_fetched'] for url in url_batch]

        mock_fetch.side_effect = test_and_mock_fetch

        fetched_urls = crawler_implementation._crawl_urls(
            recipe_urls=urls.copy(),
            scrape_callback=lambda result: [f'{url}_scraped' for url in result]
        )

        assert sorted(fetched_urls) == sorted([f'test_url_{i}_fetched_scraped' for i in range(100)])
