import pytest
from decimal import Decimal

from app.exceptions import ValidationError
from app.operations import (
    Operation,
    Addition,
    Subtraction,
    Multiplication,
    Division,
    Power,
    Root,
    OperationFactory,
)


class TestOperation:
    """Test base Operation class functionality."""

    def test_str_representation(self):
        """Test that string representation returns class name."""
        class TestOp(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        assert str(TestOp()) == "TestOp"


@pytest.mark.parametrize("operation_class,a,b,expected", [
        pytest.param(Addition, '5', '3', '8', id='addition-positive_numbers'),
        pytest.param(Addition, '-5', '-3', '-8', id='addition-negative_numbers'),
        pytest.param(Addition, '-5', '3', '-2', id='addition-mixed_signs'),
        pytest.param(Addition, '5', '-5', '0', id='addition-zero_sum'),
        pytest.param(Addition, '5.5', '3.3', '8.8', id='addition-decimals'),
        pytest.param(Addition, '1e10', '1e10', '20000000000', id='addition-large_numbers'),
        pytest.param(Subtraction, '5', '3', '2', id='subtraction-positive_numbers'),
        pytest.param(Subtraction, '-5', '-3', '-2', id='subtraction-negative_numbers'),
        pytest.param(Subtraction, '-5', '3', '-8', id='subtraction-mixed_signs'),
        pytest.param(Subtraction, '5', '5', '0', id='subtraction-zero_result'),
        pytest.param(Subtraction, '5.5', '3.3', '2.2', id='subtraction-decimals'),
        pytest.param(Subtraction, '1e10', '1e9', '9000000000', id='subtraction-large_numbers'),
        pytest.param(Multiplication, '5', '3', '15', id='multiplication-positive_numbers'),
        pytest.param(Multiplication, '-5', '-3', '15', id='multiplication-negative_numbers'),
        pytest.param(Multiplication, '-5', '3', '-15', id='multiplication-mixed_signs'),
        pytest.param(Multiplication, '5', '0', '0', id='multiplication-multiply_by_zero'),
        pytest.param(Multiplication, '5.5', '3.3', '18.15', id='multiplication-decimals'),
        pytest.param(Multiplication, '1e5', '1e5', '10000000000', id='multiplication-large_numbers'),
        pytest.param(Division, '6', '2', '3', id='division-positive_numbers'),
        pytest.param(Division, '-6', '-2', '3', id='division-negative_numbers'),
        pytest.param(Division, '-6', '2', '-3', id='division-mixed_signs'),
        pytest.param(Division, '5.5', '2', '2.75', id='division-decimals'),
        pytest.param(Division, '0', '5', '0', id='division-divide_zero'),
        pytest.param(Power, '2', '3', '8', id='power-positive_base_and_exponent'),
        pytest.param(Power, '5', '0', '1', id='power-zero_exponent'),
        pytest.param(Power, '5', '1', '5', id='power-one_exponent'),
        pytest.param(Power, '2.5', '2', '6.25', id='power-decimal_base'),
        pytest.param(Power, '0', '5', '0', id='power-zero_base'),
        pytest.param(Root, '9', '2', '3', id='root-square_root'),
        pytest.param(Root, '27', '3', '3', id='root-cube_root'),
        pytest.param(Root, '16', '4', '2', id='root-fourth_root'),
        pytest.param(Root, '2.25', '2', '1.5', id='root-decimal_root'),
])
def test_valid_operations(operation_class, a, b, expected):
    """Run every original arithmetic case as an independent pytest item."""
    assert operation_class().execute(Decimal(a), Decimal(b)) == Decimal(expected)


@pytest.mark.parametrize("operation_class,a,b,error,message", [
        pytest.param(Division, '5', '0', ValidationError, 'Division by zero is not allowed', id='division-divide_by_zero'),
        pytest.param(Power, '2', '-3', ValidationError, 'Negative exponents not supported', id='power-negative_exponent'),
        pytest.param(Root, '-9', '2', ValidationError, 'Cannot calculate root of negative number', id='root-negative_base'),
        pytest.param(Root, '9', '0', ValidationError, 'Zero root is undefined', id='root-zero_root'),
])
def test_invalid_operations(operation_class, a, b, error, message):
    with pytest.raises(error, match=message):
        operation_class().execute(Decimal(a), Decimal(b))


class TestOperationFactory:
    """Test OperationFactory functionality."""

    @pytest.mark.parametrize("name,operation_class", [
        ("add", Addition), ("subtract", Subtraction),
        ("multiply", Multiplication), ("divide", Division),
        ("power", Power), ("root", Root),
    ])
    @pytest.mark.parametrize("uppercase", [False, True], ids=["lowercase", "uppercase"])
    def test_create_valid_operations(self, name, operation_class, uppercase):
        operation = OperationFactory.create_operation(name.upper() if uppercase else name)
        assert isinstance(operation, operation_class)

    def test_create_invalid_operation(self):
        """Test creation of invalid operation raises error."""
        with pytest.raises(ValueError, match="Unknown operation: invalid_op"):
            OperationFactory.create_operation("invalid_op")

    def test_register_valid_operation(self):
        """Test registering a new valid operation."""
        class NewOperation(Operation):
            def execute(self, a: Decimal, b: Decimal) -> Decimal:
                return a

        OperationFactory.register_operation("new_op", NewOperation)
        operation = OperationFactory.create_operation("new_op")
        assert isinstance(operation, NewOperation)

    def test_register_invalid_operation(self):
        """Test registering an invalid operation class raises error."""
        class InvalidOperation:
            pass

        with pytest.raises(TypeError, match="Operation class must inherit"):
            OperationFactory.register_operation("invalid", InvalidOperation)