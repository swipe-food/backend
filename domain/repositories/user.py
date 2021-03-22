from abc import abstractmethod

from common.domain import AbstractBaseRepository
from domain.model.user_aggregate import User


class AbstractUserRepository(AbstractBaseRepository):

    @abstractmethod
    def get_by_email(self, email: str) -> User:
        raise NotImplementedError
