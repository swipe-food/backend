from abc import abstractmethod, ABC

from common.domain.repositories import AbstractBaseRepository
from user_context.domain.model.user_aggregate import User


class AbstractUserRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def add_languages(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def add_seen_recipes(self, user: User):
        raise NotImplementedError
