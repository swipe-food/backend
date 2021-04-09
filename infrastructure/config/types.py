from __future__ import annotations

from abc import ABC
from typing import Type, get_type_hints

from dotenv import dotenv_values


class ConfigComponent(ABC):
    PREFIX = ''

    @classmethod
    def load_and_parse(cls, env_file_path: str) -> ConfigComponent:
        from infrastructure.config.parser import ConfigParser
        config = dotenv_values(env_file_path)
        return ConfigParser.parse(config, cls())

    def __str__(self):
        repr_str = f'{self.__class__.__name__}('
        for annotation in self.__annotations__:
            repr_str += f'{annotation}={self.__getattribute__(annotation)}, '
        return f'{repr_str[:-2]})'


class ConfigField(ABC):
    VALID_VALUES = []
    TYPE: Type

    @classmethod
    def parse_to_type(cls, value):
        field_type = get_type_hints(cls)["TYPE"]
        return field_type(value)


class LogLevelField(ConfigField):
    VALID_VALUES = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]
    TYPE: str
