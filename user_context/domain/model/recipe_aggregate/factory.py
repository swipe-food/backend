from datetime import timedelta
from typing import List
from uuid import UUID

from common.domain.value_objects import URL, AggregateRating, Author
from common.exceptions import InvalidValueError
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.ingredient_aggregate import Ingredient
from user_context.domain.model.language_aggregate import Language
from user_context.domain.model.recipe_aggregate.recipe import Recipe
from user_context.domain.model.recipe_aggregate.value_objects import RecipeURL
from user_context.domain.model.vendor_aggregate import Vendor


def create_recipe(recipe_id: UUID, name: str, description: str, author: str, vendor_id: str, recipe_url: str,
                  image_urls: List[str], ingredients: List[Ingredient], rating_count: int, rating_value: float,
                  category: Category, vendor: Vendor, language: Language, prep_time: timedelta = None,
                  cook_time: timedelta = None, total_time: timedelta = None) -> Recipe:
    if not isinstance(name, str):
        raise InvalidValueError(Recipe, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueError(Recipe, 'description must be a string')

    if not isinstance(prep_time, timedelta) and prep_time is not None:
        raise InvalidValueError(Recipe, 'prep_time must be a timedelta')

    if not isinstance(cook_time, timedelta) and cook_time is not None:
        raise InvalidValueError(Recipe, 'cook_time must be a timedelta')

    if not isinstance(total_time, timedelta) and total_time is not None:
        raise InvalidValueError(Recipe, 'total_time must be a timedelta')

    if not isinstance(category, Category):
        raise InvalidValueError(Recipe, 'category must be a Category instance')

    if not isinstance(vendor, Vendor):
        raise InvalidValueError(Recipe, 'vendor must be a Vendor instance')

    if not isinstance(language, Language):
        raise InvalidValueError(Recipe, 'language must be a Language instance')

    if not isinstance(image_urls, list):
        raise InvalidValueError(Recipe, 'image_urls must be a list of strings')

    if not isinstance(ingredients, list):
        raise InvalidValueError(Recipe, 'ingredients must be a list of strings')

    author_object = Author(name=author)
    recipe_url_object = RecipeURL(url=recipe_url, vendor_pattern=vendor.recipe_pattern)
    image_url_objects = [URL(url=image_url) for image_url in image_urls]
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
        recipe_id=recipe_id,
        name=name,
        description=description,
        author=author_object,
        vendor_id=vendor_id,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        url=recipe_url_object,
        images=image_url_objects,
        ingredients=ingredients,
        category=category,
        aggregate_rating=aggregate_rating_object,
        language=language,
        vendor=vendor
    )
