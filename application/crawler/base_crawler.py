from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Tuple, Generator, Callable, Any

from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.category import AbstractCategoryRepository
from domain.repositories.recipe import AbstractRecipeRepository
from domain.repositories.vendor import AbstractVendorRepository
from infrastructure.config import CrawlerConfig
from infrastructure.fetch import AsyncFetcher, FetchResult


class AbstractBaseCrawler(ABC):

    def __init__(self, vendor: Vendor, config: CrawlerConfig, recipe_repository: AbstractRecipeRepository = None, category_repository: AbstractCategoryRepository = None,
                 vendor_repository: AbstractVendorRepository = None):
        self.vendor = vendor
        self.config = config
        self._recipe_repository = recipe_repository
        self._category_repository = category_repository
        self._vendor_repository = vendor_repository

    @abstractmethod
    def crawl_categories(self) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def crawl_new_recipes(self) -> List[Recipe]:
        raise NotImplementedError

    def _crawl_urls(self, urls: List[str]) -> Generator[FetchResult, None, None]:
        for page_batch in AsyncFetcher.fetch_parallel(urls, batch_size=self.config.fetch_batch_size):
            for page in page_batch:
                yield page

    def _crawl_and_process(self, urls_to_crawl: List[str], scrape_callback: Callable[[FetchResult], Any],
                           store_results: bool = False, store_callback: Callable = None):
        results = list()
        for crawled_page in self._crawl_urls(urls_to_crawl):
            scrape_result = scrape_callback(crawled_page)
            if store_results and store_callback is not None:
                store_callback(scrape_result)
            results.append(scrape_result)
        return results

    @staticmethod
    def _filter_new_recipes(recipe_overviews: List[Tuple[str, datetime]]) -> List[Tuple[str, datetime]]:
        def filter_recipes_from_previous_day(recipe_overview: Tuple[str, datetime]) -> bool:
            _, date_published = recipe_overview
            current_datetime = datetime.now()
            previous_day = datetime(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day) - timedelta(days=1)
            recipe_publish_day = datetime(year=date_published.year, month=date_published.month, day=date_published.day)
            return recipe_publish_day == previous_day

        return list(filter(filter_recipes_from_previous_day, recipe_overviews))
