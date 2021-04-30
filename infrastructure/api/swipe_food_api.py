from typing import Dict, Callable

from flask import Flask, request
from flask_cors import CORS
from flask_restplus import Api
from werkzeug.exceptions import HTTPException

from domain.repositories.base import AbstractBaseRepository
from domain.services.base import AbstractBaseService
from infrastructure.api.exceptions_handlers import ApiException
from infrastructure.api.routers import VendorRouter, StatusRouter, AbstractRouter
from infrastructure.config import ApiConfig
from infrastructure.log import Logger


class SwipeFoodAPI(Flask):
    routers: Dict[str, type(AbstractRouter)] = {
        '/vendors': VendorRouter,
        '/status': StatusRouter,
    }
    error_handlers: Dict[Exception, Callable] = {
        ApiException: ApiException.handle,
        HTTPException: ApiException.handle,
    }

    def __init__(self, config: ApiConfig, logger: Logger, repositories: Dict[str, type(AbstractBaseRepository)], services: Dict[str, type(AbstractBaseService)]):
        super().__init__(config.name)
        self.api = Api(self)
        self.api_config = config
        self.api_prefix = '/api'
        self.cors = CORS(self, resources={r"*": {"origins": self.api_config.host + "/*"}})

        self.logger = logger
        self.repositories = repositories
        self.services = services

        self._register_request_setups()
        self._register_routers()
        self._register_error_handlers()

    def run(self, host=None, port=None, debug=None, **options):
        super().run(
            host or self.api_config.host,
            port or self.api_config.port,
            debug or self.api_config.debug,
            threaded=True,
            **options
        )

    def _register_request_setups(self):
        self.before_request(self._insert_data_to_request(dict(
            logger=self.logger,
            repositories=self.repositories,
            services=self.services,
        )))

    def _register_routers(self):
        for prefix, router in self.routers.items():
            self.api.add_namespace(router(), f'{self.api_prefix}{prefix}')

    def _register_error_handlers(self):
        for error, handler in self.error_handlers.items():
            self.register_error_handler(code_or_exception=error, f=handler)

    @staticmethod
    def _insert_data_to_request(data: Dict[str, any]) -> Callable:
        def before_request_function():
            for attribute_name, attribute in data.items():
                setattr(request, attribute_name, attribute)

        return before_request_function
