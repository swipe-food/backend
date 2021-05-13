from abc import abstractmethod


class AbstractStatusService:

    @abstractmethod
    def get_build_commit(self):
        raise NotImplementedError

    @abstractmethod
    def get_build_time(self):
        raise NotImplementedError
