from __future__ import annotations

from abc import ABC
from pathlib import Path
from typing import Type, get_type_hints, Any

from dotenv import dotenv_values

PROJECT_ROOT_DIR = Path(__file__).parent.parent


class ConfigParser:

    @classmethod
    def parse(cls, config: dict, obj: ConfigComponent) -> ConfigComponent:
        for field in obj.__annotations__:
            field_type = get_type_hints(obj.__class__)[field]

            if issubclass(field_type, ConfigComponent):
                value = cls._parse_class(config, field_type)
            else:
                value = cls._parse_value(config, field.upper(), field_type)
            obj.__setattr__(field, value)
        return obj

    @classmethod
    def _parse_value(cls, config: dict, field: str, field_type: Any) -> Any:
        value = config.get(field)
        if value is None:
            raise MissingConfigError(f"Required Config field '{field}' cannot be None")
        try:
            return field_type(value)
        except ValueError:
            raise InvalidConfigError(f"Config field '{field}' has an invalid value '{value}' for type {field_type}")

    @classmethod
    def _parse_class(cls, config: dict, field_type: Type[ConfigComponent]) -> ConfigComponent:
        filtered_config = {k.split(field_type.PREFIX)[1]: v for (k, v) in config.items() if field_type.PREFIX in k}
        return cls.parse(config=filtered_config, obj=field_type())


class ConfigComponent(ABC):
    PREFIX = 'PREFIX_'


class CrawlerConfig(ConfigComponent):
    PREFIX = 'CRAWLER_'
    fetch_batch_size: int


class Config(ConfigComponent):
    PREFIX = ''
    environment: str
    log_file_name: str
    crawler: CrawlerConfig

    def __init__(self, env_file_path: str):
        self.env_file_path = env_file_path
        self._load_and_parse()

    def _load_and_parse(self):
        self.config = dotenv_values(self.env_file_path)

        ConfigParser.parse(self.config, self)


def create_new_config(env_file_path: str = f'{PROJECT_ROOT_DIR}/.env') -> Config:
    return Config(env_file_path)


class MissingConfigError(Exception):
    pass


class InvalidConfigError(Exception):
    pass
