from domain.model.common_aggregate import URL


class RecipeURL(URL):

    @classmethod
    def from_text_with_pattern(cls, url: str, vendor_pattern: str):
        # TODO validate with pattern of vendor
        scheme, domain, resource, parameters = url, url, url, url
        return cls(scheme, domain, resource, parameters)

    def __init__(self, scheme: str, domain: str, resource: str, parameters: str):
        super().__init__(scheme, domain, resource, parameters)

    def replace(self, scheme: str = None, domain: str = None, resource: str = None, parameters: str = None):
        return RecipeURL(scheme=scheme or self._parts[0],
                         domain=domain or self._parts[1],
                         resource=resource or self._parts[2],
                         parameters=parameters or self._parts[3])


class AggregateRating:
    # TODO check how to best implement this
    def __init__(self, rating_count: int, rating_value: float):
        pass
