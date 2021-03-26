from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import get_type_hints, Any

from dotenv import dotenv_values

from common.exceptions import MissingConfigError, InvalidValueError

PROJECT_ROOT_DIR = Path(__file__).parent.parent


class ConfigParser:

    @classmethod
    def _parse_component(cls, config: dict, obj: ConfigComponent) -> ConfigComponent:
        for field in obj.__annotations__:
            field_type = get_type_hints(obj.__class__)[field]

            if issubclass(field_type, ConfigComponent):
                value = cls.parse(config, field_type())
            else:
                value = cls._parse_value(config, field.upper(), field_type)
            obj.__setattr__(field, value)
        return obj

    @classmethod
    def _parse_value(cls, config: dict, field: str, field_type: Any) -> Any:
        value = config.get(field)
        if value is None:
            raise MissingConfigError(cls, f"Required Config field '{field}' cannot be None")
        try:
            if issubclass(field_type, bool):
                return value == 'True'
            return field_type(value)
        except ValueError:
            raise InvalidValueError(cls, f"Config field '{field}' has an invalid value '{value}' for type {field_type}")

    @classmethod
    def parse(cls, config: dict, field_type: ConfigComponent) -> ConfigComponent:
        filtered_config = {k.split(field_type.PREFIX)[1]: v for (k, v) in config.items() if field_type.PREFIX in k}
        return cls._parse_component(config=filtered_config, obj=field_type)


class ConfigComponent(ABC):
    PREFIX = 'PREFIX_'

    @classmethod
    def load_and_parse(cls, env_file_path: str) -> ConfigComponent:
        config = dotenv_values(env_file_path)

        return ConfigParser.parse(config, cls())

    def __str__(self):
        repr_str = f'{self.__class__.__name__}('
        for annotation in self.__annotations__:
            repr_str += f'{annotation}={self.__getattribute__(annotation)}, '
        return f'{repr_str[:-2]})'

    def __repr__(self):
        return self.__str__()


class CrawlerConfig(ConfigComponent):
    PREFIX = 'CRAWLER_'
    fetch_batch_size: int


class DatabaseConfig(ConfigComponent):
    PREFIX = 'DATABASE_'
    dialect: str
    driver: str
    host: str
    port: int
    name: str
    user: str
    password: str
    max_idle_connections: int
    max_open_connections: int
    logging_enabled: bool

    def get_dsn(self, sanitize: bool = False):
        return '{dialect}{driver}://{user}:{password}@{host}{port}/{name}'.format(
            dialect=self.dialect,
            driver=f'+{self.driver}' if self.driver is not None else '',
            user=self.user,
            password=self.password if not sanitize else '*' * 3,
            host=self.host,
            port=f':{self.port}' if self.port is not None else '',
            name=self.name
        )


class AppConfig(ConfigComponent):
    PREFIX = 'SF_'
    environment: str
    log_file_name: str
    crawler: CrawlerConfig
    database: DatabaseConfig


def create_new_config(env_file_path: str = f'{PROJECT_ROOT_DIR}/.env') -> AppConfig:
    return AppConfig.load_and_parse(env_file_path)
