from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Generator, Callable, Any

from application.crawler.scrapers import RecipeOverviewItem
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.category import AbstractCategoryRepository
from domain.repositories.recipe import AbstractRecipeRepository
from domain.repositories.vendor import AbstractVendorRepository
from infrastructure.fetch import FetchResult, AbstractFetcher


class AbstractBaseCrawler(ABC):

    def __init__(self, vendor: Vendor, fetcher: AbstractFetcher, recipe_repository: AbstractRecipeRepository = None,
                 category_repository: AbstractCategoryRepository = None, vendor_repository: AbstractVendorRepository = None):
        self.vendor = vendor
        self._fetcher = fetcher
        self._recipe_repository = recipe_repository
        self._category_repository = category_repository
        self._vendor_repository = vendor_repository

    @abstractmethod
    def crawl_categories(self, store_categories: bool = False) -> List[Category]:
        raise NotImplementedError

    @abstractmethod
    def crawl_new_recipes(self) -> List[Recipe]:
        raise NotImplementedError

    def _crawl_urls(self, urls: List[str]) -> Generator[FetchResult, None, None]:
        for page_batch in self._fetcher.fetch(urls):
            for page in page_batch:
                yield page

    def _crawl_and_process(self, urls_to_crawl: List[str], scrape_callback: Callable[[FetchResult], Any], store_results: bool = False, store_callback: Callable = None):
        results = list()
        for crawled_page in self._crawl_urls(urls_to_crawl):
            scrape_result = scrape_callback(crawled_page)
            if store_results and store_callback is not None:
                store_callback(scrape_result)
            results.append(scrape_result)
        return results

    def _crawl_categories_if_needed(self):
        if len(self._category_repository.get_all_categories_for_vendor(self.vendor)) > 0:
            self.crawl_categories(store_categories=True)

    @staticmethod
    def _filter_new_recipes(recipe_overviews: List[RecipeOverviewItem]) -> List[RecipeOverviewItem]:
        def filter_recipes_from_previous_day(recipe_overview: RecipeOverviewItem) -> bool:
            current_datetime = datetime.now()
            previous_day = datetime(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day) - timedelta(days=1)
            recipe_publish_day = datetime(year=recipe_overview.published.year, month=recipe_overview.published.month, day=recipe_overview.published.day)
            return recipe_publish_day == previous_day

        return list(filter(filter_recipes_from_previous_day, recipe_overviews))
