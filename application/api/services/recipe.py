from __future__ import annotations

import uuid

from domain.exceptions import InvalidValueException
from domain.model.recipe_aggregate import Recipe
from domain.repositories.recipe import AbstractRecipeRepository
from domain.services.recipe import AbstractRecipeService


def create_recipe_service(recipe_repo: AbstractRecipeRepository) -> RecipeService:
    if not isinstance(recipe_repo, AbstractRecipeRepository):
        raise InvalidValueException(RecipeService, 'recipe_repo must be a AbstractRecipeRepository')
    return RecipeService(recipe_repo=recipe_repo)


class RecipeService(AbstractRecipeService):

    def __init__(self, recipe_repo: AbstractRecipeRepository):
        self._recipe_repo = recipe_repo

    def get_by_id(self, recipe_id: uuid.UUID) -> Recipe:
        return self._recipe_repo.get_by_id(recipe_id)

    def get_by_name(self, recipe_name: str) -> Recipe:
        return self._recipe_repo.get_by_name(recipe_name)
