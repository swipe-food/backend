from __future__ import annotations

from itertools import chain
from typing import List

from more_itertools import one

from application.crawler.base import AbstractBaseCrawler
from application.crawler.scrapers import ChefkochScraper, RecipeOverviewItem
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from domain.repositories.category import AbstractCategoryRepository
from domain.repositories.recipe import AbstractRecipeRepository
from domain.repositories.vendor import AbstractVendorRepository
from infrastructure.fetch import AbstractFetcher


class ChefkochCrawler(AbstractBaseCrawler):

    def __init__(self, vendor: Vendor, fetcher: AbstractFetcher, recipe_repository: AbstractRecipeRepository = None,
                 category_repository: AbstractCategoryRepository = None,
                 vendor_repository: AbstractVendorRepository = None):
        super().__init__(
            vendor=vendor, fetcher=fetcher, recipe_repository=recipe_repository, category_repository=category_repository, vendor_repository=vendor_repository
        )
        self.scraper = ChefkochScraper(vendor=vendor)

    def crawl_categories(self, store_categories: bool = False) -> List[Category]:
        return one(self._crawl_and_process(
            urls_to_crawl=[self.vendor.categories_link],
            scrape_callback=lambda categories_page: self.scraper.scrape_categories(soup=categories_page.html),
            store_results=store_categories,
            store_callback=self._store_categories,
        ))

    def crawl_new_recipes(self, store_recipes: bool = True) -> List[Recipe]:
        self._crawl_categories_if_needed()

        all_recipe_overview_items = self._get_recipe_overview_items()
        recent_recipe_overview_items = set(self._filter_new_recipes(all_recipe_overview_items))

        return self._crawl_and_process(
            urls_to_crawl=[overview_item.url for overview_item in recent_recipe_overview_items],
            scrape_callback=lambda recipe_page: self.scraper.scrape_recipe(
                soup=recipe_page.html, url=recipe_page.url, category=list(filter(lambda item: item.url == recipe_page.url, recent_recipe_overview_items))[0].category
            ),
            store_results=store_recipes,
            store_callback=self._store_recipe,
        )

    def _get_recipe_overview_items(self) -> List[RecipeOverviewItem]:
        recipe_overview_urls = [self._get_date_sorted_url(category.url.value) for category in self.vendor.categories]
        return list(chain(*self._crawl_and_process(
            urls_to_crawl=recipe_overview_urls,
            scrape_callback=lambda overview_page: self.scraper.scrape_recipe_overview(
                soup=overview_page.html,
                category=one(filter(lambda category: self._get_date_sorted_url(category.url.value) == overview_page.url, self.vendor.categories)),
            ),
        )))

    def _store_categories(self, categories: List[Category]):
        if self._category_repository is None:
            raise ValueError('you must specify the category repository to store the crawled categories')
        for category in categories:
            self._category_repository.add(category)
            self.vendor.add_category(category)

    def _store_recipe(self, recipe: Recipe):
        if self._recipe_repository is None:
            raise ValueError('you must specify the recipe repository to store the crawled recipes')
        self._recipe_repository.add(recipe)

    @staticmethod
    def _get_date_sorted_url(recipe_url: str) -> str:
        url_parts = recipe_url.split('/')

        for index, part in enumerate(url_parts):
            if part.startswith('s0'):
                url_parts[index] = f'{part[:2]}o3{part[2:]}'

        return "/".join(url_parts)
