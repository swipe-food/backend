from abc import abstractmethod

from domain.services.base import AbstractBaseService


class AbstractStatusService(AbstractBaseService):

    @abstractmethod
    def get_build_commit(self):
        raise NotImplementedError

    @abstractmethod
    def get_build_time(self):
        raise NotImplementedError
