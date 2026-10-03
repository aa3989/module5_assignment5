# Enhanced Python Calculator

A command-line calculator application built in Python. This project demonstrates object-oriented programming, software design patterns, persistent calculation history, environment-based configuration, input validation, exception handling, logging, automated testing, and continuous integration.

## Features

The calculator supports the following mathematical operations:

- Addition
- Subtraction
- Multiplication
- Division
- Power
- Root

The interactive REPL also provides the following commands:

- `help` — Display available commands
- `history` — Display calculation history
- `clear` — Clear calculation history
- `undo` — Undo the most recent calculation
- `redo` — Restore the most recently undone calculation
- `save` — Save calculation history to CSV
- `load` — Load calculation history from CSV
- `exit` — Save history and exit the calculator

Users can also enter `cancel` while entering operands to cancel the current calculation.


---

## Requirements

The project requires Python and the packages listed in `requirements.txt`.

The project has been developed and tested with Python 3.14.

---

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd assignment5
```

### 2. Create a Virtual Environment

On macOS, Linux, or WSL:

```bash
python3 -m venv venv
```

On Windows:

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

macOS, Linux, or WSL:

```bash
source venv/bin/activate
```

Windows Command Prompt:

```text
venv\Scripts\activate.bat
```

Windows PowerShell:

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

The calculator supports environment-based configuration using `python-dotenv`.

A `.env` file can be placed in the project root.

Example:

```env
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```

The calculator configuration system also supports settings for:

- Maximum history size
- Automatic saving
- Decimal precision
- Maximum input value
- Default encoding
- Log directory
- Log file
- History directory
- History file

Configuration values are validated before use.

The `.env` file is excluded from Git through `.gitignore` so local environment settings are not committed to the repository.

---

## Running the Calculator

Start the application from the project root:

```bash
python main.py
```

The calculator will start its interactive command-line REPL.

Use:

```text
help
```

to display the available commands.

### Example Calculation

```text
Enter command: add
Enter first number: 10
Enter second number: 5

Result: 15
```

Additional operations can be performed using commands such as:

```text
subtract
multiply
divide
power
root
```

---

## Calculator Commands

| Command | Description |
| --- | --- |
| `add` | Add two numbers |
| `subtract` | Subtract the second number from the first |
| `multiply` | Multiply two numbers |
| `divide` | Divide the first number by the second |
| `power` | Raise a number to a power |
| `root` | Calculate a root |
| `history` | Display calculation history |
| `clear` | Clear calculation history |
| `undo` | Undo the most recent calculation |
| `redo` | Restore the most recently undone calculation |
| `save` | Save history to CSV |
| `load` | Load history from CSV |
| `help` | Display available commands |
| `exit` | Save history and exit |

When entering operands, use:

```text
cancel
```

to cancel the current calculation and return to the command prompt.

---

## Calculation History

Calculation history is managed using pandas and can be persisted to a CSV file.

Each calculation contains information such as:

- Operation
- First operand
- Second operand
- Result
- Timestamp

The calculator supports:

- Automatic history tracking
- CSV persistence
- Manual save
- Manual load
- Configurable maximum history size
- History display
- Clearing history
- Undo
- Redo

Runtime-generated history files are excluded from Git.

---

## Undo and Redo

The calculator implements undo and redo using the Memento design pattern.

After performing calculations:

```text
undo
```

restores the previous calculator state.

Use:

```text
redo
```

to restore a state that was previously undone.

Performing a new calculation after an undo updates the calculator's state history appropriately.

---

## Input Validation

User input is validated before calculations are performed.

The input validation system handles cases such as:

- Invalid numeric input
- Empty input
- Values outside the configured maximum range
- Unsupported values
- Invalid operation input

Numeric values are converted to Python `Decimal` objects to provide controlled decimal arithmetic.

---

## Error Handling

The application uses custom exceptions to distinguish different failure conditions.

These include errors related to:

- Configuration
- Input validation
- Mathematical operations

The calculator handles expected errors without terminating the REPL.

Examples include:

- Division by zero
- Invalid number formats
- Invalid roots
- Invalid configuration values
- Failed history persistence
- Unexpected operation errors

Exception chaining is used where appropriate so the original cause of an operation failure is preserved.

---

## Logging

The calculator includes logging support for application activity and errors.

Log locations can be controlled through calculator configuration.

Runtime-generated log files are excluded from Git so they are not committed to the repository.

---

## Testing

The project uses:

- `pytest`
- `pytest-cov`

Run the complete test suite with:

```bash
pytest
```

The test suite includes tests for:

- Calculations
- Calculator behavior
- Configuration
- Memento functionality
- REPL behavior
- Custom exceptions
- History
- Input validation
- Operations
- Error handling
- Persistence
- Undo and redo
- Observer behavior

### Coverage

The project currently contains **196 automated tests**.

The test suite achieves:

- **100% statement coverage**
- **100% branch coverage**
- **448/448 statements covered**
- **88/88 branches covered**

Coverage is enforced through `pytest.ini` using:

```text
--cov=app
--cov-branch
--cov-report=term-missing
--cov-report=html
--cov-fail-under=100
```

Running:

```bash
pytest
```

will therefore fail if total test coverage falls below 100%.

An HTML coverage report is generated in:

```text
htmlcov/
```

The generated coverage directory is excluded from version control.

---

## Continuous Integration

The project uses GitHub Actions for continuous integration.

The workflow is located at:

```text
.github/workflows/tests.yml
```

The workflow runs automatically for:

- Pushes to the `main` branch
- Pull requests targeting the `main` branch

The CI process:

1. Checks out the repository.
2. Sets up Python.
3. Installs dependencies from `requirements.txt`.
4. Runs the pytest test suite.
5. Measures statement and branch coverage.
6. Requires 100% test coverage.

A CI run fails if the test suite fails or coverage falls below the required threshold.

---

## Git Ignore Configuration

The repository excludes files that should not be committed, including:

```text
venv/
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.coverage
htmlcov/
.env
history/
logs/
test_history/
test_logs/
.DS_Store
.vscode/
.idea/
```

This keeps generated files, local configuration, virtual environments, logs, history data, editor settings, and test artifacts out of version control.

---

## Technologies Used

- Python 3
- Decimal
- pandas
- python-dotenv
- pytest
- pytest-cov
- Git
- GitHub
- GitHub Actions

---

## Running Final Verification

Before submitting the project, run:

```bash
pytest
```

The expected result is:

```text
196 passed
Required test coverage of 100% reached.
Total coverage: 100.00%
```

You can also check for whitespace errors with:

```bash
git diff --check
```

and review the repository status with:

```bash
git status
```

---

## License

This project includes a `LICENSE` file. See that file for the applicable license terms.