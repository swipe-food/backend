from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from typing import List


class ParsedData(ABC):
    pass


@dataclass
class ParsedCategory(ParsedData):
    name: str
    url: str


@dataclass
class ParsedRecipeOverviewItem(ParsedData):
    name: str
    url: str
    date_published: datetime


@dataclass
class ParsedRecipe(ParsedData):

    def __init__(self, structured_data: dict):
        self.name: str = self._get_attribute_from_structured_data('name', structured_data)
        self.description: str = self._get_attribute_from_structured_data('description', structured_data)
        self.image_url: str = self._get_attribute_from_structured_data('image', structured_data)
        self.category: str = self._get_attribute_from_structured_data('recipeCategory', structured_data)
        self.ingredients: List[str] = self._get_attribute_from_structured_data('recipeIngredient', structured_data)
        self.instructions: str = self._get_attribute_from_structured_data('recipeInstructions', structured_data)
        self.date_published: datetime = datetime.strptime(self._get_attribute_from_structured_data('datePublished', structured_data), '%Y-%m-%d')
        self.author: str = structured_data.get('author', dict()).get('name')
        self.rating_count: int = structured_data.get('aggregateRating', dict()).get('ratingCount')
        self.rating_value: float = structured_data.get('aggregateRating', dict()).get('ratingValue')

    @staticmethod
    def _get_attribute_from_structured_data(attribute: str, structured_data: dict):
        return structured_data.get(attribute, None)
