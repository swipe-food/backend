from __future__ import annotations

from datetime import datetime
from typing import List

from more_itertools import one

from plugins.crawler.crawlers.base_crawler import AbstractBaseCrawler
from plugins.crawler.fetch import AsyncFetcher
from plugins.crawler.scrapers.chefkoch_scraper import ChefkochScraper
from plugins.crawler.scrapers.data_classes import ParsedCategory, ParsedRecipeOverviewItem, ParsedRecipe


class ChefkochCrawler(AbstractBaseCrawler):
    base_url = 'https://www.chefkoch.de'
    categories_url = '/rezepte/kategorien/'

    @classmethod
    def crawl_categories(cls) -> List[ParsedCategory]:
        full_categories_url = f'{cls.base_url}{cls.categories_url}'
        fetched_page = one(AsyncFetcher.fetch_parallel([full_categories_url]))
        return ChefkochScraper.parse_categories(soup=fetched_page.html)

    @classmethod
    def crawl_new_recipes(cls) -> List[ParsedRecipe]:
        recipe_overviews = cls._get_recipe_overview_items()
        new_recipes = filter(lambda item: (datetime.now() - item.date_published).days == 0, recipe_overviews)
        new_recipe_urls = [recipe.url for recipe in new_recipes]
        return cls._crawl_and_parse(new_recipe_urls, scrape_callback=lambda page: ChefkochScraper.parse_recipe(soup=page.html))

    @classmethod
    def _get_recipe_overview_items(cls) -> List[ParsedRecipeOverviewItem]:
        recipe_overview_urls = [f'{cls.base_url}{cls._get_date_sorted_url(category.url)}' for category in cls.crawl_categories()]
        return cls._crawl_and_parse(recipe_overview_urls, scrape_callback=lambda page: ChefkochScraper.parse_recipe_overview(soup=page.html))

    @staticmethod
    def _get_date_sorted_url(recipe_url: str) -> str:
        url_parts = recipe_url.split('/')

        for index, part in enumerate(url_parts):
            if part.startswith('s0'):
                url_parts[index] = f'{part[:2]}o3{part[2:]}'

        return "/".join(url_parts)
