from datetime import datetime

from domain.model.match_aggregate.entities import Match
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User


def create_match(user: User, recipe: Recipe, timestamp: datetime, is_seen_by_user: bool, is_active: bool) -> Match:
    return Match(
        user=user,
        recipe=recipe,
        timestamp=timestamp,
        is_seen_by_user=is_seen_by_user,
        is_active=is_active
    )
