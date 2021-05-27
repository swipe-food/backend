from datetime import datetime
from typing import Callable, List, Generic, TypeVar
from uuid import uuid4

from application.api.services.vendor import create_vendor_service
from application.crawler import AbstractBaseCrawler
from application.crawler import ChefkochCrawler
from domain.model.language_aggregate import create_language
from domain.model.recipe_aggregate import Recipe
from domain.model.vendor_aggregate import Vendor, create_vendor
from infrastructure.adapters.scheduler import BlockingSchedulerAdapter
from infrastructure.config import create_new_config
from infrastructure.fetch import AsyncFetcher
from infrastructure.log import Logger
from infrastructure.storage.sql.postgres import create_postgres_database
from infrastructure.storage.sql.repositories.category import create_category_repository
from infrastructure.storage.sql.repositories.language import create_language_repository
from infrastructure.storage.sql.repositories.recipe import create_recipe_repository
from infrastructure.storage.sql.repositories.vendor import create_vendor_repository

CrawlerClass = TypeVar('CrawlerClass')


def initial_crawler_setup():
    config = create_new_config()
    logger = Logger.create(f'{__name__}.initial_crawler_setup')
    logger.info('starting crawler setup...')

    db = create_postgres_database(config.database, Logger.create)
    language_repo = create_language_repository(db, Logger.create)

    vendor_repo = create_vendor_repository(db, Logger.create)

    german = create_language(uuid4(), name='german', code='DE')
    language_repo.add(german)

    chefkoch = create_vendor(
        uuid4(), name='Chefkoch', description='...', url='https://www.chefkoch.de', is_active=True,
        recipe_pattern='', date_last_crawled=datetime.now(),
        categories_link='https://www.chefkoch.de/rezepte/kategorien/', language=german, categories=[]
    )
    vendor_repo.add(chefkoch)
    logger.info('crawler setup completed')


def crawl_all_sources_loop():
    config = create_new_config()
    fetcher = AsyncFetcher(batch_size=config.crawler.fetch_batch_size)

    db = create_postgres_database(config.database, Logger.create)

    category_repository = create_category_repository(db, Logger.create)
    recipe_repository = create_recipe_repository(db, Logger.create)
    vendor_repository = create_vendor_repository(db, Logger.create)

    vendor_service = create_vendor_service(vendor_repo=vendor_repository)
    if len(vendor_service.get_all()) == 0:
        initial_crawler_setup()

    def create_crawl_new_recipes_job(crawler_class: type(AbstractBaseCrawler), vendor: Vendor) -> Callable:
        def job():
            crawler = crawler_class(vendor=vendor, fetcher=fetcher, create_logger=Logger.create,
                                    recipe_repository=recipe_repository,
                                    category_repository=category_repository)
            return crawler.crawl_new_recipes(store_recipes=True)

        return job

    scheduler = BlockingSchedulerAdapter(create_logger=Logger.create)
    scheduler.add_daily_jobs(jobs=[
        create_crawl_new_recipes_job(crawler_class=ChefkochCrawler, vendor=vendor_repository.get_by_name('Chefkoch')),
    ])
    scheduler.start()


def get_crawler(crawler_class: type(Generic[CrawlerClass]), vendor_name: str, with_category_repository: bool = False,
                with_recipe_repository: bool = False) -> CrawlerClass:
    config = create_new_config()
    fetcher = AsyncFetcher(batch_size=config.crawler.fetch_batch_size)
    db = create_postgres_database(config.database, Logger.create)
    vendor_repository = create_vendor_repository(db, Logger.create)
    return crawler_class(
        vendor=vendor_repository.get_by_name(vendor_name=vendor_name),
        fetcher=fetcher, create_logger=Logger.create,
        category_repository=create_category_repository(db, Logger.create) if with_category_repository else None,
        recipe_repository=create_recipe_repository(db, Logger.create) if with_recipe_repository else None,
        vendor_repository=create_vendor_repository(db, Logger.create),
    )


def crawl_chefkoch_recipes(store_recipes: bool = False) -> List[Recipe]:  # for local development and testing
    crawler = get_crawler(ChefkochCrawler, vendor_name='Chefkoch', with_recipe_repository=True)
    return crawler.crawl_new_recipes(store_recipes=store_recipes)


if __name__ == '__main__':
    crawl_all_sources_loop()
