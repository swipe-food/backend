from datetime import datetime
from typing import List
from uuid import UUID

from common.exceptions import InvalidValueError
from user_context.domain.model.category_like_aggregate import CategoryLike
from user_context.domain.model.language_aggregate import Language
from user_context.domain.model.match_aggregate import Match
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate.user import User
from user_context.domain.model.user_aggregate.value_objects import EMail


def create_user(user_id: UUID, name: str, first_name: str, email: str, is_confirmed: bool, date_last_login: datetime,
                liked_categories: List[CategoryLike], matches: List[Match], seen_recipes: List[Recipe],
                languages: List[Language]) -> User:
    if not isinstance(liked_categories, list):
        raise InvalidValueError(User, 'liked_categories must be a list of Category instances')

    if not isinstance(matches, list):
        raise InvalidValueError(User, 'matches must be a list of Recipe instances')

    if not isinstance(seen_recipes, list):
        raise InvalidValueError(User, 'seen_recipes must be a list of Recipe instances')

    if not isinstance(languages, list):
        raise InvalidValueError(User, 'languages must be a list of Language instances')

    user_email_object = EMail(email)

    return User(
        user_id=user_id,
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
