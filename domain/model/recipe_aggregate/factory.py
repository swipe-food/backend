from datetime import timedelta
from typing import List

from domain.model.category_aggregate import Category
from domain.model.common_value_objects import URL, Language
from domain.model.recipe_aggregate.recipe import Recipe, Ingredient
from domain.model.recipe_aggregate.value_objects import RecipeURL, AggregateRating
from domain.model.vendor_aggregate import Vendor


def create_recipe(name: str, description: str, vendor_id: str, recipe_url: str,
                  image_urls: List[str], ingredients: List[str], rating_count: int, rating_value: float,
                  category: Category, vendor: Vendor, language: Language, prep_time: timedelta = None,
                  cook_time: timedelta = None, total_time: timedelta = None) -> Recipe:
    if not isinstance(name, str):
        raise ValueError('name must be a string')

    if not isinstance(description, str):
        raise ValueError('description must be a string')

    if not isinstance(prep_time, timedelta):
        raise ValueError('prep_time must be a timedelta')

    if not isinstance(cook_time, timedelta):
        raise ValueError('cook_time must be a timedelta')

    if not isinstance(total_time, timedelta):
        raise ValueError('total_time must be a timedelta')

    if not isinstance(category, Category):
        raise ValueError('category must be a Category instance')

    if not isinstance(vendor, Vendor):
        raise ValueError('vendor must be a Vendor instance')

    if not isinstance(language, Language):
        raise ValueError('language must be a Language instance')

    if not isinstance(image_urls, list):
        raise ValueError('image_urls must be a list of URL instances')

    if not isinstance(ingredients, list):
        raise ValueError('ingredients must be a list of Ingredient instances')

    recipe_url_object = RecipeURL(url=recipe_url, vendor_pattern=vendor.recipe_pattern)
    image_url_objects = [URL(url=image_url) for image_url in image_urls]
    ingredient_objects = [Ingredient(text=ingredient) for ingredient in ingredients]
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
        name=name,
        description=description,
        vendor_id=vendor_id,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        url=recipe_url_object,
        images=image_url_objects,
        ingredients=ingredient_objects,
        category=category,
        aggregate_rating=aggregate_rating_object,
        language=language,
        vendor=vendor
    )
