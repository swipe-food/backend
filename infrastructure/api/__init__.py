from flask import Flask

from flask_restplus import Api
from flask_cors import CORS

from infrastructure.api.routers import VendorRouter

__all__ = ['FoodSwipeAPI']

from infrastructure.config import ApiConfig


class FoodSwipeAPI(Flask):
    routers = {
        '/vendors': VendorRouter,
    }
    error_handlers = {

    }

    def __init__(self, config: ApiConfig):
        super().__init__(
            config.name,
            root_path=config.root_path,
        )
        self._api = Api(self)
        self.api_config = config
        self.cors = CORS(self, resources={r"*": {"origins": config.host + "/*"}})
        self._register_routers()

    def run(self, host=None, port=None, debug=None, **options):
        super().run(
            host or self.api_config.host,
            port or self.api_config.port,
            debug or self.api_config.debug,
            threaded=True,
            **options)

    @property
    def api(self) -> Api:
        return self._api

    def _register_routers(self):
        for prefix, router in self.routers.items():
            self.api.add_namespace(router(), prefix)

    def _register_error_handlers(self):
        for error, handler in self.error_handlers.items():
            self._register_error_handler(key=None, code_or_exception=error, f=handler)
