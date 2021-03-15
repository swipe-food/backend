from datetime import datetime

from domain.model.common_aggregate import create_entity_id
from domain.model.match_aggregate.entities import Match
from domain.model.user_aggregate import User


def create_match(version: int, user: User, recipe, timestamp: datetime, is_seen_by_user: bool,
                 is_active: bool) -> Match:
    return Match(match_id=create_entity_id(),
                 match_version=version,
                 user=user,
                 recipe=recipe,
                 timestamp=timestamp,
                 is_seen_by_user=is_seen_by_user,
                 is_active=is_active)
