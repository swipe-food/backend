import uuid
from abc import abstractmethod
from typing import List

from domain.model.match_aggregate import Match
from domain.services.base import AbstractBaseService


class AbstractMatchService(AbstractBaseService):

    @abstractmethod
    def add(self, match_data: dict) -> Match:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, match_id: uuid.UUID) -> Match:
        raise NotImplementedError

    @abstractmethod
    def update(self, match_id: uuid.UUID, match_data: dict) -> Match:
        raise NotImplementedError

    @abstractmethod
    def delete(self, match_id: uuid.UUID):
        raise NotImplementedError
