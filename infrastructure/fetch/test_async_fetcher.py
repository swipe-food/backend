import asyncio
from unittest.mock import patch

import aiohttp
import pytest
from aiohttp import ClientTimeout, InvalidURL
from bs4 import BeautifulSoup

from infrastructure.fetch import AsyncFetcher, FetchResult


class TestAsyncFetcher:

    @staticmethod
    @pytest.fixture
    def fetcher():
        return AsyncFetcher()

    @patch('application.crawler.fetch.async_fetcher.AsyncFetcher.fetch')
    def test_fetch_parallel(self, mock_fetch, fetcher):
        async def fetch(_, url: str):
            return FetchResult(url=url, status=200, html=BeautifulSoup())

        mock_fetch.side_effect = fetch

        test_urls = ['dummy_url'] * 10
        results = fetcher.fetch_parallel(test_urls)

        assert len(results) == len(test_urls)
        for result in results:
            assert isinstance(result, FetchResult)
            assert result.status == 200
            assert result.url == 'dummy_url'
            assert isinstance(result.html, BeautifulSoup)

    @pytest.mark.asyncio
    async def test_fetch_success(self, fetcher):
        url = 'https://www.python.org/'

        async with aiohttp.ClientSession(loop=asyncio.get_event_loop(), timeout=ClientTimeout(10)) as session:
            result = await fetcher.fetch(session, url)

        assert isinstance(result, FetchResult)
        assert result.status == 200
        assert result.url == url
        assert isinstance(result.html, BeautifulSoup)

    @pytest.mark.asyncio
    async def test_fetch_fail(self, fetcher):
        url = 'invalid_url'

        with pytest.raises(InvalidURL):
            async with aiohttp.ClientSession(loop=asyncio.get_event_loop(), timeout=ClientTimeout(10)) as session:
                await fetcher.fetch(session, url)
