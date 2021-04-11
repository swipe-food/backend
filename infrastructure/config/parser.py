import os
from typing import get_type_hints, Any

from domain.exceptions import MissingConfigException, InvalidValueException
from infrastructure.config.types import ConfigComponent, ConfigField


class ConfigParser:
    """
    A class to parse the configuration of the application based on the defined types.
    """

    @classmethod
    def parse(cls, config: dict, component: ConfigComponent, current_prefix: str = "") -> ConfigComponent:
        """
        Parses the configurations for every variable of the passed component.
        If a variable of the passed component is a ConfigComponent itself, this function will be called recursively.

            Parameters:
                    config (dict): dictionary of config fields. can be default values or content of a .env file
                    component (ConfigComponent): ConfigComponent to parse
                    current_prefix (str): current concatenated prefix of the component. e.g. SF_API_DATABASE_

            Returns:
                     component (ConfigComponent): parsed component
        """
        current_prefix += component.PREFIX
        for variable in component.__annotations__:
            variable_type = get_type_hints(component.__class__)[variable]

            if issubclass(variable_type, ConfigComponent):
                value = cls.parse(config, variable_type(), current_prefix)
            else:
                env_field_name = current_prefix + variable.upper()
                value = cls._parse_env_variable(config, env_field_name, variable_type)
            component.__setattr__(variable, value)
        return component

    @classmethod
    def _parse_env_variable(cls, config: dict, variable: str, field_type: Any) -> Any:
        """
        Parses a single environmental variable into it's target type.
        The environmental variable will be read directly from os or via the passed config dictionary.
        This function uses the following precedence order:
            1. env variable
            2. config dict
        Additionaly this function handles any config variable of the type ConfigField.

            Parameters:
                    config (dict): dictionary of config fields. can be default values or content of a .env file
                    variable (str): config variable to parse
                    field_type (Any): type of variable. Can be any type.

            Returns:
                     parsed_value (Any): parsed value of variable
        """
        value = os.getenv(variable, config.get(variable))
        if value is None:
            raise MissingConfigException(cls, f"Required Config field '{variable}' cannot be None")
        try:
            if issubclass(field_type, bool):
                return value == 'True'
            elif issubclass(field_type, ConfigField):
                parsed_value = field_type.parse_to_type(value)
                if parsed_value not in field_type.VALID_VALUES:
                    raise InvalidValueException(cls, "Config variable '{var}' has an invalid value '{parsed_var}' for type '{var_type}'. Valid values are: {values}".format(
                        var=variable,
                        parsed_var=parsed_value,
                        var_type=field_type.__name__,
                        values=field_type.VALID_VALUES
                    ))
                return parsed_value
            return field_type(value)
        except InvalidValueException as exception:
            raise exception
        except ValueError:
            raise InvalidValueException(cls, f"Config variable '{variable}' has an invalid value '{value}' for type '{field_type}'")
