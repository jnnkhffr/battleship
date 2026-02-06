# Battleship Tests

## Installation

```bash
pip install -r requirements.txt
```

## Tests ausführen

### Alle Tests ausführen
```bash
pytest
```

### Tests mit mehr Details
```bash
pytest -v
```

### Einzelne Test-Datei ausführen
```bash
pytest test_board.py
pytest test_fleet.py
pytest test_fleet_commander.py
```

### Spezifische Test-Klasse ausführen
```bash
pytest test_board.py::TestShipPlacement
```

### Einzelnen Test ausführen
```bash
pytest test_board.py::TestShipPlacement::test_can_place_ship_on_empty_board
```

## Coverage (Test-Abdeckung)

### Coverage Report erstellen
```bash
pytest --cov=battleship_game
```

### HTML Coverage Report
```bash
pytest --cov=battleship_game --cov-report=html
```

Dann öffne `htmlcov/index.html` im Browser.

## Projektstruktur

```
battleship_game/
├── board.py
├── fleet.py
├── fleet_commander.py
├── computer_fleet.py
├── game.py
├── config.py
└── main.py

tests/  (oder battleship_tests/)
├── conftest.py              # Fixtures für alle Tests
├── test_board.py           # Tests für Board-Klasse
├── test_fleet.py           # Tests für Schiffs-Klassen
└── test_fleet_commander.py # Tests für FleetManager
```

## Was wird getestet?

### test_board.py
- Board-Initialisierung
- Schiffsplatzierung (gültig/ungültig)
- Treffer und Fehlschüsse
- Schiff versenken

### test_fleet.py
- Schiffs-Initialisierung
- Treffer registrieren
- Schiff versenken

### test_fleet_commander.py
- FleetManager-Initialisierung
- Schiffe platzieren
- Schüsse empfangen
- Flotte besiegt
