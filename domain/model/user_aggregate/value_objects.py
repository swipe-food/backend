class EMail:

    @classmethod
    def from_text(cls, address: str):
        if '@' not in address:
            raise ValueError("EMail address must contain '@'")
        local_part, _, domain_part = address.partition('@')
        return cls(local_part, domain_part)

    def __init__(self, local_part: str, domain_part: str):
        self._parts = (local_part, domain_part)

    def __str__(self) -> str:
        return '@'.join(self._parts)

    def __repr__(self) -> str:
        return 'EMail(local_part={!r}, domain_part={!r})'.format(*self._parts)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, EMail):
            return NotImplemented  # TODO check if this approach is good
        return self._parts == o._parts

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    @property
    def local(self):
        return self._parts[0]

    @property
    def domain(self):
        return self._parts[1]

    def replace(self, local_part: str = None, domain_part: str = None):
        return EMail(local_part=local_part or self._parts[0],
                     domain_part=domain_part or self._parts[1])
