from __future__ import annotations

import uuid

from domain.exceptions import InvalidValueException
from domain.model.match_aggregate import Match, create_match
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
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

    def __init__(self, match_repo: AbstractMatchRepository, user_repo: AbstractUserRepository,
                 recipe_repo: AbstractRecipeRepository):
        self._match_repo = match_repo
        self._user_repo = user_repo
        self._recipe_repo = recipe_repo

    def get_by_id(self, entity_id: uuid.UUID) -> Match:
        return self._match_repo.get_by_id(entity_id)

    def add(self, entity_data: dict) -> Match:
        user: User = self._user_repo.get_by_id(entity_data['user_id'])
        recipe: Recipe = self._recipe_repo.get_by_id(entity_data['recipe_id'])

        match = create_match(match_id=uuid.uuid4(),
                             user=user, recipe=recipe,
                             timestamp=entity_data['timestamp'],
                             is_seen_by_user=entity_data['is_seen_by_user'],
                             is_active=entity_data['is_active']
                             )

        # TODO handle category like matches
        self._match_repo.add(match)
        return match

    def update(self, entity_id: uuid.UUID, entity_data: dict) -> Match:
        match = self.get_by_id(entity_id)
        if 'is_active' in entity_data:
            match.is_active = entity_data['is_active']
        if 'is_seen_by_user' in entity_data:
            match.is_seen_by_user = entity_data['is_seen_by_user']

        self._match_repo.update(match)
        return match

    def delete(self, match_id: uuid.UUID):
        match = self.get_by_id(match_id)
        match.delete()
        return self._match_repo.delete(match)
