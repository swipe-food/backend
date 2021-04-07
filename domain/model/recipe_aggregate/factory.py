from datetime import timedelta, datetime
from typing import List
from uuid import UUID, uuid4

from domain.exceptions import InvalidValueException
from domain.model.category_aggregate import Category
from domain.model.common_value_objects import URL
from domain.model.ingredient_aggregate import Ingredient, create_ingredient
from domain.model.language_aggregate import Language
from domain.model.recipe_aggregate.recipe import Recipe
from domain.model.recipe_aggregate.value_objects import RecipeURL, AggregateRating, Author
from domain.model.vendor_aggregate import Vendor


def create_recipe(recipe_id: UUID, name: str, description: str, author: str,
                  prep_time: timedelta, cook_time: timedelta, total_time: timedelta, date_published: datetime,
                  url: str, category: Category, vendor: Vendor, language: Language, rating_count: int,
                  rating_value: float, image_url: str, ingredients: List[Ingredient]) -> Recipe:
    if not isinstance(name, str):
        raise InvalidValueException(Recipe, 'name must be a string')

    if not isinstance(description, str):
        raise InvalidValueException(Recipe, 'description must be a string')

    if not isinstance(prep_time, timedelta):
        raise InvalidValueException(Recipe, 'prep_time must be a timedelta')

    if not isinstance(cook_time, timedelta):
        raise InvalidValueException(Recipe, 'cook_time must be a timedelta')

    if not isinstance(total_time, timedelta):
        raise InvalidValueException(Recipe, 'total_time must be a timedelta')

    if not isinstance(date_published, datetime):
        raise InvalidValueException(Recipe, 'date_published must be a datetime')

    if not isinstance(category, Category):
        raise InvalidValueException(Recipe, 'category must be a Category instance')

    if not isinstance(vendor, Vendor):
        raise InvalidValueException(Recipe, 'vendor must be a Vendor instance')

    if not isinstance(language, Language):
        raise InvalidValueException(Recipe, 'language must be a Language instance')

    if not isinstance(image_url, str):
        raise InvalidValueException(Recipe, 'image_urls must be a list of strings')

    if not isinstance(ingredients, list):
        raise InvalidValueException(Recipe, 'ingredients must be a list of strings')

    author_object = Author(name=author)
    recipe_url_object = RecipeURL(url=url, vendor_pattern=vendor.recipe_pattern) if vendor is not None else None
    image_url_object = URL(url=image_url)
    aggregate_rating_object = AggregateRating(rating_count=rating_count, rating_value=rating_value)

    return Recipe(
        recipe_id=recipe_id,
        name=name,
        description=description,
        author=author_object,
        prep_time=prep_time,
        cook_time=cook_time,
        total_time=total_time,
        date_published=date_published,
        url=recipe_url_object,
        category=category,
        vendor=vendor,
        language=language,
        aggregate_rating=aggregate_rating_object,
        image=image_url_object,
        ingredients=ingredients,
    )


def create_recipe_from_structured_data(structured_data: dict, url: str, vendor: Vendor, language: Language) -> Recipe:
    def get_attribute(attribute: str):
        return structured_data.get(attribute, None)

    return create_recipe(
        recipe_id=uuid4(),  # TODO: don't know if this is the best place to init it, but it has to be done somewhere
        name=get_attribute('name'),
        description=get_attribute('description'),
        author=structured_data.get('author', dict()).get('name'),
        prep_time=timedelta(minutes=10),  # TODO: not contained in structured data :(
        cook_time=timedelta(minutes=10),  # TODO: not contained in structured data :(
        total_time=timedelta(minutes=10),  # TODO: not contained in structured data :(
        date_published=datetime.strptime(get_attribute('datePublished'), '%Y-%m-%d'),
        url=url,
        category=list(filter(lambda category: category.name == get_attribute('recipeCategory'), vendor.categories))[0],  # TODO: not the best option...
        vendor=vendor,
        language=language,  # TODO: how do we get this?
        rating_count=structured_data.get('aggregateRating', dict()).get('ratingCount') or 0,
        rating_value=structured_data.get('aggregateRating', dict()).get('ratingValue') or 0.0,
        image_url=get_attribute('image'),
        ingredients=[create_ingredient(ingredient_id=uuid4(), text=ingredient) for ingredient in get_attribute('recipeIngredient')],
    )
