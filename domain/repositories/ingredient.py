from abc import ABC, abstractmethod

from domain.model.ingredient_aggregate import Ingredient
from domain.repositories.base import AbstractQueryBaseRepository, AbstractCommandBaseRepository


class AbstractCategoryRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, ingredient_name: str) -> Ingredient:
        raise NotImplementedError
