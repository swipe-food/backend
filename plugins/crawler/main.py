from plugins.crawler.chefkoch_crawler import ChefkochCrawler

if __name__ == '__main__':
    res = ChefkochCrawler.crawl_new_recipes()
    print(res)
