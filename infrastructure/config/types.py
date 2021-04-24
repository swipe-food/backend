from __future__ import annotations

from abc import ABC
from typing import Any

from domain.exceptions import MissingConfigException, InvalidValueException


class ConfigComponent(ABC):
    PREFIX = ''

    @classmethod
    def load_and_parse(cls, config: dict) -> ConfigComponent:
        from infrastructure.config.parser import ConfigParser
        return ConfigParser.parse(config, cls())

    def __str__(self):
        repr_str = f'{self.__class__.__name__}('
        for annotation in self.__annotations__:
            repr_str += f'{annotation}={self.__getattribute__(annotation)}, '
        return f'{repr_str[:-2]})'


class ConfigField(ABC):
    """
    Enables  optional and more granular configuration fields.

    Parameters:
         optional (bool): True if the field is optional
         default (Any): default value
    """

    def __init__(self, optional: bool = False, default: Any = None):
        self._optional = optional
        self._value = default

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: Any):
        if not self._optional or (self._optional and value is not None):
            self._value = value

    def validate(self, env_field_name: str):
        """validates if the config field value is set"""
        if self._value is None and not self._optional:
            raise MissingConfigException(self, f"Required Config field '{env_field_name}' cannot be None")
        pass


class LogLevelField(ConfigField):
    VALID_VALUES = ["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"]

    def __init__(self, optional: bool = False, default: Any = None):
        super().__init__(optional, default)

    def validate(self, env_field_name: str):
        """validates if the value is a valid python logging level"""
        super().validate(env_field_name)
        if self._value not in self.VALID_VALUES:
            raise InvalidValueException(self, "Config field '{field}' has an invalid value '{value}' for type '{field_type}'. Valid values are: {values}".format(
                field=env_field_name,
                value=self._value,
                field_type=self.__class__.__name__,
                values=self.VALID_VALUES
            ))
