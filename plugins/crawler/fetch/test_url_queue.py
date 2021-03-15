from plugins.crawler.fetch.url_queue import URLQueue


class TestUrlQueue:
    test_urls = [
        'https://www.python.org/',
        'https://xkcd.com/',
    ]

    @classmethod
    def url_queue(cls) -> URLQueue:
        return URLQueue()

    @classmethod
    def test_create_empty_url_queue(cls, url_queue: URLQueue):
        assert url_queue.urls == list()

    @classmethod
    def test_create_filled_url_queue(cls):
        url_queue = URLQueue(cls.test_urls)
        assert url_queue.urls == cls.test_urls

    @classmethod
    def test_fill_url_queue(cls, url_queue: URLQueue):
        url_queue.add(cls.test_urls)
        assert url_queue.urls == cls.test_urls

    @classmethod
    def test_add_url_to_queue(cls, url_queue: URLQueue):
        new_url = 'https://code-specialist.com'
        previous_length = len(url_queue.urls)
        url_queue.add(new_url)
        assert len(url_queue.urls) == previous_length + 1
        assert 'https://code-specialist.com' in url_queue.urls

    @classmethod
    def test_url_queue_builtin_add(cls, url_queue: URLQueue):
        new_url = 'https://code-specialist.com'
        previous_length = len(url_queue.urls)
        url_queue += new_url
        assert len(url_queue.urls) == previous_length + 1
        assert 'https://code-specialist.com' in url_queue.urls

    @classmethod
    def test_url_queue_clear(cls, url_queue: URLQueue):
        url_queue.add(cls.test_urls)
        url_queue.clear()
        assert url_queue.urls == list()

    @classmethod
    def test_url_queue_len(cls, url_queue: URLQueue):
        assert len(url_queue) == 0
        url_queue.add(cls.test_urls)
        assert len(url_queue) == len(cls.test_urls)

    @classmethod
    def test_url_queue_is_empty_true(cls, url_queue: URLQueue):
        assert url_queue.is_empty()

    @classmethod
    def test_url_queue_is_empty_false(cls, url_queue: URLQueue):
        url_queue.add(cls.test_urls)
        assert not url_queue.is_empty()

    @classmethod
    def test_url_queue_bool_true(cls, url_queue: URLQueue):
        url_queue.add(cls.test_urls)
        assert url_queue

    @classmethod
    def test_url_queue_bool_false(cls, url_queue: URLQueue):
        assert not url_queue
