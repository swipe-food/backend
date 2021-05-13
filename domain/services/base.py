import uuid
from abc import ABC, abstractmethod

from domain.model.base import Entity


class AbstractQueryService(ABC):

    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> Entity:
        raise NotImplementedError


class AbstractCommandService(ABC):

    @abstractmethod
    def add(self, entity_data: dict) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity_id: uuid.UUID, entity_data: dict) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id: uuid.UUID):
        raise NotImplementedError
