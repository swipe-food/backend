from typing import List
from unittest.mock import patch

from more_itertools import one

from infrastructure.crawler.crawlers.chefkoch_crawler import ChefkochCrawler
from infrastructure.crawler.scrapers import ChefkochScraper
from infrastructure.crawler.test_utils import parsed_recipe_sample, load_sample_website


class TestChefkochCrawler:

    @patch('infrastructure.crawler.fetch.async_fetcher.AsyncFetcher.fetch_parallel')
    def test_crawl_categories(self, mock_fetch):
        def mock_and_test_fetch(urls: List[str]):
            assert urls == [f'{ChefkochCrawler.base_url}{ChefkochCrawler.categories_url}']
            return [load_sample_website('categories.html')]

        mock_fetch.side_effect = mock_and_test_fetch

        categories = ChefkochCrawler.crawl_categories()
        assert len(categories) == 182
        for category in categories:
            assert isinstance(category.name, str)
            assert isinstance(category.url, str)

    @patch('infrastructure.crawler.crawlers.base_crawler.AbstractBaseCrawler._crawl_and_parse')
    @patch('infrastructure.crawler.crawlers.chefkoch_crawler.ChefkochCrawler.crawl_categories')
    def test_crawl_new_recipes(self, mock_categories, mock_crawl_and_parse):
        call_counter = 0

        def mock_and_test_crawl_parse(recipe_urls, scrape_callback):
            nonlocal call_counter
            call_counter += 1
            if call_counter == 1:  # mock call in _get_recipe_overview_items
                assert len(recipe_urls) == 182
                return scrape_callback(load_sample_website('recipe_overview.html'))
            elif call_counter == 2:
                return [scrape_callback(load_sample_website('recipe.html'))]
            else:
                raise Exception('called _crawl_and_parse too often!')

        mock_categories.return_value = ChefkochScraper.parse_categories(soup=load_sample_website('categories.html'))
        mock_crawl_and_parse.side_effect = mock_and_test_crawl_parse

        recipes = ChefkochCrawler.crawl_new_recipes()

        assert one(recipes) == parsed_recipe_sample
