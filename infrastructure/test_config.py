import pytest

from domain.exceptions import MissingConfigException, InvalidValueException
from infrastructure.config import ConfigComponent, ConfigParser, ConfigField


def get_fake_config(missing_value: bool = False, invalid_value: bool = False, invalid_config_field: bool = False) -> dict:
    config = {
        'A_INT_VALUE': '42',
        'A_B_BOOLEAN_VALUE': 'True',
        'A_C_D_STRING_VALUE': 'Test',
        'A_C_D_SMALL_NUMBER': '4',
        'A_C_FLOAT_VALUE': '4.5'
    }

    if missing_value:
        config.pop('A_B_BOOLEAN_VALUE')
    if invalid_value:
        config['A_INT_VALUE'] = 'Invalid Int Value'
    if invalid_config_field:
        config["A_C_D_SMALL_NUMBER"] = "50"
    return config


class TestConfigField(ConfigField):
    """"accepts all integer values greater 0 and smaller 10"""
    VALID_VALUES = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    TYPE: int


class TestComponentD(ConfigComponent):
    PREFIX = 'D_'
    string_value: str
    small_number: TestConfigField


class TestComponentC(ConfigComponent):
    PREFIX = 'C_'
    float_value: float
    component_d: TestComponentD


class TestComponentB(ConfigComponent):
    PREFIX = 'B_'
    boolean_value: bool


class TestConfigA(ConfigComponent):
    PREFIX = 'A_'
    int_value: int
    component_b: TestComponentB
    component_c: TestComponentC

    def __init__(self, config: dict):
        ConfigParser.parse(config, self)


class TestConfigParser:

    def test_config_success(self):
        test_config = TestConfigA(get_fake_config())

        assert test_config.int_value == 42
        assert test_config.component_b.boolean_value is True
        assert test_config.component_c.float_value == 4.5
        assert test_config.component_c.component_d.string_value == 'Test'
        assert test_config.component_c.component_d.small_number == 4

    def test_config_invalid(self):
        with pytest.raises(InvalidValueException):
            TestConfigA(get_fake_config(invalid_config_field=True))

    def test_config_invalid_config_field(self):
        with pytest.raises(InvalidValueException):
            TestConfigA(get_fake_config(invalid_value=True))

    def test_config_missing(self):
        with pytest.raises(MissingConfigException):
            TestConfigA(get_fake_config(missing_value=True))
