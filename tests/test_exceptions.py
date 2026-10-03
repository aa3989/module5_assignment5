import pytest
from app.exceptions import CalculatorError, ValidationError, OperationError, ConfigurationError


@pytest.mark.parametrize(
    "error_type,caught_type,message",
    [
        pytest.param(CalculatorError, CalculatorError, 'Base calculator error occurred', id='calculator_error_is_base_exception'),
        pytest.param(ValidationError, CalculatorError, 'Validation failed', id='validation_error_is_calculator_error'),
        pytest.param(ValidationError, ValidationError, 'Validation error', id='validation_error_specific_exception'),
        pytest.param(OperationError, CalculatorError, 'Operation failed', id='operation_error_is_calculator_error'),
        pytest.param(OperationError, OperationError, 'Specific operation error', id='operation_error_specific_exception'),
        pytest.param(ConfigurationError, CalculatorError, 'Configuration invalid', id='configuration_error_is_calculator_error'),
        pytest.param(ConfigurationError, ConfigurationError, 'Specific configuration error', id='configuration_error_specific_exception'),
    ],
)
def test_exception_hierarchy_and_message(error_type, caught_type, message):
    """Exceptions can be caught by their declared type and preserve messages."""
    with pytest.raises(caught_type) as exc_info:
        raise error_type(message)
    assert isinstance(exc_info.value, CalculatorError)
    assert type(exc_info.value) is error_type
    assert str(exc_info.value) == message
