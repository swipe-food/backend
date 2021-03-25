from abc import abstractmethod, ABC

from common.domain.repositories import AbstractBaseRepository
from crawler_context.domain.model.ingredient_aggregate import Ingredient


class AbstractIngredientRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, ingredient_name: str) -> Ingredient:
        raise NotImplementedError
