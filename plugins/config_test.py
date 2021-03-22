import pytest

from plugins.config import ConfigComponent, ConfigParser, MissingConfigError, InvalidConfigError


def get_fake_config(missing_value: bool = False, invalid_value: bool = False) -> dict:
    config = {
        'A_INT_VALUE': '42',
        'A_B_BOOLEAN_VALUE': 'True',
        'A_C_D_STRING_VALUE': 'Test',
        'A_C_FLOAT_VALUE': '4.5'
    }

    if missing_value:
        config.pop('A_B_BOOLEAN_VALUE')
    if invalid_value:
        config['A_INT_VALUE'] = 'Invalid Int Value'
    return config


class TestComponentD(ConfigComponent):
    PREFIX = 'D_'
    string_value: str


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

    def test_config_invalid(self):

        with pytest.raises(InvalidConfigError):
            TestConfigA(get_fake_config(invalid_value=True))

    def test_config_missing(self):

        with pytest.raises(MissingConfigError):
            TestConfigA(get_fake_config(missing_value=True))
