from datetime import timedelta
from typing import List

from domain.model.category_aggregate.entities import Category
from domain.model.common_aggregate import create_entity_id, Language
from domain.model.recipe_aggregate.entities import Recipe, ImageURL, Ingredient
from domain.model.recipe_aggregate.value_objects import RecipeURL, AggregateRating
from domain.model.vendor_aggregate.entities import Vendor


def create_image_url(version: int, url: str) -> ImageURL:
    # TODO validate
    scheme, domain, resource, parameters = url, url, url, url
    return ImageURL(image_url_id=create_entity_id(),
                    image_url_version=version,
                    scheme=scheme,
                    domain=domain,
                    resource=resource,
                    parameters=parameters)


def create_ingredient(version: int, text: str) -> Ingredient:
    return Ingredient(ingredient_id=create_entity_id(),
                      ingredient_version=version,
                      text=text)


def create_recipe(version: int, name: str, description: str, vendor_id: str, recipe_url: str,
                  images: List[ImageURL],
                  ingredients: List[Ingredient], aggregate_rating: AggregateRating,
                  category: Category, vendor: Vendor,
                  language: Language, prep_time: timedelta = None,
                  cook_time: timedelta = None, total_time: timedelta = None) -> Recipe:
    return Recipe(recipe_id=create_entity_id(),
                  recipe_version=version,
                  name=name,
                  description=description,
                  vendor_id=vendor_id,
                  prep_time=prep_time,
                  cook_time=cook_time,
                  total_time=total_time,
                  url=RecipeURL.from_text_with_pattern(recipe_url, vendor.recipe_pattern),
                  images=images,
                  ingredients=ingredients,
                  category=category,
                  aggregate_rating=aggregate_rating,
                  language=language,
                  vendor=vendor)
