from urllib.parse import urlparse


class URL:
    VALID_SCHEMES = ['http', 'https']

    @classmethod
    def from_text(cls, url: str):
        scheme, netloc, path, query = cls._parse(url)

        if scheme not in cls.VALID_SCHEMES or netloc == '':
            raise ValueError(f'Invalid {cls.__class__.__name__} {url}')

        return cls(scheme, netloc, path, query)

    @classmethod
    def _parse(cls, url: str):
        tokens = urlparse(url)
        scheme = getattr(tokens, 'scheme')
        netloc = getattr(tokens, 'netloc')
        path = getattr(tokens, 'path')
        query = getattr(tokens, 'query')
        return scheme, netloc, path, query

    def __init__(self, scheme: str, netloc: str, path: str, query: str):
        self._parts = (scheme, netloc, path, query)

    def __str__(self) -> str:
        return f'{self._parts[0]}://{self._parts[1]}{self._parts[2]}{self._parts[3]}'

    def __repr__(self) -> str:
        return '{c}(url={url!r})'.format(
            c=self.__class__.__name__,
            url=self.__str__(),
        )

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return NotImplemented
        return self._parts == o._parts

    def __ne__(self, o: object) -> bool:
        return not (self == o)

    @property
    def parts(self):
        return self._parts

    def replace(self, scheme: str = None, netloc: str = None, path: str = None, query: str = None):
        return URL(scheme=scheme or self._parts[0],
                   netloc=netloc or self._parts[1],
                   path=path or self._parts[2],
                   query=query or self._parts[3])