import pytest
from dotenv import dotenv_values

from plugins.config import ConfigComponent, ConfigParser, MissingConfigError, InvalidConfigError


def get_fake_config(missing_value: bool = False, invalid_value: bool = False) -> dict:
    config = {
        'INT_VALUE': '42',
        'A_BOOLEAN_VALUE': 'True',
        'A_C_STRING_VALUE': 'Test',
        'B_FLOAT_VALUE': '4.5'
    }

    if missing_value:
        config.pop('A_BOOLEAN_VALUE')
    if invalid_value:
        config['INT_VALUE'] = 'Invalid Int Value'
    return config


class TestComponentC(ConfigComponent):
    PREFIX = 'C_'
    string_value: str


class TestComponentA(ConfigComponent):
    PREFIX = 'A_'
    boolean_value: bool
    component_c: TestComponentC


class TestComponentB(ConfigComponent):
    PREFIX = 'B_'
    float_value: float


class TestConfig(ConfigComponent):
    PREFIX = ''
    int_value: int
    component_a: TestComponentA
    component_b: TestComponentB

    def __init__(self, config: dict):
        ConfigParser.parse(config, self)


class TestConfigParser:

    def test_config_success(self):
        test_config = TestConfig(get_fake_config())

        assert test_config.int_value == 42
        assert test_config.component_a.boolean_value is True
        assert test_config.component_a.component_c.string_value == 'Test'
        assert test_config.component_b.float_value == 4.5

    def test_config_invalid(self):

        with pytest.raises(InvalidConfigError):
            TestConfig(get_fake_config(invalid_value=True))

    def test_config_missing(self):

        with pytest.raises(MissingConfigError):
            TestConfig(get_fake_config(missing_value=True))