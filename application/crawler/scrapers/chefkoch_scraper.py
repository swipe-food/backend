import json
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4

from bs4 import BeautifulSoup

from application.crawler.scrapers.base_scraper import AbstractBaseScraper
from domain.model.category_aggregate import Category, create_category
from domain.model.recipe_aggregate import Recipe
from domain.model.recipe_aggregate.factory import create_recipe_from_structured_data
from domain.model.vendor_aggregate import Vendor


class ChefkochScraper(AbstractBaseScraper):
    def __init__(self, vendor: Vendor):
        self.vendor = vendor

    def scrape_recipe(self, soup: BeautifulSoup, url: str) -> Recipe:
        for structured_data_entry in soup.find_all("script", type="application/ld+json"):
            structured_data = json.loads(structured_data_entry.string)
            if structured_data.get('@type', None) == 'Recipe':
                return create_recipe_from_structured_data(structured_data=structured_data, url=url, vendor=self.vendor, language=self.vendor.languages[0])

    def scrape_recipe_overview(self, soup: BeautifulSoup) -> List[Tuple[str, datetime]]:
        recipe_overview_items = list()
        for recipe in soup.findAll('article'):
            url = recipe.find('a').attrs.get('href', None)
            date_string = recipe.find(class_='recipe-date').contents[1].strip()
            date = datetime.strptime(date_string, '%d.%m.%Y')
            recipe_overview_items.append((str(url), date))
        return recipe_overview_items

    def scrape_categories(self, soup: BeautifulSoup) -> List[Category]:
        categories = list()
        for category_column in soup.findAll(class_='category-column'):
            categories += [
                create_category(category_id=uuid4(), name=category.string, url=f'{self.vendor.url}{category.attrs.get("href", None)}', vendor=self.vendor)
                for category in category_column.findAll('a')
            ]
        return categories
