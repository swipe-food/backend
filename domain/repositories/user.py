from abc import abstractmethod, ABC

from domain.model.language_aggregate import Language
from domain.model.recipe_aggregate import Recipe
from domain.model.user_aggregate import User
from domain.repositories.base import AbstractBaseRepository


class AbstractUserRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def add_language(self, user: User, language: Language):
        raise NotImplementedError

    @abstractmethod
    def remove_language(self, user: User, language: Language):
        raise NotImplementedError

    @abstractmethod
    def add_seen_recipe(self, user: User, recipe: Recipe):
        raise NotImplementedError
