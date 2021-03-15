import pytest
from bs4 import BeautifulSoup

from plugins.crawler.fetch.async_fetcher import AsyncFetcher, FetchResult


class TestAsyncFetcher:

    @staticmethod
    @pytest.fixture
    def fetcher():
        return AsyncFetcher()

    def test_fetch_parallel(self, fetcher):
        # TODO: patch

        test_urls = ['dummy_url'] * 10
        results = fetcher.fetch_parallel(test_urls)

        assert len(results) == len(test_urls)
        for result in results:
            assert isinstance(result, FetchResult)
            assert result.status == 200
            assert result.url == 'dummy_url'
            assert isinstance(result.html, BeautifulSoup)

    def test_fetch_success(self, fetcher):
        url = 'https://www.python.org/'
        result = fetcher.fetch(url)
        assert isinstance(result, FetchResult)
        assert result.status == 200
        assert result.url == url
        assert isinstance(result.html, BeautifulSoup)

    def test_fetch_fail(self, fetcher):
        url = 'invalid_url'
        result = fetcher.fetch(url)
        assert isinstance(result, FetchResult)
        assert result.status == 400
        assert result.url == url
        assert result.html is None
