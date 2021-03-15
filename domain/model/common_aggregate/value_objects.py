class URL:
    VALID_SCHEMES = ['http', 'https']

    @classmethod
    def from_text(cls, url: str):
        # TODO validate
        scheme, domain, resource, parameters = url, url, url, url
        return cls(scheme, domain, resource, parameters)

    def __init__(self, scheme: str, domain: str, resource: str, parameters: str):
        self._parts = (scheme, domain, resource, parameters)

    def __str__(self) -> str:
        return f'{self._parts[0]}//{self._parts[1]}{self._parts[2]}{self._parts[3]}'

    def __repr__(self) -> str:
        return '{c}(url={url!r})'.format(
            c=self.__class__.__name__,
            url=self.__str__(),
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return NotImplemented  # TODO check if this approach is good
        return self._parts == o._parts

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    def replace(self, scheme: str = None, domain: str = None, resource: str = None, parameters: str = None):
        return URL(scheme=scheme or self._parts[0],
                   domain=domain or self._parts[1],
                   resource=resource or self._parts[2],
                   parameters=parameters or self._parts[3])