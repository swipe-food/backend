from abc import ABC, abstractmethod
from typing import List, Callable

from plugins.crawler.config import FETCH_BATCH_SIZE
from plugins.crawler.fetch import URLQueue, AsyncFetcher, FetchResult
from plugins.crawler.scrapers.data import ParsedCategory, ParsedRecipe, ParsedData


class AbstractBaseCrawler(ABC):

    @classmethod
    @abstractmethod
    def crawl_categories(cls) -> List[ParsedCategory]:
        raise NotImplemented

    @classmethod
    @abstractmethod
    def crawl_new_recipes(cls) -> List[ParsedRecipe]:
        raise NotImplemented

    @classmethod
    def _crawl_and_parse(cls, recipe_urls: List[str], scrape_callback: Callable[[FetchResult], ParsedData or List[ParsedData]]):
        parsed_recipes = list()

        while not (queue := URLQueue(recipe_urls)).is_empty():
            url_batch = [next(queue) for _ in range(FETCH_BATCH_SIZE) if not queue.is_empty()]

            for page in AsyncFetcher.fetch_parallel(url_batch):
                parsed_data = scrape_callback(page)
                if isinstance(parsed_data, list):
                    parsed_recipes += parsed_data
                else:
                    parsed_recipes.append(parsed_data)

        return parsed_recipes
