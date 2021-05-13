from abc import abstractmethod, ABC

from domain.model.recipe_aggregate import Recipe
from domain.services.base import AbstractQueryService


class AbstractRecipeService(AbstractQueryService, ABC):

    @abstractmethod
    def get_by_name(self, recipe_name: str) -> Recipe:
        raise NotImplementedError
