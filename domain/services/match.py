import uuid
from abc import abstractmethod, ABC
from typing import List

from domain.model.match_aggregate import Match
from domain.services.base import AbstractQueryService


class AbstractMatchService(AbstractQueryService, ABC):
    pass
