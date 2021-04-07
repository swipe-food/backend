import asyncio
from dataclasses import dataclass
from typing import List, Generator

import aiohttp
from aiohttp import ClientTimeout, ClientSession
from bs4 import BeautifulSoup

from infrastructure.fetch.url_queue import URLQueue


@dataclass
class FetchResult:
    url: str
    status: int
    html: BeautifulSoup


class AsyncFetcher:
    user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0'

    @classmethod
    def fetch_parallel(cls, urls: List[str], batch_size: int) -> Generator[List[FetchResult], None, None]:
        """Fetches urls parallel in batches and returns a generator that yields every fetched URL batch as a list of FetchResult objects."""
        loop = asyncio.get_event_loop()
        queue = URLQueue(urls=urls)
        while not queue.is_empty():
            url_batch = [next(queue) for _ in range(batch_size) if not queue.is_empty()]
            yield loop.run_until_complete(cls._fetch_parallel_job(url_batch))

    @staticmethod
    async def fetch(session: ClientSession, url: str) -> FetchResult:
        async with session.get(url) as response:
            status = response.status
            html = await response.read()
            return FetchResult(url=url, status=status, html=BeautifulSoup(html, "lxml"))

    @classmethod
    async def _fetch_parallel_job(cls, urls):
        async with aiohttp.ClientSession(timeout=ClientTimeout(10), headers={'user-agent': cls.user_agent}) as session:
            return await asyncio.gather(
                *[cls.fetch(session, url) for url in urls], return_exceptions=True
            )
