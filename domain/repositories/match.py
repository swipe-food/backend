from abc import ABC

from domain.repositories.base import AbstractQueryBaseRepository, AbstractCommandBaseRepository


class AbstractMatchRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):
    pass
