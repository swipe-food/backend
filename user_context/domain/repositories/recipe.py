from abc import abstractmethod, ABC
from typing import List

from common.domain.repositories import AbstractQueryBaseRepository
from user_context.domain.model.recipe_aggregate import Recipe
from user_context.domain.model.user_aggregate import User


class AbstractRecipeRepository(AbstractQueryBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, recipe_name: str) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def get_matched_users(self, recipe: Recipe) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_unseen_recipes_for_user(self, user: User, limit: int = 20) -> List[Recipe]:
        raise NotImplementedError
