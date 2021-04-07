from typing import Callable, List, Generic, TypeVar

from application.crawler import AbstractBaseCrawler
from application.crawler import ChefkochCrawler
from domain.model.category_aggregate import Category
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor
from infrastructure.adapters.scheduler import BlockingSchedulerAdapter
from infrastructure.config import create_new_config
from infrastructure.log import Logger
from infrastructure.storage.sql.postgres import create_postgres_database
from infrastructure.storage.sql.repositories.category import create_category_repository
from infrastructure.storage.sql.repositories.recipe import create_recipe_repository
from infrastructure.storage.sql.repositories.vendor import create_vendor_repository

CrawlerClass = TypeVar('CrawlerClass')


def crawl_all_sources_loop():
    config = create_new_config()

    db = create_postgres_database(config.database, Logger.create)

    recipe_repository = create_recipe_repository(db, Logger.create)
    vendor_repository = create_vendor_repository(db, Logger.create)

    def create_crawl_new_recipes_job(crawler_class: type(AbstractBaseCrawler), vendor: Vendor) -> Callable:
        def job():
            crawler = crawler_class(vendor=vendor, config=config.crawler, recipe_repository=recipe_repository)
            return crawler.crawl_new_recipes(store_recipes=True)

        return job

    scheduler = BlockingSchedulerAdapter()
    scheduler.add_daily_jobs(jobs=[
        create_crawl_new_recipes_job(crawler_class=ChefkochCrawler, vendor=vendor_repository.get_by_name('Chefkoch')),
    ])
    scheduler.start()


def get_crawler(crawler_class: type(Generic[CrawlerClass]), vendor_name: str, with_category_repository: bool = False, with_recipe_repository: bool = False) -> CrawlerClass:
    config = create_new_config()
    db = create_postgres_database(config.database, Logger.create)
    vendor_repository = create_vendor_repository(db, Logger.create)
    return crawler_class(
        vendor=vendor_repository.get_by_name(vendor_name=vendor_name),
        config=config.crawler,
        category_repository=create_category_repository(db, Logger.create) if with_category_repository else None,
        recipe_repository=create_recipe_repository(db, Logger.create) if with_recipe_repository else None,
        vendor_repository=create_vendor_repository(db, Logger.create),
    )


def crawl_chefkoch_categories(store_categories: bool = False) -> List[Category]:
    crawler = get_crawler(ChefkochCrawler, vendor_name='Chefkoch', with_category_repository=True)
    return crawler.crawl_categories(store_categories=store_categories)


def crawl_chefkoch_recipes(store_recipes: bool = False) -> List[Recipe]:
    crawler = get_crawler(ChefkochCrawler, vendor_name='Chefkoch', with_recipe_repository=True)
    return crawler.crawl_new_recipes(store_recipes=store_recipes)


if __name__ == '__main__':
    # crawl_all_sources_loop()
    # crawl_chefkoch_categories(store_categories=True)
    crawl_chefkoch_recipes(store_recipes=True)
