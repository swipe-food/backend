from adapters.scheduler import BlockingSchedulerAdapter
from plugins.config import create_new_config
from plugins.crawler import ChefkochCrawler
from plugins.crawler.crawlers import AbstractBaseCrawler


def crawl_all_sources_loop():
    scheduler = BlockingSchedulerAdapter()
    scheduler.add_daily_jobs(jobs=[crawler.crawl_new_recipes for crawler in AbstractBaseCrawler.__subclasses__()])
    scheduler.start()


if __name__ == '__main__':
    config = create_new_config()

    ChefkochCrawler.fetch_batch_size = config.crawler.fetch_batch_size
    ChefkochCrawler.crawl_new_recipes()
    crawl_all_sources_loop()
