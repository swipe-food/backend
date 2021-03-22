from abc import abstractmethod
from typing import List

from common.domain.repositories import AbstractBaseRepository
from crawler_context.domain.model.category_aggregate import Category
from crawler_context.domain.model.vendor_aggregate import Vendor


class AbstractCategoryRepository(AbstractBaseRepository):

    @abstractmethod
    def get_by_name(self, category_name: str) -> Category:
        raise NotImplementedError

    @abstractmethod
    def get_vendors(self, category: Category) -> List[Vendor]:
        raise NotImplementedError
