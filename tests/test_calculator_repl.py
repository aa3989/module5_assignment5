from decimal import Decimal
from unittest.mock import Mock, patch

import pytest

from app.calculator_repl import calculator_repl
from app.exceptions import OperationError, ValidationError


def make_mock_calculator():
    """Create a mock Calculator with sensible default behavior."""
    calc = Mock()
    calc.show_history.return_value = []
    calc.undo.return_value = False
    calc.redo.return_value = False
    calc.perform_operation.return_value = Decimal("5")
    return calc


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["history", "exit"])
@patch("builtins.print")
def test_history_empty(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("No calculations in history")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["history", "exit"])
@patch("builtins.print")
def test_history_with_entries(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    calc.show_history.return_value = [
        "Addition: 2 + 3 = 5",
        "Multiplication: 4 * 5 = 20",
    ]
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("\nCalculation History:")
    mock_print.assert_any_call("1. Addition: 2 + 3 = 5")
    mock_print.assert_any_call("2. Multiplication: 4 * 5 = 20")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["clear", "exit"])
@patch("builtins.print")
def test_clear_history(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    calc.clear_history.assert_called_once()
    mock_print.assert_any_call("History cleared")


@pytest.mark.parametrize(
    "undo_result, expected_message",
    [
        (True, "Operation undone"),
        (False, "Nothing to undo"),
    ],
)
def test_undo(undo_result, expected_message):
    calc = make_mock_calculator()
    calc.undo.return_value = undo_result

    with patch("app.calculator_repl.Calculator", return_value=calc), \
         patch("builtins.input", side_effect=["undo", "exit"]), \
         patch("builtins.print") as mock_print:

        calculator_repl()

    mock_print.assert_any_call(expected_message)


@pytest.mark.parametrize(
    "redo_result, expected_message",
    [
        (True, "Operation redone"),
        (False, "Nothing to redo"),
    ],
)
def test_redo(redo_result, expected_message):
    calc = make_mock_calculator()
    calc.redo.return_value = redo_result

    with patch("app.calculator_repl.Calculator", return_value=calc), \
         patch("builtins.input", side_effect=["redo", "exit"]), \
         patch("builtins.print") as mock_print:

        calculator_repl()

    mock_print.assert_any_call(expected_message)


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["save", "exit"])
@patch("builtins.print")
def test_save_history(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("History saved successfully")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["save", "exit"])
@patch("builtins.print")
def test_save_history_error(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    calc.save_history.side_effect = [
        OperationError("save failed"),
        None,
    ]
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("Error saving history: save failed")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["load", "exit"])
@patch("builtins.print")
def test_load_history(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    calc.load_history.assert_called_once()
    mock_print.assert_any_call("History loaded successfully")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["load", "exit"])
@patch("builtins.print")
def test_load_history_error(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    calc.load_history.side_effect = OperationError("load failed")
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("Error loading history: load failed")

@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["help", "exit"])
@patch("builtins.print")
def test_help_command(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("\nAvailable commands:")
    mock_print.assert_any_call(
        "  add, subtract, multiply, divide, power, root - Perform calculations"
    )
    mock_print.assert_any_call("  history - Show calculation history")
    mock_print.assert_any_call("  exit - Exit the calculator")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["exit"])
@patch("builtins.print")
def test_exit_save_failure(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    calc.save_history.side_effect = OperationError("save failed")
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call(
        "Warning: Could not save history: save failed"
    )
    mock_print.assert_any_call("Goodbye!")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["add", "cancel", "exit"])
@patch("builtins.print")
def test_operation_cancel_first_number(
    mock_print, mock_input, mock_calculator
):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("Operation cancelled")
    calc.perform_operation.assert_not_called()


@patch("app.calculator_repl.Calculator")
@patch(
    "builtins.input",
    side_effect=["add", "2", "cancel", "exit"]
)
@patch("builtins.print")
def test_operation_cancel_second_number(
    mock_print, mock_input, mock_calculator
):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("Operation cancelled")
    calc.perform_operation.assert_not_called()


