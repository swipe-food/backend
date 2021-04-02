from abc import ABC

from domain.repositories.base import AbstractQueryBaseRepository, AbstractCommandBaseRepository


class AbstractCategoryLikeRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):
    pass
