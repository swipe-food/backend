from abc import abstractmethod
from typing import List

from common.domain import AbstractBaseRepository
from user_context.domain import Recipe
from user_context.domain import User


class AbstractRecipeRepository(AbstractBaseRepository):

    @abstractmethod
    def get_by_name(self, recipe_name: str) -> Recipe:
        raise NotImplementedError

    @abstractmethod
    def get_matched_users(self, recipe: Recipe) -> List[User]:
        raise NotImplementedError
