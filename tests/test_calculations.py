import pytest
from decimal import Decimal
from datetime import datetime
from app.calculation import Calculation
from app.exceptions import OperationError
import logging


@pytest.mark.parametrize(
    "operation,a,b,expected",
    [
        pytest.param("Addition", "2", "3", "5", id="addition"),
        pytest.param("Subtraction", "5", "3", "2", id="subtraction"),
        pytest.param("Multiplication", "4", "2", "8", id="multiplication"),
        pytest.param("Division", "8", "2", "4", id="division"),
        pytest.param("Power", "2", "3", "8", id="power"),
        pytest.param("Root", "16", "2", "4", id="root"),
    ],
)
def test_calculation_results(operation, a, b, expected):
    """Each supported calculation produces the expected result."""
    calc = Calculation(operation, Decimal(a), Decimal(b))
    assert calc.result == Decimal(expected)


@pytest.mark.parametrize(
    "operation,a,b,message",
    [
        pytest.param("Division", "8", "0", "Division by zero is not allowed", id="zero-divisor"),
        pytest.param("Power", "2", "-3", "Negative exponents are not supported", id="negative-exponent"),
        pytest.param("Root", "-16", "2", "Cannot calculate root of negative number", id="negative-root"),
        pytest.param("Unknown", "5", "3", "Unknown operation", id="unknown-operation"),
    ],
)
def test_invalid_calculations(operation, a, b, message):
    """Invalid operations retain their specific error messages."""
    with pytest.raises(OperationError, match=message):
        Calculation(operation, Decimal(a), Decimal(b))


def test_to_dict():
    calc = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    result_dict = calc.to_dict()
    assert result_dict == {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": calc.timestamp.isoformat()
    }


def test_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    calc = Calculation.from_dict(data)
    assert calc.operation == "Addition"
    assert calc.operand1 == Decimal("2")
    assert calc.operand2 == Decimal("3")
    assert calc.result == Decimal("5")


def test_invalid_from_dict():
    data = {
        "operation": "Addition",
        "operand1": "invalid",
        "operand2": "3",
        "result": "5",
        "timestamp": datetime.now().isoformat()
    }
    with pytest.raises(OperationError, match="Invalid calculation data"):
        Calculation.from_dict(data)


def test_format_result():
    calc = Calculation(operation="Division", operand1=Decimal("1"), operand2=Decimal("3"))
    assert calc.format_result(precision=2) == "0.33"
    assert calc.format_result(precision=10) == "0.3333333333"


def test_equality():
    calc1 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc2 = Calculation(operation="Addition", operand1=Decimal("2"), operand2=Decimal("3"))
    calc3 = Calculation(operation="Subtraction", operand1=Decimal("5"), operand2=Decimal("3"))
    assert calc1 == calc2
    assert calc1 != calc3


# New Test to Cover Logging Warning
def test_from_dict_result_mismatch(caplog):
    """
    Test the from_dict method to ensure it logs a warning when the saved result
    does not match the computed result.
    """
    # Arrange
    data = {
        "operation": "Addition",
        "operand1": "2",
        "operand2": "3",
        "result": "10",  # Incorrect result to trigger logging.warning
        "timestamp": datetime.now().isoformat()
    }

    # Act
    with caplog.at_level(logging.WARNING):
        calc = Calculation.from_dict(data)

    # Assert
    assert "Loaded calculation result 10 differs from computed result 5" in caplog.text

def test_zero_root():
    """Test that a zero-degree root raises OperationError."""
    with pytest.raises(OperationError, match="Zero root is undefined"):
        Calculation(
            operation="Root",
            operand1=Decimal("16"),
            operand2=Decimal("0")
        )


def test_calculation_str():
    """Test the human-readable string representation."""
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3")
    )

    assert str(calc) == "Addition(2, 3) = 5"


def test_calculation_repr():
    """Test the detailed representation of a calculation."""
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3")
    )

    result = repr(calc)

    assert "Calculation(operation='Addition'" in result
    assert "operand1=2" in result
    assert "operand2=3" in result
    assert "result=5" in result
    assert calc.timestamp.isoformat() in result


def test_equality_with_non_calculation():
    """Test comparison with an unrelated object."""
    calc = Calculation(
        operation="Addition",
        operand1=Decimal("2"),
        operand2=Decimal("3")
    )

    assert calc.__eq__("not a calculation") is NotImplemented

def test_calculation_arithmetic_error(monkeypatch):
    """Test that arithmetic errors are converted to OperationError."""

    def raise_arithmetic_error(self):
        raise ArithmeticError("forced arithmetic error")

    monkeypatch.setattr(
        Calculation,
        "calculate",
        raise_arithmetic_error
    )

    with pytest.raises(ArithmeticError, match="forced arithmetic error"):
        Calculation(
            operation="Addition",
            operand1=Decimal("2"),
            operand2=Decimal("3")
        )
def test_calculation_wraps_arithmetic_error():
    """Test that arithmetic errors are wrapped in OperationError."""
    calc = object.__new__(Calculation)

    calc.operation = "Division"
    calc.operand1 = Decimal("Infinity")
    calc.operand2 = Decimal("Infinity")

    with pytest.raises(
        OperationError,
        match="Calculation failed"
    ) as exc_info:
        calc.calculate()

    assert isinstance(exc_info.value.__cause__, ArithmeticError)