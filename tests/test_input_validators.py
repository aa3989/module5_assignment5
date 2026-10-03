import pytest
from decimal import Decimal
from app.calculator_config import CalculatorConfig
from app.exceptions import ValidationError
from app.input_validators import InputValidator


@pytest.fixture
def config():
    return CalculatorConfig(max_input_value=Decimal("1000000"))


@pytest.mark.parametrize("value,expected", [
        pytest.param(123, Decimal('123'), id='positive_integer'),
        pytest.param(123.456, Decimal('123.456').normalize(), id='positive_decimal'),
        pytest.param('123', Decimal('123'), id='positive_string_integer'),
        pytest.param('123.456', Decimal('123.456').normalize(), id='positive_string_decimal'),
        pytest.param(-789, Decimal('-789'), id='negative_integer'),
        pytest.param(-789.123, Decimal('-789.123').normalize(), id='negative_decimal'),
        pytest.param('-789', Decimal('-789'), id='negative_string_integer'),
        pytest.param('-789.123', Decimal('-789.123').normalize(), id='negative_string_decimal'),
        pytest.param(0, Decimal('0'), id='zero'),
        pytest.param('  456  ', Decimal('456'), id='trimmed_string'),
])
def test_valid_numbers(value, expected, config):
    """Accept numeric types, numeric strings, signs, zero, and whitespace."""
    assert InputValidator.validate_number(value, config) == expected


@pytest.mark.parametrize("value,message", [
        pytest.param('abc', 'Invalid number format: abc', id='invalid_string'),
        pytest.param(Decimal('1000001'), 'Value exceeds maximum allowed', id='exceeds_max_value'),
        pytest.param('1000001', 'Value exceeds maximum allowed', id='exceeds_max_value_string'),
        pytest.param(-Decimal('1000001'), 'Value exceeds maximum allowed', id='exceeds_negative_max_value'),
        pytest.param('', 'Invalid number format: ', id='empty_string'),
        pytest.param('   ', 'Invalid number format: ', id='whitespace_string'),
        pytest.param(None, 'Invalid number format: None', id='none_value'),
        pytest.param([], 'Invalid number format: ', id='non_numeric_type'),
])
def test_invalid_numbers(value, message, config):
    """Reject malformed and out-of-range values with the expected message."""
    with pytest.raises(ValidationError, match=message):
        InputValidator.validate_number(value, config)
