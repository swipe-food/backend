import uuid
from abc import ABC, abstractmethod
from typing import List

from domain.model.base import Entity


class AbstractBaseRepository(ABC):

    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, limit: int = None) -> List[Entity]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: Entity):
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: Entity):
        raise NotImplementedError
