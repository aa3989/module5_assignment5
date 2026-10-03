"""Tests for the Calculator Memento implementation."""

import datetime
from decimal import Decimal

import pytest

from app.calculation import Calculation
from app.calculator_memento import CalculatorMemento


@pytest.fixture
def sample_calculation():
    """Create a sample calculation for memento tests."""
    return Calculation(
        operation="Addition",
        operand1=Decimal("10"),
        operand2=Decimal("5")
    )


@pytest.fixture
def sample_timestamp():
    """Create a predictable timestamp for testing."""
    return datetime.datetime(2026, 1, 1, 12, 30, 0)


def test_memento_creation(sample_calculation, sample_timestamp):
    """Test creating a CalculatorMemento."""
    memento = CalculatorMemento(
        history=[sample_calculation],
        timestamp=sample_timestamp
    )

    assert len(memento.history) == 1
    assert memento.history[0] == sample_calculation
    assert memento.timestamp == sample_timestamp


def test_memento_default_timestamp(sample_calculation):
    """Test that a timestamp is automatically created."""
    before = datetime.datetime.now()

    memento = CalculatorMemento(
        history=[sample_calculation]
    )

    after = datetime.datetime.now()

    assert before <= memento.timestamp <= after


def test_memento_to_dict(sample_calculation, sample_timestamp):
    """Test serialization of a memento to a dictionary."""
    memento = CalculatorMemento(
        history=[sample_calculation],
        timestamp=sample_timestamp
    )

    data = memento.to_dict()

    assert isinstance(data, dict)
    assert "history" in data
    assert "timestamp" in data

    assert len(data["history"]) == 1

    assert data["history"][0]["operation"] == "Addition"
    assert data["history"][0]["operand1"] == "10"
    assert data["history"][0]["operand2"] == "5"
    assert data["history"][0]["result"] == "15"

    assert data["timestamp"] == sample_timestamp.isoformat()


def test_memento_from_dict(sample_timestamp):
    """Test deserialization of a memento from a dictionary."""
    data = {
        "history": [
            {
                "operation": "Addition",
                "operand1": "10",
                "operand2": "5",
                "result": "15",
                "timestamp": "2026-01-01T12:00:00"
            }
        ],
        "timestamp": sample_timestamp.isoformat()
    }

    memento = CalculatorMemento.from_dict(data)

    assert isinstance(memento, CalculatorMemento)
    assert len(memento.history) == 1

    calculation = memento.history[0]

    assert isinstance(calculation, Calculation)
    assert calculation.operation == "Addition"
    assert calculation.operand1 == Decimal("10")
    assert calculation.operand2 == Decimal("5")
    assert calculation.result == Decimal("15")

    assert memento.timestamp == sample_timestamp


@pytest.mark.parametrize(
    "operation,operand1,operand2,expected",
    [
        ("Addition", "10", "5", "15"),
        ("Subtraction", "10", "5", "5"),
        ("Multiplication", "10", "5", "50"),
        ("Division", "10", "5", "2"),
        ("Power", "2", "3", "8"),
        ("Root", "25", "2", "5"),
    ],
)
def test_memento_round_trip(
    operation,
    operand1,
    operand2,
    expected
):
    """Test memento serialization/deserialization for all operations."""
    calculation = Calculation(
        operation=operation,
        operand1=Decimal(operand1),
        operand2=Decimal(operand2)
    )

    original = CalculatorMemento(
        history=[calculation]
    )

    serialized = original.to_dict()
    restored = CalculatorMemento.from_dict(serialized)

    assert len(restored.history) == 1

    restored_calculation = restored.history[0]

    assert restored_calculation.operation == operation
    assert restored_calculation.operand1 == Decimal(operand1)
    assert restored_calculation.operand2 == Decimal(operand2)
    assert restored_calculation.result == Decimal(expected)

    assert restored.timestamp == original.timestamp


def test_empty_memento_round_trip():
    """Test serialization/deserialization of an empty history."""
    original = CalculatorMemento(history=[])

    serialized = original.to_dict()
    restored = CalculatorMemento.from_dict(serialized)

    assert restored.history == []
    assert restored.timestamp == original.timestamp