import pytest

from application.crawler.fetch.url_queue import URLQueue


class TestUrlQueue:
    test_urls = [
        'https://www.python.org/',
        'https://xkcd.com/',
    ]

    @staticmethod
    @pytest.fixture
    def url_queue() -> URLQueue:
        return URLQueue()

    def test_create_empty_url_queue(self, url_queue: URLQueue):
        assert url_queue.urls == list()

    def test_create_filled_url_queue(self):
        url_queue = URLQueue(self.test_urls)
        assert url_queue.urls == self.test_urls

    def test_fill_url_queue(self, url_queue: URLQueue):
        url_queue.add(self.test_urls)
        assert url_queue.urls == self.test_urls

    def test_add_url_to_queue(self, url_queue: URLQueue):
        new_url = 'https://code-specialist.com'
        previous_length = len(url_queue.urls)
        url_queue.add(new_url)
        assert len(url_queue.urls) == previous_length + 1
        assert 'https://code-specialist.com' in url_queue.urls

    def test_url_queue_builtin_add(self, url_queue: URLQueue):
        new_url = 'https://code-specialist.com'
        previous_length = len(url_queue.urls)
        url_queue += new_url
        assert len(url_queue.urls) == previous_length + 1
        assert 'https://code-specialist.com' in url_queue.urls

    def test_url_queue_add_fail(self, url_queue: URLQueue):
        with pytest.raises(ValueError):
            url_queue.add(42)

    def test_url_queue_clear(self, url_queue: URLQueue):
        url_queue.add(self.test_urls)
        url_queue.clear()
        assert url_queue.urls == list()

    def test_url_queue_len(self, url_queue: URLQueue):
        assert len(url_queue) == 0
        url_queue.add(self.test_urls)
        assert len(url_queue) == len(self.test_urls)

    def test_url_queue_is_empty_true(self, url_queue: URLQueue):
        assert url_queue.is_empty()

    def test_url_queue_is_empty_false(self, url_queue: URLQueue):
        url_queue.add(self.test_urls)
        assert not url_queue.is_empty()

    def test_url_queue_bool_true(self, url_queue: URLQueue):
        url_queue.add(self.test_urls)
        assert url_queue

    def test_url_queue_bool_false(self, url_queue: URLQueue):
        assert not url_queue

    def test_process_url_queue(self, url_queue: URLQueue):
        url_queue.add(self.test_urls)
        for url in url_queue:
            assert url in self.test_urls
        assert url_queue.is_empty()
