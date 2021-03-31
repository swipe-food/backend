from abc import ABC

from common.domain.repositories import AbstractQueryBaseRepository, AbstractCommandBaseRepository


class AbstractMatchRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):
    pass
