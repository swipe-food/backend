from __future__ import annotations

from domain.exceptions import InvalidValueException
from domain.services.status import AbstractStatusService
from infrastructure.config import AppConfig


def create_status_service(config: AppConfig) -> StatusService:
    if not isinstance(config, AppConfig):
        raise InvalidValueException(StatusService, 'config must be a AppConfig')
    return StatusService(config=config)


class StatusService(AbstractStatusService):

    def __init__(self, config: AppConfig):
        self._build_commit = config.build_commit
        self._build_time = config.build_time

    def get_build_commit(self):
        return self._build_commit

    def get_build_time(self):
        return self._build_time