@pytest.mark.parametrize(
    "command",
    ["add", "subtract", "multiply", "divide", "power", "root"],
)
def test_arithmetic_commands(command):
    calc = make_mock_calculator()
    calc.perform_operation.return_value = Decimal("5")

    operation = Mock()

    with patch(
        "app.calculator_repl.Calculator",
        return_value=calc
    ), patch(
        "app.calculator_repl.OperationFactory.create_operation",
        return_value=operation
    ) as mock_factory, patch(
        "builtins.input",
        side_effect=[command, "2", "3", "exit"]
    ), patch(
        "builtins.print"
    ) as mock_print:

        calculator_repl()

    mock_factory.assert_any_call(command)
    calc.set_operation.assert_called_with(operation)
    calc.perform_operation.assert_called_with("2", "3")
    mock_print.assert_any_call("\nResult: 5")


@pytest.mark.parametrize(
    "error",
    [
        ValidationError("invalid input"),
        OperationError("operation failed"),
    ],
)
def test_known_operation_errors(error):
    calc = make_mock_calculator()
    calc.perform_operation.side_effect = error

    with patch(
        "app.calculator_repl.Calculator",
        return_value=calc
    ), patch(
        "builtins.input",
        side_effect=["add", "2", "3", "exit"]
    ), patch(
        "builtins.print"
    ) as mock_print:

        calculator_repl()

    mock_print.assert_any_call(f"Error: {error}")


def test_unexpected_operation_error():
    calc = make_mock_calculator()
    calc.perform_operation.side_effect = RuntimeError("boom")

    with patch(
        "app.calculator_repl.Calculator",
        return_value=calc
    ), patch(
        "builtins.input",
        side_effect=["add", "2", "3", "exit"]
    ), patch(
        "builtins.print"
    ) as mock_print:

        calculator_repl()

    mock_print.assert_any_call("Unexpected error: boom")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=["banana", "exit"])
@patch("builtins.print")
def test_unknown_command(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call(
        "Unknown command: 'banana'. Type 'help' for available commands."
    )


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=[KeyboardInterrupt, "exit"])
@patch("builtins.print")
def test_keyboard_interrupt(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("\nOperation cancelled")


@patch("app.calculator_repl.Calculator")
@patch("builtins.input", side_effect=EOFError)
@patch("builtins.print")
def test_eof_error(mock_print, mock_input, mock_calculator):
    calc = make_mock_calculator()
    mock_calculator.return_value = calc

    calculator_repl()

    mock_print.assert_any_call("\nInput terminated. Exiting...")


def test_general_repl_error():
    calc = make_mock_calculator()

    with patch(
        "app.calculator_repl.Calculator",
        return_value=calc
    ), patch(
        "builtins.input",
        side_effect=[RuntimeError("input failed"), "exit"]
    ), patch(
        "builtins.print"
    ) as mock_print:

        calculator_repl()

    mock_print.assert_any_call("Error: input failed")


def test_fatal_initialization_error():
    with patch(
        "app.calculator_repl.Calculator",
        side_effect=RuntimeError("initialization failed")
    ), patch(
        "app.calculator_repl.logging.error"
    ) as mock_logging_error, patch(
        "builtins.print"
    ) as mock_print:

        with pytest.raises(
            RuntimeError,
            match="initialization failed"
        ):
            calculator_repl()

    mock_print.assert_any_call(
        "Fatal error: initialization failed"
    )
    mock_logging_error.assert_called_once_with(
        "Fatal error in calculator REPL: initialization failed"
    )

def test_operation_with_non_decimal_result():
    """Test calculation result that is not a Decimal."""
    calc = make_mock_calculator()
    calc.perform_operation.return_value = 5

    operation = Mock()

    with patch(
        "app.calculator_repl.Calculator",
        return_value=calc
    ), patch(
        "app.calculator_repl.OperationFactory.create_operation",
        return_value=operation
    ), patch(
        "builtins.input",
        side_effect=["add", "2", "3", "exit"]
    ), patch(
        "builtins.print"
    ) as mock_print:

        calculator_repl()

    calc.perform_operation.assert_called_with("2", "3")
    mock_print.assert_any_call("\nResult: 5")