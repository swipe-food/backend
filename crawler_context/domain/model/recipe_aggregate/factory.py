from datetime import datetime
from typing import List

from common.domain import Ingredient, AggregateRating, URL
from crawler_context.domain.model.recipe_aggregate.recipe import Recipe
from crawler_context.domain.model.recipe_aggregate.value_objects import RecipeCategory, Author


def create_recipe(name: str, description: str, image_url: str, category: str,
                  ingredients: List[str], instructions: str, date_published: datetime,
                  author: str, rating_count: int, rating_value: float) -> Recipe:
    if not isinstance(name, str):
        raise ValueError('recipe name must be a string')

    if not isinstance(description, str):
        raise ValueError('recipe description must be a string')

    if not isinstance(image_url, str):
        raise ValueError('recipe image url must be a string')

    if not isinstance(category, str):
        raise ValueError('recipe category must be a string')

    if not isinstance(ingredients, list):
        raise ValueError('recipe ingredients must be a list of strings or Ingredient instances')

    if not isinstance(instructions, str):
        raise ValueError('recipe instructions must be a string')

    if not isinstance(date_published, datetime):
        raise ValueError('date_published must be a datetime')

    if not isinstance(author, str):
        raise ValueError('recipe author must be a string')

    if not isinstance(rating_count, int):
        raise ValueError('recipe rating_count must be a int')

    if not isinstance(rating_value, float):
        raise ValueError('recipe rating_value must be a float')

    image_url_object = URL(url=image_url)
    category_object = RecipeCategory(name=category)
    ingredient_objects = [Ingredient(ingredient) for ingredient in ingredients]
    author_object = Author(name=author)
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
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
