from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from domain.model import vendor_aggregate, category_aggregate, user_aggregate, match_aggregate, recipe_aggregate
from domain.model.common_aggregate import create_entity_id, Language


def create_language(version: int, name: str, code: str):
    if len(code) != 2:
        raise ValueError('Language Acronym must have a length of 2')
    return Language(language_id=create_entity_id(),
                    language_version=version,
                    name=name,
                    code=code)


def create_category(version: int, name: str, vendor: vendor_aggregate.Vendor) -> category_aggregate.Category:
    return category_aggregate.Category(category_id=create_entity_id(),
                                       category_version=version,
                                       name=name,
                                       vendor=vendor)


def create_vendor(version: int, name: str, description: str, url: str, is_active: bool, date_last_crawled: datetime,
                  languages: List[Language], recipe_pattern: str) -> vendor_aggregate.Vendor:
    return vendor_aggregate.Vendor(vendor_id=create_entity_id(),
                                   vendor_version=version,
                                   name=name,
                                   description=description,
                                   url=vendor_aggregate.URL.from_text(url),
                                   is_active=is_active,
                                   date_last_crawled=date_last_crawled,
                                   languages=languages,
                                   recipe_pattern=recipe_pattern)


def create_user(version: int, name: str, first_name: str, email: str, is_confirmed: bool, date_last_login: datetime,
                languages: List[Language]) -> user_aggregate.User:
    return user_aggregate.User(user_id=create_entity_id(),
                               user_version=version,
                               name=name,
                               first_name=first_name,
                               email=user_aggregate.EMail.from_text(email),
                               is_confirmed=is_confirmed,
                               date_last_login=date_last_login,
                               languages=languages)


def create_category_like(version: int, user: user_aggregate.User, category: category_aggregate.Category, views: int,
                         matches: int) -> user_aggregate.CategoryLike:
    return user_aggregate.CategoryLike(liked_category_id=create_entity_id(),
                                       liked_category_version=version,
                                       user=user,
                                       category=category,
                                       views=views,
                                       matches=matches)


def create_image_url(version: int, url: str) -> recipe_aggregate.ImageURL:
    # TODO validate
    scheme, domain, resource, parameters = url, url, url, url
    return recipe_aggregate.ImageURL(image_url_id=create_entity_id(),
                                     image_url_version=version,
                                     scheme=scheme,
                                     domain=domain,
                                     resource=resource,
                                     parameters=parameters)


def create_ingredient(version: int, text: str) -> recipe_aggregate.Ingredient:
    return recipe_aggregate.Ingredient(ingredient_id=create_entity_id(),
                                       ingredient_version=version,
                                       text=text)


def create_recipe(version: int, name: str, description: str, vendor_id: str, recipe_url: str,
                  images: List[recipe_aggregate.ImageURL],
                  ingredients: List[recipe_aggregate.Ingredient], aggregate_rating: recipe_aggregate.AggregateRating,
                  category: category_aggregate.Category, vendor: vendor_aggregate.Vendor,
                  language: Language, prep_time: timedelta = None,
                  cook_time: timedelta = None, total_time: timedelta = None) -> recipe_aggregate.Recipe:
    return recipe_aggregate.Recipe(recipe_id=create_entity_id(),
                                   recipe_version=version,
                                   name=name,
                                   description=description,
                                   vendor_id=vendor_id,
                                   prep_time=prep_time,
                                   cook_time=cook_time,
                                   total_time=total_time,
                                   url=recipe_aggregate.RecipeURL.from_text_with_pattern(recipe_url,
                                                                                         vendor.recipe_pattern),
                                   images=images,
                                   ingredients=ingredients,
                                   category=category,
                                   aggregate_rating=aggregate_rating,
                                   language=language,
                                   vendor=vendor)


def create_match(version: int, user: user_aggregate.User, recipe, timestamp: datetime, is_seen_by_user: bool,
                 is_active: bool) -> match_aggregate.Match:
    return match_aggregate.Match(match_id=create_entity_id(),
                                 match_version=version,
                                 user=user,
                                 recipe=recipe,
                                 timestamp=timestamp,
                                 is_seen_by_user=is_seen_by_user,
                                 is_active=is_active)
