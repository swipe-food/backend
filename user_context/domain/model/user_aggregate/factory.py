from datetime import datetime
from typing import List

from common.domain.value_objects import Language
from user_context.domain.model.category_aggregate import Category
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate import EMail
from user_context.domain.model.user_aggregate.user import User


def create_user(name: str, first_name: str, email: str, is_confirmed: bool, date_last_login: datetime,
                liked_categories: List[Category], matches: List[Recipe], seen_recipes: List[Recipe],
                languages: List[Language]) -> User:
    if not isinstance(liked_categories, list):
        raise ValueError('liked_categories must be a list of Category instances')

    if not isinstance(matches, list):
        raise ValueError('matches must be a list of Recipe instances')

    if not isinstance(seen_recipes, list):
        raise ValueError('seen_recipes must be a list of Recipe instances')

    if not isinstance(languages, list):
        raise ValueError('languages must be a list of Language instances')

    user_email_object = EMail(email)

    return User(
        name=name,
        first_name=first_name,
        email=user_email_object,
        is_confirmed=is_confirmed,
        date_last_login=date_last_login,
        liked_categories=liked_categories,
        matches=matches,
        seen_recipes=seen_recipes,
        languages=languages,
    )
