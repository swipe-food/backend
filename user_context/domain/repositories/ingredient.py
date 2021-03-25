from abc import ABC, abstractmethod

from common.domain.repositories import AbstractBaseRepository
from user_context.domain.model.ingredient_aggregate import Ingredient


class AbstractCategoryRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, ingredient_name: str) -> Ingredient:
        raise NotImplementedError
