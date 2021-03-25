from abc import abstractmethod, ABC

from common.domain.repositories import AbstractBaseRepository
from crawler_context.domain.model.recipe_aggregate import Recipe


class AbstractRecipeRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, recipe_name: str) -> Recipe:
        raise NotImplementedError
