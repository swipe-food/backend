from abc import abstractmethod

from common.domain.repositories import AbstractBaseRepository
from crawler_context.domain.model.vendor_aggregate import Vendor


class AbstractVendorRepository(AbstractBaseRepository):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError
