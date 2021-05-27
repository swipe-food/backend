import asyncio
from asyncio import AbstractEventLoop
from typing import List, Generator

import aiohttp
from aiohttp import ClientTimeout, ClientSession
from bs4 import BeautifulSoup

from infrastructure.fetch.base import AbstractFetcher, FetchResult
from infrastructure.fetch.url_queue import URLQueue


class AsyncFetcher(AbstractFetcher):
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'

    def __init__(self, batch_size: int):
        self.fetch_batch_size = batch_size

    def fetch(self, urls: List[str]) -> Generator[List[FetchResult], None, None]:
        """Fetches urls parallel in batches and returns a generator that yields every fetched URL batch as a list of FetchResult objects."""

        loop = self._get_event_loop()
        queue = URLQueue(urls=urls)
        while not queue.is_empty():
            url_batch = [next(queue) for _ in range(self.fetch_batch_size) if not queue.is_empty()]
            yield loop.run_until_complete(self._fetch_parallel_job(url_batch))

    @staticmethod
    async def _fetch_url_async(session: ClientSession, url: str) -> FetchResult:
        async with session.get(url) as response:
            status = response.status
            html = await response.read()
            return FetchResult(url=url, status=status, html=BeautifulSoup(html, "lxml"))

    async def _fetch_parallel_job(self, urls):
        async with aiohttp.ClientSession(timeout=ClientTimeout(10), headers={'user-agent': self.user_agent}) as session:
            return await asyncio.gather(
                *[self._fetch_url_async(session, url) for url in urls], return_exceptions=True
            )

    @staticmethod
    def _get_event_loop() -> AbstractEventLoop:
        try:
            return asyncio.get_event_loop()
        except RuntimeError as exception:
            if "There is no current event loop in thread" in str(exception):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                return asyncio.get_event_loop()
