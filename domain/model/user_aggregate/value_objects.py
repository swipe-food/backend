import re


class EMail:
    VALIDATION_REGEX = "[^@]+@[^@]+\.[^@]+"

    @classmethod
    def from_text(cls, email_address: str):
        pattern = re.compile(cls.VALIDATION_REGEX)
        if not pattern.match(email_address):
            raise ValueError(f"Invalid {cls.__class__.__name__} '{email_address}'")
        local_part, _, domain_part = email_address.partition('@')
        return cls(local_part, domain_part)

    def __init__(self, local_part: str, domain_part: str):
        self._parts = (local_part, domain_part)

    def __str__(self) -> str:
        return '@'.join(self._parts)

    def __repr__(self) -> str:
        return 'EMail(local_part={!r}, domain_part={!r})'.format(*self._parts)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, EMail):
            return NotImplemented
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
