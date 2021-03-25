from abc import abstractmethod, ABC

from common.domain.repositories import AbstractBaseRepository
from user_context.domain.model.user_aggregate import User


class AbstractUserRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError
