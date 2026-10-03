import pytest
import os
from decimal import Decimal
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError

@pytest.fixture(autouse=True)
def configured_environment(monkeypatch):
    """Give every configuration case the same isolated environment."""
    for name in list(os.environ):
        if name.startswith("CALCULATOR_"):
            monkeypatch.delenv(name)
    values = {
        "CALCULATOR_MAX_HISTORY_SIZE": "500",
        "CALCULATOR_AUTO_SAVE": "false",
        "CALCULATOR_PRECISION": "8",
        "CALCULATOR_MAX_INPUT_VALUE": "1000",
        "CALCULATOR_DEFAULT_ENCODING": "utf-16",
        "CALCULATOR_LOG_DIR": "./test_logs",
        "CALCULATOR_HISTORY_DIR": "./test_history",
        "CALCULATOR_HISTORY_FILE": "./test_history/test_history.csv",
        "CALCULATOR_LOG_FILE": "./test_logs/test_log.log",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)


def clear_env_vars(monkeypatch, *names):
    for name in names:
        monkeypatch.delenv(name, raising=False)


def test_default_configuration():
    config = CalculatorConfig()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal("1000")
    assert config.default_encoding == 'utf-16'
    assert config.log_dir == Path('./test_logs').resolve()
    assert config.history_dir == Path('./test_history').resolve()
    assert config.history_file == Path('./test_history/test_history.csv').resolve()
    assert config.log_file == Path('./test_logs/test_log.log').resolve()

def test_custom_configuration():
    config = CalculatorConfig(
        max_history_size=300,
        auto_save=True,
        precision=5,
        max_input_value=Decimal("500"),
        default_encoding="ascii"
    )
    assert config.max_history_size == 300
    assert config.auto_save is True
    assert config.precision == 5
    assert config.max_input_value == Decimal("500")
    assert config.default_encoding == "ascii"

def test_directory_properties(monkeypatch):
    clear_env_vars(monkeypatch, 'CALCULATOR_LOG_DIR', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.log_dir == Path('/custom_base_dir/logs').resolve()
    assert config.history_dir == Path('/custom_base_dir/history').resolve()

def test_file_properties(monkeypatch):
    clear_env_vars(monkeypatch, 'CALCULATOR_HISTORY_FILE', 'CALCULATOR_LOG_FILE', 'CALCULATOR_HISTORY_DIR', 'CALCULATOR_LOG_DIR')
    config = CalculatorConfig(base_dir=Path('/custom_base_dir'))
    assert config.history_file == Path('/custom_base_dir/history/calculator_history.csv').resolve()
    assert config.log_file == Path('/custom_base_dir/logs/calculator.log').resolve()

@pytest.mark.parametrize(
    "setting,value",
    [("max_history_size", -1), ("precision", -1), ("max_input_value", Decimal("-1"))],
)
def test_invalid_configuration(setting, value):
    """Negative settings raise the corresponding configuration error."""
    with pytest.raises(ConfigurationError, match=f"{setting} must be positive"):
        CalculatorConfig(**{setting: value}).validate()


@pytest.mark.parametrize("value,expected", [("true", True), ("1", True), ("false", False), ("0", False)])
def test_auto_save_environment(monkeypatch, value, expected):
    monkeypatch.setenv("CALCULATOR_AUTO_SAVE", value)
    assert CalculatorConfig(auto_save=None).auto_save is expected


def test_environment_overrides():
    config = CalculatorConfig()
    assert config.max_history_size == 500
    assert config.auto_save is False
    assert config.precision == 8
    assert config.max_input_value == Decimal("1000")
    assert config.default_encoding == 'utf-16'

def test_default_fallbacks(monkeypatch):
    # Clear all related environment variables and test default values
    clear_env_vars(monkeypatch, 
        'CALCULATOR_MAX_HISTORY_SIZE', 'CALCULATOR_AUTO_SAVE', 'CALCULATOR_PRECISION',
        'CALCULATOR_MAX_INPUT_VALUE', 'CALCULATOR_DEFAULT_ENCODING'
    )
    config = CalculatorConfig()
    assert config.max_history_size == 1000
    assert config.auto_save is True
    assert config.precision == 10
    assert config.max_input_value == Decimal("1e999")
    assert config.default_encoding == 'utf-8'

def test_get_project_root():
    # Test that get_project_root() points to the correct path
    from app.calculator_config import get_project_root
    assert (get_project_root() / "app").exists()  # Adjust the path check as needed based on your file structure

def test_log_dir_property(monkeypatch):
    # Clear environment to test base_dir path creation for log_dir
    clear_env_vars(monkeypatch, 'CALCULATOR_LOG_DIR')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.log_dir == Path('/new_base_dir/logs').resolve()

def test_history_dir_property(monkeypatch):
    # Clear environment to test base_dir path creation for history_dir
    clear_env_vars(monkeypatch, 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.history_dir == Path('/new_base_dir/history').resolve()

def test_log_file_property(monkeypatch):
    # Clear environment to test base_dir path creation for log_file
    clear_env_vars(monkeypatch, 'CALCULATOR_LOG_FILE', 'CALCULATOR_LOG_DIR')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.log_file == Path('/new_base_dir/logs/calculator.log').resolve()

def test_history_file_property(monkeypatch):
    # Clear environment to test base_dir path creation for history_file
    clear_env_vars(monkeypatch, 'CALCULATOR_HISTORY_FILE', 'CALCULATOR_HISTORY_DIR')
    config = CalculatorConfig(base_dir=Path('/new_base_dir'))
    assert config.history_file == Path('/new_base_dir/history/calculator_history.csv').resolve()

