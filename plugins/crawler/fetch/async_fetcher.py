from dataclasses import dataclass


@dataclass
class FetchResult:
    url: str
    status: int
    html: str


class AsyncFetcher:
    pass
