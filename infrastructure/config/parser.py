import os
from typing import get_type_hints, Any, Optional

from domain.exceptions import MissingConfigException, InvalidValueException
from infrastructure.config.types import ConfigComponent, ConfigField


class ConfigParser:
    """
    A class to parse the configuration of the application based on the defined types.
    """

    @classmethod
    def parse(cls, config: dict, component: ConfigComponent, current_prefix: str = "") -> ConfigComponent:
        """
        Parses the configurations for every field of the passed component.
        If a field of the passed component is a ConfigComponent itself, this function will be called recursively.

            Parameters:
                    config (dict): dictionary of config fields. can be default values or content of a local.env file
                    component (ConfigComponent): ConfigComponent to parse
                    current_prefix (str): current concatenated prefix of the component. e.g. SF_API_DATABASE_

            Returns:
                     component (ConfigComponent): parsed component
        """
        current_prefix += component.PREFIX
        for field in component.__annotations__:
            field_type = get_type_hints(component.__class__)[field]

            if issubclass(field_type, ConfigComponent):
                value = cls.parse(config, field_type(), current_prefix)
            else:
                env_field_name = current_prefix + field.upper()
                try:
                    field_object = component.__getattribute__(field)
                except AttributeError:
                    field_object = None
                if isinstance(field_object, ConfigField):
                    value = cls._parse_config_field(config, env_field_name, field_type, field_object)
                else:
                    value = cls._parse_required_env_field(config, env_field_name, field_type)
            component.__setattr__(field, value)
        return component

    @classmethod
    def _parse_config_field(cls, config: dict, field: str, field_type: Any, field_obj: ConfigField) -> Any:
        """
        Parses a env field into a ConfigField object.
        Parameters:
                config (dict): dictionary of config fields. can be default values or content of a local.env file
                field (str): config field to parse
                field_type (Any): type of field. Can be any type.
                field_obj (ConfigField): instance of the config field
        Returns:
             field_obj.value: value of ConfigField
         """
        value = cls._parse_env_field(config, field, field_type)
        field_obj.value = value
        field_obj.validate(field)
        return field_obj.value

    @classmethod
    def _parse_required_env_field(cls, config: dict, field: str, field_type: Any):
        value = cls._parse_env_field(config, field, field_type)
        if value is None:
            raise MissingConfigException(cls, f"Required Config field '{field}' cannot be None")
        return value

    @classmethod
    def _parse_env_field(cls, config: dict, field: str, field_type: Any) -> Any:
        """
        Parses a single environmental field into it's target type.
        The environmental field will be read directly from os or via the passed config dictionary.
        This function uses the following precedence order:
            1. env field
            2. config dict

            Parameters:
                    config (dict): dictionary of config fields. can be default values or content of a local.env file
                    field (str): config field to parse
                    field_type (Any): type of field. Can be any type.

            Returns:
                     parsed_value (Any): parsed value of field
        """
        value = os.getenv(field, config.get(field))
        try:
            if issubclass(field_type, bool):
                return value == 'True' if value is not None else None
            if value is None:
                return None
            return field_type(value)
        except ValueError:
            raise InvalidValueException(cls, f"Config field '{field}' has an invalid value '{value}' for type '{field_type}'")
