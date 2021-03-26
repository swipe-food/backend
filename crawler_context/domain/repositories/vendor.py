from abc import abstractmethod, ABC

from common.domain.repositories import AbstractBaseRepository
from crawler_context.domain.model.vendor_aggregate import Vendor


class AbstractVendorRepository(AbstractBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError
