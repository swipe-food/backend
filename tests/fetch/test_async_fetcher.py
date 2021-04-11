import asyncio
from typing import Generator
from unittest.mock import patch

import aiohttp
import pytest
from aiohttp import ClientTimeout, InvalidURL
from bs4 import BeautifulSoup
from more_itertools import one

from infrastructure.fetch import AsyncFetcher, FetchResult


class TestAsyncFetcher:

    @staticmethod
    @pytest.fixture
    def fetcher():
        return AsyncFetcher(batch_size=10)

    @patch('infrastructure.fetch.async_fetcher.AsyncFetcher._fetch_url_async')
    def test_fetch(self, mock_fetch, fetcher):
        async def fetch(_, url: str):
            return FetchResult(url=url, status=200, html=BeautifulSoup())

        mock_fetch.side_effect = fetch

        test_urls = ['dummy_url'] * 10
        result_generator = fetcher.fetch(test_urls)

        assert isinstance(result_generator, Generator)
        results = one(list(result_generator))

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
            result = await fetcher._fetch_url_async(session, url)

        assert isinstance(result, FetchResult)
        assert result.status == 200
        assert result.url == url
        assert isinstance(result.html, BeautifulSoup)

    @pytest.mark.asyncio
    async def test_fetch_fail(self, fetcher):
        url = 'invalid_url'

        with pytest.raises(InvalidURL):
            async with aiohttp.ClientSession(loop=asyncio.get_event_loop(), timeout=ClientTimeout(10)) as session:
                await fetcher._fetch_url_async(session, url)
