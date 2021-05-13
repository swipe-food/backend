from abc import abstractmethod, ABC
from typing import List

from domain.model.language_aggregate import Language
from domain.services.base import AbstractQueryService


class AbstractLanguageService(AbstractQueryService, ABC):

    @abstractmethod
    def get_all(self, limit: int) -> List[Language]:
        raise NotImplementedError
