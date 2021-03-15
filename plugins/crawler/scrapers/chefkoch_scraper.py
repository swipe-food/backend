import json
from datetime import datetime
from typing import List

from plugins.crawler.scrapers.base_scraper import AbstractBaseScraper
from plugins.crawler.scrapers.data import ParsedRecipe, ParsedCategory, ParsedRecipeOverviewItem


class ChefkochScraper(AbstractBaseScraper):
    def parse_recipe(self) -> ParsedRecipe:
        for structured_data_entry in self.soup.find_all("script", type="application/ld+json"):
            structured_data = json.loads(structured_data_entry.string)
            if structured_data.get('@type', None) == 'Recipe':
                return ParsedRecipe(structured_data)

    def parse_recipe_overview(self) -> List[ParsedRecipeOverviewItem]:
        recipe_overview_items = list()
        for recipe in self.soup.findAll('article'):
            name = recipe.find('h2').string
            url = recipe.find('a').attrs.get('href', None)
            date_string = recipe.find(class_='recipe-date').contents[1].strip()
            date = datetime.strptime(date_string, '%d.%m.%Y')
            recipe_overview_items.append(ParsedRecipeOverviewItem(name=name, url=url, date_published=date))
        return recipe_overview_items

    def parse_categories(self) -> List[ParsedCategory]:
        categories = list()
        for category_column in self.soup.findAll(class_='category-column'):
            categories += [
                ParsedCategory(name=category.string, url=category.attrs.get('href', None))
                for category in category_column.findAll('a')
            ]
        return categories
