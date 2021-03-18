from adapters.scheduler import BlockingSchedulerAdapter
from plugins.crawler.crawlers import AbstractBaseCrawler


def crawl_all_sources_loop():
    scheduler = BlockingSchedulerAdapter()
    scheduler.add_daily_jobs(jobs=[crawler.crawl_new_recipes for crawler in AbstractBaseCrawler.__subclasses__()])
    scheduler.start()


if __name__ == '__main__':
    crawl_all_sources_loop()
