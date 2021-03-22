from abc import abstractmethod

from domain.repositories.base import AbstractRepository


class AbstractCategoryRepository(AbstractRepository):

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get_by_name(self):
        raise NotImplementedError

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError
