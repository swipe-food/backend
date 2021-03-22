from __future__ import annotations

from datetime import datetime
from typing import List, Tuple

from common.domain import Entity, URL, Immutable


def create_category_recipe_overviews(overview_items: List[Tuple[str, str, datetime]]) -> CategoryRecipeOverviews:
    return CategoryRecipeOverviews(overview_items)


class CategoryRecipeOverviews(Entity):

    def __init__(self, overview_items: List[Tuple[str, str, datetime]]):
        super().__init__()

        self._overview_items: List[RecipeOverviewItem] = []

        for item in overview_items:
            self.add_item(item)

    @property
    def items(self) -> Tuple[RecipeOverviewItem]:
        self._check_not_discarded()
        return tuple(self._overview_items)

    def add_item(self, item_data: Tuple[str, str, datetime]):
        self._check_not_discarded()
        if not isinstance(item_data, tuple):
            raise ValueError('item data name must be a tuple')
        name, url, date_published = item_data
        overview_item = RecipeOverviewItem(name=name, url=URL(url=url), date_published=date_published)
        self._overview_items.append(overview_item)
        self._increment_version()

    def __str__(self) -> str:
        return f"Category Recipe Overviews ('{len(self._overview_items)} items)'"


class RecipeOverviewItem(Immutable):

    def __init__(self, name: str, url: URL, date_published: datetime):
        if not isinstance(name, str):
            raise ValueError('name must be a string')

        if not isinstance(url, URL):
            raise ValueError('name must be a URL instance')

        if not isinstance(date_published, datetime):
            raise ValueError('name must be a datetime')

        self._name = name
        self._url = url
        self._date_published = date_published

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> URL:
        return self._url

    @property
    def date_published(self) -> datetime:
        return self._date_published

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._name == other._name and self._url == other._url and self._date_published == other._date_published

    def __str__(self) -> str:
        return f'Recipe Overview: {self._name} from {self._date_published.strftime("%d.%m.%Y")}'
