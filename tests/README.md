# Battleship Tests

## Installation

```bash
pip install -r requirements.txt
```

## Running Tests

### Run all tests
```bash
pytest
```

### Run tests with more details
```bash
pytest -v
```

### Run a single test file
```bash
pytest test_board.py
pytest test_fleet.py
pytest test_fleet_commander.py
```

### Run a specific test class
```bash
pytest test_board.py::TestShipPlacement
```

### Run a single test
```bash
pytest test_board.py::TestShipPlacement::test_can_place_ship_on_empty_board
```

## Coverage (Test Coverage)

### Generate coverage report
```bash
pytest --cov=battleship_game
```

### HTML coverage report
```bash
pytest --cov=battleship_game --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Project Structure

```
battleship_game/
├── board.py
├── fleet.py
├── fleet_commander.py
├── computer_fleet.py
├── game.py
├── config.py
└── main.py

tests/  (or battleship_tests/)
├── conftest.py              # Fixtures for all tests
├── test_board.py           # Tests for Board class
├── test_fleet.py           # Tests for Ship classes
└── test_fleet_commander.py # Tests for FleetManager
```

## What is being tested?

### test_board.py
- Board initialization
- Ship placement (valid/invalid)
- Hits and misses
- Sinking ships

### test_fleet.py
- Ship initialization
- Registering hits
- Sinking ships

### test_fleet_commander.py
- FleetManager initialization
- Placing ships
- Receiving shots
- Fleet defeated
