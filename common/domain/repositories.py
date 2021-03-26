import uuid
from abc import ABC, abstractmethod
from typing import List

from common.domain.model.base import Entity


class AbstractBaseRepository(ABC):

    def __init__(self, db_connection):
        self._db_connection = db_connection

    @abstractmethod
    def add(self, entity: Entity):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: uuid.UUID) -> Entity:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Entity]:
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity):
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity: Entity):
        raise NotImplementedError
