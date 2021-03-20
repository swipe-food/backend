from datetime import timedelta
from typing import List

from domain.model.category_aggregate import Category
from domain.model.common_aggregate import Language, URL
from domain.model.recipe_aggregate.entities import Recipe, Ingredient
from domain.model.recipe_aggregate.value_objects import RecipeURL, AggregateRating
from domain.model.vendor_aggregate import Vendor


def create_recipe(name: str, description: str, vendor_id: str, recipe_url: str,
                  images: List[URL], ingredients: List[Ingredient], aggregate_rating: AggregateRating,
                  category: Category, vendor: Vendor, language: Language, prep_time: timedelta = None,
                  cook_time: timedelta = None, total_time: timedelta = None) -> Recipe:
    return Recipe(
        name=name,
        description=description,
        vendor_id=vendor_id,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        url=RecipeURL(recipe_url, vendor.recipe_pattern),
        images=images,
        ingredients=ingredients,
        category=category,
        aggregate_rating=aggregate_rating,
        language=language,
        vendor=vendor
    )
