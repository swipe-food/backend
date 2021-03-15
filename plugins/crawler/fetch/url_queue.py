from typing import List


class URLQueue:

    def __init__(self, urls: List[str] = None):
        self.urls = urls if urls else list()
