from abc import ABC, abstractmethod

from common.domain.model.ingredient_aggregate import Ingredient
from common.domain.repositories import AbstractQueryBaseRepository


class AbstractCategoryRepository(AbstractQueryBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, ingredient_name: str) -> Ingredient:
        raise NotImplementedError
