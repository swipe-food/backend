from abc import abstractmethod, ABC
from typing import List

from common.domain.repositories import AbstractQueryBaseRepository, AbstractCommandBaseRepository
from crawler_context.domain.model.category_aggregate import Category
from crawler_context.domain.model.vendor_aggregate import Vendor


class AbstractCategoryRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, category_name: str) -> Category:
        raise NotImplementedError

    @abstractmethod
    def get_vendors(self, category: Category) -> List[Vendor]:
        raise NotImplementedError
