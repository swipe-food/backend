from datetime import datetime
from typing import List
from uuid import UUID

from common.domain.value_objects import AggregateRating, URL
from common.exceptions import InvalidValueError
from crawler_context.domain.model.recipe_aggregate.recipe import Recipe
from crawler_context.domain.model.recipe_aggregate.value_objects import RecipeCategory, Author, Ingredient


def create_recipe(recipe_id: UUID, name: str, description: str, image_url: str, category: str,
                  ingredients: List[str], instructions: str, date_published: datetime,
                  author: str, rating_count: int, rating_value: float) -> Recipe:
    if not isinstance(name, str):
        raise InvalidValueError(Recipe, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueError(Recipe, 'description must be a string')

    if not isinstance(image_url, str):
        raise InvalidValueError(Recipe, 'image url must be a string')

    if not isinstance(category, str):
        raise InvalidValueError(Recipe, 'category must be a string')

    if not isinstance(ingredients, list):
        raise InvalidValueError(Recipe, 'ingredients must be a list of strings or Ingredient instances')

    if not isinstance(instructions, str):
        raise InvalidValueError(Recipe, 'instructions must be a string')

    if not isinstance(date_published, datetime):
        raise InvalidValueError(Recipe, 'date_published must be a datetime')

    if not isinstance(author, str):
        raise InvalidValueError(Recipe, 'author must be a string')

    if not isinstance(rating_count, int):
        raise InvalidValueError(Recipe, 'rating_count must be a int')

    if not isinstance(rating_value, float):
        raise InvalidValueError(Recipe, 'rating_value must be a float')

    image_url_object = URL(url=image_url)
    category_object = RecipeCategory(name=category)
    ingredient_objects = [Ingredient(ingredient) for ingredient in ingredients]
    author_object = Author(name=author)
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
        recipe_id=recipe_id,
        name=name,
        description=description,
        image_url=image_url_object,
        category=category_object,
        ingredients=ingredient_objects,
        instructions=instructions,
        date_published=date_published,
        author=author_object,
        aggregate_rating=aggregate_rating_object,
    )
