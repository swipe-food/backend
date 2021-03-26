from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List, Callable

from infrastructure.crawler.fetch import URLQueue, AsyncFetcher, FetchResult
from infrastructure.crawler.scrapers.data_classes import ParsedCategory, ParsedRecipe, ParsedData, ParsedRecipeOverviewItem


class AbstractBaseCrawler(ABC):
    fetch_batch_size: int

    @classmethod
    @abstractmethod
    def crawl_categories(cls) -> List[ParsedCategory]:
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def crawl_new_recipes(cls) -> List[ParsedRecipe]:
        raise NotImplementedError

    @classmethod
    def _crawl_and_parse(cls, recipe_urls: List[str], scrape_callback: Callable[[FetchResult], ParsedData or List[ParsedData]]):
        parsed_recipes = list()

        while not (queue := URLQueue(recipe_urls)).is_empty():
            url_batch = [next(queue) for _ in range(cls.fetch_batch_size) if not queue.is_empty()]

            for page in AsyncFetcher.fetch_parallel(url_batch):
                parsed_data = scrape_callback(page)
                if isinstance(parsed_data, list):
                    parsed_recipes += parsed_data
                else:
                    parsed_recipes.append(parsed_data)

        return parsed_recipes

    @classmethod
    def _filter_new_recipes(cls, recipes: List[ParsedRecipeOverviewItem]) -> List[ParsedRecipeOverviewItem]:
        def filter_recipes_from_previous_day(recipe: ParsedRecipeOverviewItem) -> bool:
            current_datetime = datetime.now()
            previous_day = datetime(year=current_datetime.year, month=current_datetime.month, day=current_datetime.day) - timedelta(days=1)
            recipe_publish_day = datetime(year=recipe.date_published.year, month=recipe.date_published.month, day=recipe.date_published.day)
            return recipe_publish_day == previous_day

        return list(filter(filter_recipes_from_previous_day, recipes))
