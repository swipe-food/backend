from abc import ABC

from common.domain.repositories import AbstractQueryBaseRepository, AbstractCommandBaseRepository


class AbstractCategoryLikeRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):
    pass
