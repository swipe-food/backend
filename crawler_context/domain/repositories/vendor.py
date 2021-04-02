from abc import abstractmethod, ABC

from common.domain.repositories import AbstractQueryBaseRepository, AbstractCommandBaseRepository
from crawler_context.domain.model.vendor_aggregate import Vendor


class AbstractVendorRepository(AbstractQueryBaseRepository, AbstractCommandBaseRepository, ABC):

    @abstractmethod
    def get_by_name(self, vendor_name: str) -> Vendor:
        raise NotImplementedError
