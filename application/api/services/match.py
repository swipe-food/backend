from __future__ import annotations

import uuid

from domain.exceptions import InvalidValueException
from domain.model.match_aggregate import Match, create_match
from domain.repositories.match import AbstractMatchRepository
from domain.repositories.recipe import AbstractRecipeRepository
from domain.repositories.user import AbstractUserRepository
from domain.services.match import AbstractMatchService


def create_match_service(match_repo: AbstractMatchRepository, user_repo: AbstractUserRepository,
                         recipe_repo: AbstractRecipeRepository) -> MatchService:
    if not isinstance(match_repo, AbstractMatchRepository):
        raise InvalidValueException(MatchService, 'match_repo must be a AbstractMatchRepository')
    if not isinstance(user_repo, AbstractUserRepository):
        raise InvalidValueException(MatchService, 'user_repo must be a AbstractUserRepository')
    if not isinstance(recipe_repo, AbstractRecipeRepository):
        raise InvalidValueException(MatchService, 'recipe_repo must be a AbstractRecipeRepository')
    return MatchService(match_repo=match_repo, user_repo=user_repo, recipe_repo=recipe_repo)


class MatchService(AbstractMatchService):

    def __init__(self, match_repo: AbstractMatchRepository, user_repo: AbstractUserRepository, recipe_repo: AbstractRecipeRepository):
        self._match_repo = match_repo
        self._user_repo = user_repo
        self._recipe_repo = recipe_repo

    def get_by_id(self, match_id: uuid.UUID) -> Match:
        return self._match_repo.get_by_id(match_id)

    def add(self, match_data: dict) -> Match:
        user = self._user_repo.get_by_id(match_data['user_id'])
        recipe = self._recipe_repo.get_by_id(match_data['recipe_id'])

        match = create_match(match_id=uuid.uuid4(),
                             user=user, recipe=recipe,
                             timestamp=match_data['timestamp'],
                             is_seen_by_user=match_data['is_seen_by_user'],
                             is_active=match_data['is_active']
                             )
        self._match_repo.add(match)
        return match

    def update(self, match_id: uuid.UUID, match_data: dict) -> Match:
        match = self._match_repo.get_by_id(match_id)
        if 'is_active' in match_data:
            match.is_active = match_data['is_active']
        if 'is_seen_by_user' in match_data:
            match.is_seen_by_user = match_data['is_seen_by_user']

        self._match_repo.update(match)
        return match

    def delete(self, match_id: uuid.UUID):
        match = self._match_repo.get_by_id(match_id)
        return self._match_repo.delete(match)
